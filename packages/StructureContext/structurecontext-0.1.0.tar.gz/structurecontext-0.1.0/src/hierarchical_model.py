import logging
logging.basicConfig(level=logging.DEBUG)

import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '4'

from typing import List, Dict, Tuple
import random
import matplotlib.pyplot as plt
import itertools
import cProfile
import yappi
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, Qwen2ForCausalLM, Qwen2PreTrainedModel, Qwen2Model, DynamicCache

from .hierarchical_context import ContextNode



class HierarchicalModel:
    """
    层次化上下文的模型包装类,实现逐层深入的上下文搜索和生成
    """
    @staticmethod
    def rotate_half(x):
        """
        Copied from transformers.models.llama.modeling_llama.rotate_half. 
        Rotates half the hidden dims of the input.
        """
        x1 = x[..., : x.shape[-1] // 2]
        x2 = x[..., x.shape[-1] // 2 :]
        return torch.cat((-x2, x1), dim=-1)
    
    @staticmethod
    def sort_key(node_ns, target_ns):
        """
        按照part文件路径与target_node文件路径的区别大小排序
        """
        node_ns = node_ns.split(".")
        target_ns = target_ns.split(".")
        diff_pos = 0
        while diff_pos < len(node_ns) and diff_pos < len(target_ns):
            if node_ns[diff_pos] != target_ns[diff_pos]:
                break
            diff_pos += 1
        return diff_pos
    
    @staticmethod
    def remove_after_target(node_list, target_node):
        """
        删除节点列表中的目标节点以及文件内在目标节点之后的节点 并且将剩余节点按文件外节点、同文件节点 进行排序
        
        参数:
            node_list - 节点列表
            target_node - 目标节点
        返回:
            过滤后的节点列表
        """
        # 获取目标节点所在文件
        target_file = target_node.file_path
        # 过滤后的节点列表
        out_file_nodes = []
        in_file_nodes = []
        
        # 遍历节点列表
        for node in node_list:
            # 如果节点不在目标文件中,直接保留
            if node.file_path != target_file and len(node.content):
                out_file_nodes.append(node)
                continue
                
            # 如果节点在目标文件中且在目标节点之前,保留该节点
            if node.begin_line < target_node.begin_line and len(node.content):
                in_file_nodes.append(node)
        
        return out_file_nodes+in_file_nodes
    
    def __init__(self, model, lm_head, tokenizer):
        self.model = model
        self.max_layer = len(self.model.layers)
        self.lm_head = lm_head
        self.tokenizer = tokenizer
        self.device = model.device
        self.max_context_length = 1536
        self.max_length = 512
        self.output_attentions = False
        
        # 项目数据库
        self.context_dict = None
        self.target_node = None
        
        # 层展开参数
        self.spread_layer = 8
        self.max_spread_turn = 16
        self.max_node_length = 256
        self.max_node_num = 64
        self.max_infile_node_num = 32
        self.attn_window = 8 # 使用输入中最后的attn_window个token计算注意力
        
        # 采样参数
        self.top_p = 0.8
        self.top_k = 20
        self.temperature = 0.7
        pass
    
    def node_length(self, node):
        """
        获取输入的token长度
        """
        length = min(self.max_context_length, len(self.tokenizer.tokenize(node.content)))
        return length
    
    def encode_init_hidden(self, input_ids):
        """
        编码初始hidden 即模型输入未经过第一次Attn计算前的hidden
        """
        input_ids = input_ids
        inputs_embeds = self.model.embed_tokens(input_ids)
        # create position embeddings to be shared across the decoder layers
        return inputs_embeds
    
    def encode_by_layer(self, hidden_states, start_layer, end_layer, begin_pos = 0, instruct_kv = None):
        """
        将hidden_states从第start_layer层到第end_layer层进行编码
        参数:
            hidden_states: 输入hidden [seq_len, hidden_dim]
            start_layer: 起始层索引 int
            end_layer: 结束层索引 int
            begin_pos: 起始位置索引 int
        返回:
            all_key: key向量 [layer_num, head_num, seq_len, dim]
            all_value: value向量 [layer_num, head_num, seq_len, dim]
            all_hidden: hidden向量 [layer_num, seq_len, hidden_dim]
        """
        assert len(hidden_states.shape) == 2, "hidden_states must be [seq_len, hidden_dim]"
        seq_len = hidden_states.shape[0]
        hidden_list = []
        hidden_states = hidden_states.unsqueeze(0)
        # create position embeddings to be shared across the decoder layers
        position_ids = torch.arange(
                begin_pos, begin_pos+hidden_states.shape[1], device=hidden_states.device
            )
        position_embeddings = self.model.rotary_emb(hidden_states, position_ids.unsqueeze(0))
        causal_mask = self.model._update_causal_mask(
            None, hidden_states, position_ids, instruct_kv, False
        )
        past_key_value = DynamicCache()
        if instruct_kv is not None:
            for layer in range(start_layer, end_layer+1):
                past_key_value.update(instruct_kv.key_cache[layer], instruct_kv.value_cache[layer], layer)

        for layer_id in range(start_layer, end_layer+1):
            decoder_layer = self.model.layers[layer_id]
            layer_outputs = decoder_layer(
                    hidden_states,
                    attention_mask=causal_mask,
                    position_ids=position_ids.unsqueeze(0),
                    use_cache = True,
                    past_key_value = past_key_value,
                    output_attentions=False,
                    position_embeddings=position_embeddings,
                )
            hidden_states = layer_outputs[0]
            hidden_list.append(layer_outputs[0].squeeze(0))

        all_key = torch.stack(past_key_value.key_cache[start_layer:end_layer+1], dim=1).squeeze(0).detach()
        all_value = torch.stack(past_key_value.value_cache[start_layer:end_layer+1], dim=1).squeeze(0).detach()
        all_hidden = torch.stack(hidden_list, dim=0).detach()
        
        # all_key去除instruct_kv中的key和value
        if instruct_kv is not None:
            all_key = all_key[:,:,instruct_kv.seen_tokens:]
            all_value = all_value[:,:,instruct_kv.seen_tokens:]
            
        del hidden_states, hidden_list, past_key_value, position_ids, position_embeddings, causal_mask
        assert all_key.shape[0] == all_value.shape[0] == all_hidden.shape[0] == end_layer - start_layer + 1, "layer num error"
        assert all_key.shape[-2] == all_value.shape[-2] == all_hidden.shape[-2] == seq_len, "seq_len error"
        return all_key, all_value, all_hidden


    def extend_nodeseq(self, node_list: List[ContextNode]) -> Tuple[torch.Tensor, torch.Tensor]:
        # 如果当前在处理代码节点序列，则为了整合上下文信息，将节点的前序节点拼接直到填满上下文窗口
        if len(node_list) == 0:
            return []
        
        file_ns = node_list[0].file_ns
        
        high_list = []
        node_parts = None
        file_length = {}
        for pos, node in enumerate(node_list):
            if node.type in ["file", "folder", "repository"]:
                high_list.append(node)
            elif node_parts == None:
                node_parts = [[node]]
                file_length[node.file_ns] = node.length
            elif node.file_ns == node_parts[-1][-1].file_ns and node.begin_line == node_parts[-1][-1].end_line:
                node_parts[-1].append(node)
                file_length[node.file_ns] += node.length
            else:
                node_parts.append([node])
                if node.file_ns not in file_length:
                    file_length[node.file_ns] = node.length
                else:
                    file_length[node.file_ns] += node.length
            
        extend_node_list = node_parts if node_parts else []

        all_length = sum([node.length for node in node_list])
        unfinished_ids = [i for i in range(len(extend_node_list))] if len(extend_node_list) > 0 else []
        now_part = 0
        while (all_length < 30000) and len(unfinished_ids):
            now_part = now_part%len(unfinished_ids)
            now_ids = unfinished_ids[now_part]
            now_node = extend_node_list[now_ids][0]

            while now_node.type not in ["file", "folder", "repository"] and now_node.previous is None:
                now_node = self.context_dict[now_node.parent]

            if now_node.type in ["file", "folder", "repository"] or now_node.previous is None:
                unfinished_ids.remove(now_ids)
            else:
                previous_node = self.context_dict[now_node.previous]
                assert previous_node.type not in ["folder", "file", "repository"]
                
                """while len(previous_node.children):
                    previous_node = self.context_dict[previous_node.children[-1]]"""
                
                if previous_node.type in ["function", "class"] and previous_node.length == 0:
                    heads = previous_node.dfs_heads(self.context_dict)
                    previous_node.content = "\n".join([head.content for head in heads])+'\n'
                    self.context_dict[previous_node.namespace].content = previous_node.content
                    pass
                if not hasattr(previous_node, "token_ids") or previous_node.token_ids == None:
                    tokens = self.tokenizer(previous_node.content)['input_ids']
                    previous_node.token_ids = tokens
                previous_node.length = min(self.max_node_length, len(previous_node.token_ids))
                
                #判断前序是不是已经接触到上一个节点
                if now_ids > 0 and previous_node.begin_line < extend_node_list[now_ids-1][-1].end_line:
                    unfinished_ids.remove(now_ids)
                elif file_length[now_node.file_ns] + previous_node.length > int(self.max_context_length):
                    unfinished_ids.remove(now_ids)
                else:
                    extend_node_list[now_ids] = [previous_node]+extend_node_list[now_ids]
                    now_part += 1
                    all_length += previous_node.length
                    file_length[now_node.file_ns] += previous_node.length
        
        extend_parts = []
        extend_part = []
        for part in extend_node_list:
            if len(extend_part)==0 or part[0].file_ns == extend_part[0].file_ns:
                extend_part+=part
            else:
                extend_parts.append(extend_part)
                extend_part = part
        if len(extend_part):
            extend_parts.append(extend_part)

        if len(high_list):
            extend_parts = [high_list]+extend_parts
        
        return extend_parts

    def collect_children(self, nodes: List[ContextNode]) -> List[ContextNode]:
        """收集节点的所有子节点 如果不存在子节点则继续保留当前节点 按父节点内子节点列表顺序排序"""
        nodes = [node for node in nodes if isinstance(node, ContextNode)]
        # nodes.sort(key=lambda x: ((x.file_path if x.file_path else x.namespace), x.begin_line))
        children = []
        keep_nodes = []
        for node in nodes:
            if len(node.children) == 0:
                children.append(node)
            if len(node.children) != 0:
                for child_ns in node.children:
                    children.append(self.context_dict[child_ns])
                
        return children
        
    def cluster_brothers(self, nodes: List[ContextNode], add_target=False) -> List[List[str]]:
        """
        将节点列表按照文件进行聚类 并填补缺失的语法上级 例如如果保留了一个类函数里的代码片段 则此类函数的head节点 此类的head节点 此文件的head节点都需要保留以保证文件内节点组织成的代码段结构正确
        """
        node_parts = {}
        now_part = []
        nodes.sort(key=lambda x: (x.type=="file", self.sort_key(x.file_path if x.file_path else x.namespace, self.target_node.file_ns), x.begin_line))
        if add_target:
            nodes.append(self.target_node)
        for node in nodes:
            file_ns = node.file_ns if node.type not in ['file', 'folder'] else " "
            if file_ns not in node_parts:
                if len(node.content):
                    now_part = []
                    node_parts[file_ns] = set()
                    parent = self.context_dict[node.parent]
                    if node.type not in ["file", "folder"]:
                        while parent.type not in ["folder", "repository"]:
                            now_part.append(self.context_dict[parent.children[0]])
                            parent = self.context_dict[parent.parent]
                    now_part = now_part[::-1]
                    now_part.append(node)
                    node_parts[file_ns].update(now_part)
                else:
                    qika = 1
            else:
                if len(node.content):
                    now_part = []
                    parent = self.context_dict[node.parent]
                    if node.type not in ["file", "folder"]:
                        while parent.type not in ["folder", "repository"]:
                            if self.context_dict[parent.children[0]] in node_parts[file_ns]:
                                break
                            now_part.append(self.context_dict[parent.children[0]])
                            parent = self.context_dict[parent.parent]
                    now_part = now_part[::-1]
                    now_part.append(node)
                    node_parts[file_ns].update(now_part)
                else:
                    qika = 1
        
        # 排序并分类
        infile_part = None
        high_part = None
        cross_parts = []
        for key in node_parts:
            if key == " ":
                high_part = sorted(node_parts[key], key=lambda x: (x.type=="file", self.sort_key(x.file_ns if x.file_ns else x.namespace, self.target_node.file_ns), x.begin_line, x.end_line))
            elif key == self.target_node.file_ns:
                infile_part = sorted(node_parts[key], key=lambda x: (self.sort_key(x.file_ns if x.file_ns else x.namespace, self.target_node.file_ns), x.begin_line, x.end_line))
            else:
                cross_parts.append(sorted(node_parts[key], key=lambda x: (self.sort_key(x.file_ns if x.file_ns else x.namespace, self.target_node.file_ns), x.begin_line, x.end_line)))
        cross_parts.sort(key=lambda x: (self.sort_key(x[0].file_ns if x[0].file_ns else x[0].namespace, self.target_node.file_ns), len((x[0].file_ns if x[0].file_ns else x[0].namespace).split("."))))
        node_parts = cross_parts
        if high_part:
            for node in high_part:
                if node.type in ["folder", "file"] and node.length == 0:
                    instruct = "\n## Cross-file contents from {}".format(node.content[2:-1])
                    instruct += "\n\n"
                    node.content = instruct
                    for idx, child_ns in enumerate(node.children):
                        if self.context_dict[child_ns].type in ["folder", "file"]:
                            node.content += self.context_dict[child_ns].content + '\n'
                        elif self.context_dict[child_ns].type in ["function", "class"]:
                            heads = self.context_dict[child_ns].dfs_heads(self.context_dict)
                            node.content += "\n".join([head.content for head in heads])+'\n'
                    node.content += "\n"
                    self.context_dict[node.namespace].content = node.content
                    pass
            node_parts = [high_part] + node_parts
        
        for part in node_parts:
            for node in part:
                if node.type == "code" and node.name == "_head" and node.length == 0:
                    instruct = "\n## Cross-file contents from {}\n\n".format(node.content[2:-1])
                    node.content = instruct
                    self.context_dict[node.namespace].content = node.content
                if node.type in ["function", "class"] and node.length == 0:
                    heads = node.dfs_heads(self.context_dict)
                    # node.content = "\n".join([head.content for head in heads])+'\n'
                    node.content = "".join([self.context_dict[child].content for child in node.children])
                    self.context_dict[node.namespace].content = node.content
                    pass
        
        for idx, part in enumerate(node_parts):
            part_length = 0
            for idy, node in enumerate(part):
                if not hasattr(node, "token_ids") or node.token_ids == None:
                    tokens = self.tokenizer(node.content)['input_ids']
                    node.token_ids = tokens
                if node.type in ["folder", "file"]:
                    node.length = min(self.max_context_length, len(node.token_ids))
                else:
                    node.length = min(self.max_node_length, len(node.token_ids))
                    if node.file_ns != self.target_node.file_ns and part_length + node.length > self.max_context_length:
                        node_parts[idx] = part[:idy]
                        break
                    part_length += node.length
        
        if infile_part:
            # 移除目标节点以及目标节点之后的节点
            infile_part.remove(self.target_node)
            infile_part = [node for node in infile_part if node.end_line <= self.target_node.begin_line]
            for node in infile_part:
                if node.type == "code" and node.name == "_head" and node.length == 0:
                    instruct = "\n## In-file contents from {}\n\n".format(node.content[2:-1])
                    node.content = instruct
                    self.context_dict[node.namespace].content = node.content
                if node.type in ["function", "class"] and node.length == 0:
                    heads = node.dfs_heads(self.context_dict)
                    node.content = "\n".join([head.content for head in heads])+'\n'
                    self.context_dict[node.namespace].content = node.content
                    pass
            infile_length = 0
            for idx, node in enumerate(infile_part[::-1]):
                if not hasattr(node, "token_ids") or node.token_ids == None:
                    tokens = self.tokenizer(node.content)['input_ids']
                    node.token_ids = tokens
                node.length = min(self.max_node_length, len(node.token_ids))
                infile_length += node.length
                if infile_length > self.max_context_length:
                    infile_part = infile_part[::-1][:idx][::-1]
                    break
            node_parts = node_parts + [infile_part]
            
        return node_parts

    def cut_to_encode(self, node_parts, extend_parts, max_length=3200):
        """
        将part拼接成尽量填充模型窗口以降低编码次数
        """
        encode_parts = []
        encode_tokens = []
        encode_masks = []
        now_part = []
        now_token = []
        now_mask = []
        now_length = 0
        for idx, node_part in enumerate(node_parts):
            if node_part[0].type in ["file", "folder"]:
                now_length = 0
                now_part = []
                now_token = []
                now_mask = []
                for idy, node in enumerate(extend_parts[idx]):
                    now_length += node.length
                    if node in node_part:
                        now_part.append(node)
                    now_token += node.token_ids[:node.length]
                    now_mask += [1 if node in node_part else 0]*node.length
                    if (idy == len(extend_parts[idx])-1) or (now_length+extend_parts[idx][idy+1].length > max_length):
                        encode_parts.append(now_part)
                        encode_tokens.append(now_token)
                        encode_masks.append(now_mask)
                        now_length = 0
                        now_part = []
                        now_mask = []
                        now_token = []
            else:
                part_length = sum([node.length for node in extend_parts[idx]])
                now_length += part_length
                now_part += node_part
                for idy, node in enumerate(extend_parts[idx]):
                    now_token += node.token_ids[:node.length]
                    now_mask += [1 if node in node_part else 0]*node.length
                if (idx == len(node_parts)-1) or (now_length+sum([node.length for node in extend_parts[idx+1]]) > max_length):
                    encode_parts.append(now_part)
                    encode_tokens.append(now_token)
                    encode_masks.append(now_mask)
                    now_length = 0
                    now_part = []
                    now_mask = []
                    now_token = []
        
        return encode_parts, encode_tokens, encode_masks
            

        
    def shift_pos(self, key:torch.Tensor, pos:int):
        """
        基于ROPE位置编码对输入向量进行平移
        输入:
            key: torch.Tensor((num), head_num, seq_len, head_dim)
            pos: int
        输出:
            key: torch.Tensor((num), head_num, seq_len, head_dim)
        """
        if pos == 0:
            return key
        length = key.shape[-2]
        key_divice = key.device
        key = key
        dim_num = len(key.shape)
        if dim_num == 3:
            key = key.unsqueeze(0)
        if pos > 0:
            # 由于是统一移动相同位置，因此position_ids值全部为pos
            position_ids = torch.full(
                (1, length), pos, device=key.device
            )
            position_embeddings = self.model.rotary_emb(key, position_ids)
            cos, sin = position_embeddings
        elif pos < 0:
            position_ids = torch.full(
                (1, length), -pos, device=key.device
            )
            position_embeddings = self.model.rotary_emb(key, position_ids)
            cos, sin = position_embeddings
            sin = -sin
        cos = cos.unsqueeze(1)
        sin = sin.unsqueeze(1)
        k_embed = (key * cos) + (HierarchicalModel.rotate_half(key) * sin)
        if dim_num == 3:
            k_embed = k_embed.squeeze(0)
        return k_embed
            
    def sample_next_idx(self, logits: torch.Tensor):
        """
        采样输出 基于top-p和temperature超参数
        """
        # 对logits应用temperature
        logits = logits / self.temperature
        
        # 计算softmax概率
        probs = torch.nn.functional.softmax(logits, dim=-1)
        
        # 按概率从大到小排序
        sorted_probs, sorted_indices = torch.sort(probs, descending=True)
        
        # 计算累积概率
        cumsum_probs = torch.cumsum(sorted_probs, dim=-1)
        
        # 找到累积概率超过top_p的位置
        mask = cumsum_probs > self.top_p
        mask[..., 1:] = mask[..., :-1].clone()
        mask[..., 0] = 0
        
        
        # 将不在top_p范围内的概率置为0
        sorted_probs.masked_fill_(mask, 0.0)
        
        if self.top_k and self.top_k < sorted_probs.shape[-1]:
            sorted_probs[..., self.top_k:] = 0.0
        
        # 重新归一化概率
        sorted_probs_sum = torch.sum(sorted_probs, dim=-1, keepdim=True)
        sorted_probs = sorted_probs / sorted_probs_sum
        
        # 按概率采样
        idx = torch.multinomial(sorted_probs, num_samples=1)
        
        # 获取采样的token id
        next_idx = sorted_indices[0, idx[0]]
        
        return next_idx, probs

    def select_high_attention_nodes(self, nodes_ns: List[str], attn_scores: torch.Tensor, min_num=8) -> List[ContextNode]:
        """
        根据注意力分数筛选高注意力节点
        """
        
        def weight_sum(attn_scores):
            """
            对注意力分数矩阵沿输入（即倒数第二维）进行加权求和，并返回加权后的结果。
            输入的attn_scores为(batch_size, head_num, query_len, key_len)
            输出的weighted_sum为(batch_size, head_num, key_len)
            """
            weights = torch.tensor([1, 1, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25]).bfloat16()
            # 因为越靠后的步骤权重越大，因此需要倒序
            weights = torch.flip(weights, dims=[0])
            weights = weights.to(attn_scores.device)
            # 截断多余的部分
            attn_scores = attn_scores[:,:,-weights.shape[0]:,:]
            weights = weights[-attn_scores.shape[-2]:]
            weighted_sum = torch.einsum('...ij,...i->...j', attn_scores, weights)
            return weighted_sum
        
        def filter_file(node):
            if node.name != "__init__":
                return True
            return False
        
        target_file = self.target_node.file_ns
        nodes = [self.context_dict[ns] for ns in nodes_ns]
        may_change = False
        for node in nodes:
            if len(node.children) > 0:
                may_change = True
                break
        if self.target_node.class_ns:
            inclass_codes = [node.namespace for node in nodes if (node.type not in ["file", "folder"] and node.file_ns == target_file and node.class_ns == self.target_node.class_ns)]
            infile_codes = [node.namespace for node in nodes if (node.type not in ["file", "folder"] and node.file_ns == target_file and node.class_ns != self.target_node.class_ns)]
        else:
            inclass_codes = []
            infile_codes = [node.namespace for node in nodes if (node.type not in ["file", "folder"] and node.file_ns == target_file)]
        cross_codes = [node.namespace for node in nodes if (node.type not in ["file", "folder"] and node.file_ns != target_file)]
        file_nodes = [node.namespace for node in nodes if (node.type in ["file"])]
        folder_nodes = [node.namespace for node in nodes if (node.type in ["folder"])]
        
        # 如果没有任何筛选 则直接返回所有节点
        if len(infile_codes)<=min_num and len(cross_codes) <= min_num and len(file_nodes) <= 2 and len(folder_nodes) <= 2:
            new_cross_context = self.collect_children([self.context_dict[node] for node in (folder_nodes + file_nodes)])
            old_cross_code_context = self.collect_children(cross_codes,)
            infile_context = self.collect_children([self.context_dict[node] for node in infile_codes])
            inclass_context = self.collect_children([self.context_dict[node] for node in inclass_codes])
            
            min_cross_num = min_num 
            max_free_num = max(3*self.max_node_num, 384)
            node_free_num = max_free_num
            
        else:
            cross_num = len(cross_codes)
            infile_num = len(infile_codes)
            file_num = len(file_nodes)
            folder_num = len(folder_nodes)

            """
            此处分开寻找 类内 文件内 和 跨文件 节点
            类内节点全部保留
            文件内节点选择前66%最高注意力的节点 
            跨文件节点选择前33%最高注意力的节点 
            另外 每类代码节点 至少选择min_num个节点 每类文件节点至少选择2个节点
            """
            file_num = min(max(3, int(file_num * 0.33)), 6)
            folder_num = min(max(3, int(folder_num * 0.66)), 9)
            # 之前的跨文件代码节点保留至少min_cross_num(1/3)，max_corss_num的其余位置如果有剩余则继续保留直到到顶
            min_cross_num = max(1, int(min_num), int(cross_num * 0.33)) 
            max_free_num = max(3*self.max_node_num, 256)
            node_free_num = max_free_num if may_change else self.max_node_num
            min_infile_num = min(self.max_infile_node_num, infile_num)
            min_class_num = len(inclass_codes)
            
            node_size = [node.length for node in nodes]
            node_attn = torch.zeros(len(nodes), dtype=torch.float32)
            now_pos = 0
            weight_scores = attn_scores[0,:,:,:].mean(dim=-2) # weight_sum(attn_scores) # 
            for i, node in enumerate(nodes):
                node_scores = weight_scores[:, now_pos:now_pos+node_size[i]]
                now_pos += node_size[i]
                try:
                    # 对节点的注意力为其20%最高注意力的平均
                    # 先找到20%最高注意力
                    node_scores = node_scores.topk(int(1 + node_size[i]*0.2), dim=-1).values
                    node_attn[i] = node_scores.mean(dim=-1).mean(dim=0)
                except:
                    node_attn[i] = 0
            
            filter_value = node_attn.mean().item()
            selected_nodes = {
                "inclass": [],
                "infile": [],
                "cross": [],
                "file": [],
                "folder": [],
            }
            flag_type = {
                "inclass": False,
                "infile": False,
                "cross": False,
                "file": False,
                "folder": False,
            }
            
            infile_length = 0
            _, indices = torch.sort(node_attn, descending=True)
            # top_k = max(1, min_num, int(len(nodes) * 0.3))  # 至少选择min_num个节点
            # selected_indices = indices[:top_k]
            for idx in indices:
                idx = idx.item()
                node = nodes[idx]
                if node.namespace in inclass_codes:
                    selected_nodes["inclass"].append(node)
                    if len(selected_nodes["inclass"]) >= min_class_num:
                        flag_type["inclass"] = True
                    
                elif node.namespace in infile_codes and node.name != "_head":
                    selected_nodes["infile"].append(node)
                    if len(selected_nodes["infile"]) >= min_infile_num:
                        flag_type["infile"] = True
                        continue
                    
                elif not flag_type["cross"] and node.namespace in cross_codes and node.name != "_head":
                    selected_nodes["cross"].append(node)
                    node_free_num -= max(1, len(node.children))
                    if len(selected_nodes["cross"]) >= min_cross_num and node_free_num<=0: # or node_attn[idx] < filter_value:
                        flag_type["cross"] = True
                        continue
                        
                elif not flag_type["file"] and node.namespace in file_nodes and filter_file(node):
                    node_free_num -= max(1, len(node.children))
                    selected_nodes["file"].append(node)
                    if len(selected_nodes["file"]) >= file_num and node_free_num<=0:
                        flag_type["file"] = True
                        continue
                
                elif not flag_type["folder"] and node.namespace in folder_nodes:
                    if len(selected_nodes["folder"]) >= folder_num:
                        flag_type["folder"] = True
                        continue
                    selected_nodes["folder"].append(node)
                    
                if flag_type["inclass"] and flag_type["infile"] and flag_type["cross"] and flag_type["file"] and flag_type["folder"]:
                    break
            
            
            # 收集子节点作为下一层上下文
            new_cross_context = self.collect_children(selected_nodes["folder"]+selected_nodes["file"])
            old_cross_code_context = self.collect_children(selected_nodes["cross"])
            infile_context = self.collect_children(selected_nodes["infile"])
            inclass_context = self.collect_children(selected_nodes["inclass"])
        

        # 删去目标节点以及同文件内在目标节点之后的节点
        infile_context = self.remove_after_target(infile_context, self.target_node)
        inclass_context = self.remove_after_target(inclass_context, self.target_node)
        
        
        file_context = [node for node in new_cross_context if node.type in ['file', 'folder']]
        new_cross_code_context = [node for node in new_cross_context if node.type not in ['folder', 'file']]
        
        if may_change:
            old_corss_num = max(min_cross_num, max_free_num-len(new_cross_code_context))
        else:
            old_corss_num = max(self.max_node_num, min_cross_num)
        if len(old_cross_code_context) > old_corss_num:
            # 删除多的旧crossfile节点
            if old_corss_num<=0:
                logging.debug(f"old crossfile remove all nodes")
                old_cross_code_context = []
            else:
                cut_num = len(old_cross_code_context)-old_corss_num

                logging.debug(f"crossfile old code remove {cut_num} nodes")
                old_cross_code_context = old_cross_code_context[:-cut_num]
        
        if len(old_cross_code_context) + len(new_cross_code_context) > max_free_num:
            # 删除多的新crossfile节点
            code_num = max_free_num - len(old_cross_code_context)
            if code_num<=0:
                logging.debug(f"new crossfile remove all nodes")
                new_cross_code_context = []
                
            elif code_num<len(new_cross_code_context):
                cut_num = len(new_cross_code_context) - code_num
                cut_range = min(len(new_cross_code_context), 3*cut_num)
                logging.debug(f"crossfile new code remove {cut_num} nodes")
                new_cross_code_context = new_cross_code_context[:-cut_range] + random.sample(new_cross_code_context[-cut_range:], cut_range-cut_num)
        
        cross_code_context = new_cross_code_context+old_cross_code_context
        
        all_context = file_context + cross_code_context + infile_context + inclass_context
        
        if len(file_context) > 0 and False:
            folder_num = len([node for node in file_context if node.type == "folder"])
            file_num = len([node for node in file_context if node.type == "file"])
            cross_num = len(cross_code_context)
            infile_num = len(infile_context+inclass_context)
            logging.info(f"folder_num: {folder_num}, file_num: {file_num}, cross_num: {cross_num}, infile_num: {infile_num}")
            
        change = False
        for node in all_context:
            if node.namespace not in nodes_ns:
                change = True
                break
        
        if change == False:
            if len(cross_code_context) > self.max_node_num:
                change = True

        return all_context, change        

    def search_context_step(self, inputs_embeds, old_context: List[ContextNode], instruct_kv: DynamicCache = None, prefix_kv: DynamicCache = None) -> List[ContextNode]:
        """
        根据当前上下文节点计算当前生成的注意力分布，再根据注意力分布搜索新的上下文节点
        """
        """
        # 设置时钟类型（CPU时间或挂钟时间）
        yappi.set_clock_type("wall")  # 可选"wall"模式

        # 启动分析器（支持线程级控制）
        yappi.start(builtins=True, profile_threads=False)
        """
        attn_scores = None
        old_context = [node for node in old_context if len(node.content) > 0]
        node_parts = self.cluster_brothers(old_context, add_target=False)
        if self.spread_layer < self.max_layer:
            extend_parts = self.extend_nodeseq([node for part in node_parts for node in part])
        else:
            extend_parts = node_parts
            
        # 将全部ids切分组织成适合输入的大小
        encode_parts, encode_ids_parts, encode_mask_parts = self.cut_to_encode(node_parts, extend_parts, max_length=3200)          
            
        # 收集指令kv
        past_key_values:DynamicCache = DynamicCache()
        if instruct_kv:
            instruct_length = instruct_kv.key_cache[0].shape[2]
            for layer in range(0, self.spread_layer+1):
                past_key_values.update(instruct_kv.key_cache[layer], instruct_kv.value_cache[layer], layer)
        else:
            instruct_length = 0
        now_pos = instruct_length
            
        # 按切分块收集项目上下文kv
        all_hiddens = list(itertools.chain.from_iterable(encode_ids_parts))
        all_hiddens = torch.tensor(all_hiddens, device=self.device)
        all_hiddens = self.encode_init_hidden(all_hiddens).squeeze(0)
        all_mask = torch.tensor(list(itertools.chain.from_iterable(encode_mask_parts)), device=self.device).bool()
        logging.debug(f"extend_length: {all_hiddens.shape[0]}, context_length: {all_mask.sum()}")
        for idx, part in enumerate(encode_parts):
            part_length = len(encode_mask_parts[idx])
            hidden = all_hiddens[now_pos-instruct_length:now_pos-instruct_length+part_length]
            mask = all_mask[now_pos-instruct_length:now_pos-instruct_length+part_length]
            
            part_key, part_value, part_hidden = self.encode_by_layer(hidden, 0, self.spread_layer, now_pos, past_key_values)
            assert part_key.shape[2] == part_value.shape[2] == part_hidden.shape[1] == part_length
            now_pos += part_key.shape[2]
            key = part_key[:,:,mask]
            value = part_value[:,:,mask]
            for layer in range(0, self.spread_layer+1):
                past_key_values.update(key[layer].unsqueeze(0), value[layer].unsqueeze(0), layer)
            del hidden, part_key, part_value, part_hidden
            del key, value, mask
        
        # 收集局部上下文kv，包含当前生成直接输入（函数头+需求描述）和已生成部分
        begin_pos = 0
        if prefix_kv is not None and len(prefix_kv.key_cache) >= self.spread_layer+1:
            begin_pos = prefix_kv.key_cache[0].shape[2]
            for layer_idx in range(0, self.spread_layer+1):
                prefix_k = self.shift_pos(prefix_kv.key_cache[layer_idx], now_pos-instruct_length)
                prefix_v = prefix_kv.value_cache[layer_idx]
                past_key_values.update(prefix_k, prefix_v, layer_idx)
                assert prefix_k.shape[2] == prefix_v.shape[2] == begin_pos
                del prefix_k, prefix_v
            
                
        # 编码位置信息和掩码 输入的起始位置为上下文总长度+缓存输入的长度
        cache_position = torch.arange(
            now_pos+begin_pos, now_pos+begin_pos+inputs_embeds.shape[1], device=inputs_embeds.device
        )
        if cache_position[-1] >= 32000:
            logging.info("超出32000的上下文尺寸")
        position_ids = cache_position.unsqueeze(0)
        causal_mask = self.model._update_causal_mask(
                None, inputs_embeds, cache_position, past_key_values, output_attentions=True
            )
            
        # 从0到self.spread_layer层运算
        for layer_idx in range(0, self.spread_layer+1):
            # 编码当前层输入特征
            layer = self.model.layers[layer_idx]
            if layer_idx == 0:
                layer_output_hidden = None
                hidden_states = inputs_embeds
            else:
                hidden_states = layer_output_hidden

            # create position embeddings to be shared across the decoder layers
            position_embeddings = self.model.rotary_emb(hidden_states, position_ids)

            layer_outputs = layer(
                    hidden_states,
                    attention_mask=causal_mask,
                    position_ids=position_ids,
                    past_key_value=past_key_values,
                    output_attentions=True,
                    use_cache=True,
                    cache_position=cache_position,
                    position_embeddings=position_embeddings,
                )
            layer_output_hidden = layer_outputs[0]
            
            # 收集注意力分布
            if layer_idx > 4 and layer_idx <= self.spread_layer:
                if attn_scores == None:
                    attn_scores = layer_outputs[1][:,:,-self.attn_window:].detach().to("cpu")
                else:
                    attn_scores = torch.cat([attn_scores, layer_outputs[1][:,:,-self.attn_window:].detach().to("cpu")], dim=1)
                
            # 释放显存
            del layer_outputs
                
            
        # 检索高注意力节点并展开为新上下文
        curr_context = [node.namespace for node in old_context]
        high_attn_nodes, change_flag = self.select_high_attention_nodes(curr_context, attn_scores, min_num=16)    

        """
        # yappi结束
        yappi.stop()
        stats = yappi.get_func_stats()
        stats.print_all(columns={ 0: ("name", 128),1: ("ncall", 5),2: ("tsub", 8),3: ("ttot", 8),4: ("tavg", 8) })
        """
        return high_attn_nodes, change_flag
        
    
    def generate_step(
                        self, 
                        input_ids: torch.Tensor, 
                        prefix_kv, 
                        init_context_nodes: List[str],
                        instruct_kv: DynamicCache
                    ) -> dict:
        """
        执行一步生成,包含逐层深入的上下文搜索
        返回生成的token_id和使用的上下文节点
        """
        
        """# 设置时钟类型（CPU时间或挂钟时间）
        yappi.set_clock_type("wall")  # 可选"wall"模式

        # 启动分析器（支持线程级控制）
        yappi.start(builtins=True, profile_threads=False)"""
        
        curr_context = [self.context_dict[ns] for ns in init_context_nodes]
        inputs_embeds = self.model.embed_tokens(input_ids)
        
        # 逐层处理
        change_flag = True
        change_num = 0
        while change_flag:
            curr_context, change_flag = self.search_context_step(inputs_embeds, curr_context, instruct_kv, prefix_kv)
            change_num += 1
            if change_num >= self.max_spread_turn:
                logging.info("到达展开轮次上限{}".format(self.max_spread_turn))
                change_flag = False
        
        #过滤项目上下文
        curr_context = [node for node in curr_context if len(node.content) > 0]
        
        # 构建上下文kvcache
        past_key_values:DynamicCache = DynamicCache()
        # 收集指令
        if instruct_kv:
            instruct_length = instruct_kv.key_cache[0].shape[2]
            for layer in range(0, self.max_layer):
                past_key_values.update(instruct_kv.key_cache[layer], instruct_kv.value_cache[layer], layer)
        else:
            instruct_length = 0
        now_pos = instruct_length
        
        # 收集项目上下文
        node_parts = self.cluster_brothers(curr_context, add_target=False)
        extend_parts = self.extend_nodeseq([node for part in node_parts for node in part])
            
        # 将全部ids切分组织成适合输入的大小
        encode_parts, encode_ids_parts, encode_mask_parts = self.cut_to_encode(node_parts, extend_parts, max_length=3200)          
            
        # 按切分块收集项目上下文kv
        all_ids = torch.tensor(list(itertools.chain.from_iterable(encode_ids_parts)), device=self.device).unsqueeze(0)
        all_mask = torch.tensor(list(itertools.chain.from_iterable(encode_mask_parts)), device=self.device).bool()
        for idx, part in enumerate(encode_parts):
            part_length = len(encode_mask_parts[idx])
            part_ids = all_ids[:, now_pos-instruct_length:now_pos-instruct_length+part_length]
            part_mask = all_mask[now_pos-instruct_length:now_pos-instruct_length+part_length]
            part_position = torch.arange(
                now_pos, now_pos+part_length, device=self.device
            ).unsqueeze(0)
            now_cache_length = past_key_values.seen_tokens
            # 复制一份past_key_values以防模型修改
            part_past_key_values = DynamicCache()
            for layer in range(0, self.max_layer):
                part_past_key_values.update(past_key_values.key_cache[layer], past_key_values.value_cache[layer], layer)
            part_output = self.model.forward(
                input_ids=part_ids,
                position_ids=part_position,
                past_key_values=part_past_key_values,
                output_attentions=False,
                use_cache=True
            )
            # 从part_output中收集kv
            for layer in range(0, self.max_layer):
                part_k = part_output.past_key_values[layer][0][:,:,now_cache_length:]
                part_v = part_output.past_key_values[layer][1][:,:,now_cache_length:]
                
                part_k = part_k[:,:,part_mask]
                part_v = part_v[:,:,part_mask]
                past_key_values.update(part_k, part_v, layer)
                del part_k, part_v
            
            now_pos += part_length
            del part_output, part_ids, part_mask, part_position, part_length
        del all_ids, all_mask
        
        # 收集局部上下文kv，包含当前生成直接输入（函数头+需求描述）和已生成部分
        begin_pos = 0
        if prefix_kv is not None:
            begin_pos = prefix_kv.key_cache[0].shape[2]
            for layer_idx in range(0, self.max_layer):
                prefix_k = self.shift_pos(prefix_kv.key_cache[layer_idx].to(self.device), now_pos-instruct_length)
                prefix_v = prefix_kv.value_cache[layer_idx].to(self.device)
                past_key_values.update(prefix_k, prefix_v, layer_idx)
                assert prefix_k.shape[2] == prefix_v.shape[2] == begin_pos
                del prefix_k, prefix_v
        else:
            prefix_kv = DynamicCache()
        
        position_ids = torch.arange(
            now_pos+begin_pos, now_pos+begin_pos+input_ids.shape[1], device=self.device
        ).unsqueeze(0)
        if position_ids[0,-1] >= 32000:
            logging.info("超出32000的上下文尺寸")
        now_cache_length = past_key_values.seen_tokens
        output = self.model.forward(
            input_ids=input_ids,
            position_ids=position_ids,
            past_key_values=past_key_values,
            output_attentions=False,
            use_cache=True
        )
        
        # 将新输入的kv收集到prefix_kv中
        for layer_idx in range(0, self.max_layer):
            input_k = self.shift_pos(output.past_key_values.key_cache[layer_idx][:,:,now_cache_length:], -now_pos+instruct_length)
            input_v = output.past_key_values.value_cache[layer_idx][:,:,now_cache_length:]
            prefix_kv.update(input_k, input_v, layer_idx)
            del input_k, input_v
        
        
        # 使用类方法进行采样
        last_hidden_state = output.last_hidden_state[:, -1:, :]
        logits = self.lm_head(last_hidden_state)
        next_idx, probs = self.sample_next_idx(logits[:, -1])

        info_dict = {
            "probs": probs,
            "logits": logits[:, -1],
            "next_idx": next_idx,
            "curr_context": [node.namespace for node in curr_context],
            "prefix_kv": prefix_kv,
            "position": now_pos+begin_pos
        }
        
        return info_dict

    def generate_step_nocontext(self, 
                        input_ids: torch.Tensor, 
                        prefix_kv: DynamicCache, 
                    ) -> dict:
        """
        执行一步生成,不包含上下文
        返回生成的token_id
        """
        output = self.model.forward(
            input_ids=input_ids,
            past_key_values=prefix_kv,
            output_attentions=False,
            use_cache=True
        )
        last_hidden_state = output.last_hidden_state
        prefix_kv = output.past_key_values
        logits = self.lm_head(last_hidden_state)
        next_idx, probs = self.sample_next_idx(logits[:, -1])
        return {
            "probs": probs,
            "logits": logits[:, -1],
            "next_idx": next_idx,
            "prefix_kv": prefix_kv,
        }
        
