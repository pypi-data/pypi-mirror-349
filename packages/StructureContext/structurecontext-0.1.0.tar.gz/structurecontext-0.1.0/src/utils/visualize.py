
"""
统计绘图相关的函数
"""

import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

def visualize_line(data: torch.tensor, label = [], save_path="/home/qikahh/projects/Structured_Code_Context/visualize.png"):
    """
    对于多维tensor 绘制折线图
    最后一维为x轴
    倒数第二维为不同样本，需要在它们之间计算均值和标准差
    如果有倒数第三维 则对应不同折线 名称为label里的对应元素
    """
    # 检查输入维度，不足的补全至3维，超过的从前方维度融合
    if len(data.shape) > 3:
        data = data.reshape(data.shape[-3:])
    while len(data.shape) < 3:
        data = data.unsqueeze(0)  
    
    # 检查label元素数量与data第0维长度是否一致
    if len(label) != data.shape[0]:
        label = [str(i) for i in range(data.shape[0])]
        
    # 沿第一维进行平均和标准差计算
    mean = data.mean(dim=1)
    std = data.std(dim=1)
    
    # 建造画布
    plt.figure(figsize=(10, 6))
    
    for i in range(data.shape[0]):
        plt.plot(range(mean[i].shape[-1]), mean[i], label=label[i])
        plt.fill_between(range(mean[i].shape[-1]), mean[i] - std[i], mean[i] + std[i], alpha=0.3)
    
    plt.xlabel('Layer')
    plt.ylabel('Weight Ratio(%)')
    
    plt.legend()
    plt.savefig(save_path)
    pass
        

def visualize_Passk(save_path="/home/qikahh/projects/Structured_Code_Context"):
    # 数据
    methods = ['Local', 'Infile', 'BM25', 'HierC']
    P1_SA = [21.51, 24.37, 23.93, 25.08]
    P1_NSA = [3.59, 11.81, 9.85, 15.09]
    R1_inclass = [13.66, 26.75, 20.30, 24.64]
    R1_infile = [9.15, 14.83, 13.09, 15.17]
    R1_cross = [5.79, 7.91, 7.22, 10.14]

    # 设置柱状图的宽度
    bar_width = 0.2
    x = np.arange(len(methods))

    # 绘制P@1的柱状图并保存
    plt.figure(figsize=(8, 6))
    plt.bar(x - bar_width/2, P1_SA, width=bar_width, label='P@1 SA', color='b')
    plt.bar(x + bar_width/2, P1_NSA, width=bar_width, label='P@1 NSA', color='g')

    plt.xlabel('方法')
    plt.ylabel('P@1')
    plt.title('P@1对比')
    plt.xticks(x, methods)
    plt.legend()
    plt.grid(axis='y')

    # 保存图像
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, 'P1_comparison.png'))  # 保存为PNG文件
    plt.close()  # 关闭当前图形

    # 绘制R@1的柱状图并保存
    plt.figure(figsize=(8, 6))
    plt.bar(x - bar_width, R1_inclass, width=bar_width, label='R@1 inclass', color='r')
    plt.bar(x, R1_infile, width=bar_width, label='R@1 infile', color='orange')
    plt.bar(x + bar_width, R1_cross, width=bar_width, label='R@1 cross', color='purple')

    plt.xlabel('方法')
    plt.ylabel('R@1')
    plt.title('R@1对比')
    plt.xticks(x, methods)
    plt.legend()
    plt.grid(axis='y')

    # 保存图像
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, 'R1_comparison.png'))  # 保存为PNG文件
    plt.close()  # 关闭当前图形

def visualize_passk_by_type(save_path="/home/qikahh/projects/DynamicStructredContext/Logs/passk_by_type.png"):
    """
    绘制不同方法生成独立函数与非独立函数时的pass@k
    data为一个字典，key为方法名，value为结果字典
    结果字典中key为（独立函数，非独立函数），value为pass@k字典
    pass@k字典中key为k，value为pass@k的值
    
    绘制图像为柱状图，横坐标为方法名，纵坐标为pass@k的值
    每个方法有两个柱子，一个表示独立函数，一个表示非独立函数
    每个柱子重叠不同k的pass@k，越低的k颜色越深，越放置在前景
    不同方法的相同函数类别、k的柱子颜色一致
    """
    data = {
        "Local": 
            [{"1": 19.29, "3": 29.30}, {"1": 4.78, "3": 8.26}],
        "BM25":
            [{"1": 28.78, "3": 37.25}, {"1": 16.58, "3": 22.89}],
        "RepoCoder": 
            [{"1": 28.72, "3": 38.35}, {"1": 22.50, "3": 29.74}],
        "Infile": 
            [{"1": 31.51, "3": 40.81}, {"1": 24.08, "3": 32.19}],
        "HierC": 
            [{"1": 36.45, "3": 43.71}, {"1": 25.71, "3": 36.28}],
    }
    
    # 获取方法名列表
    methods = list(data.keys())
    # 初始化颜色列表, 分别用蓝色和橙色标注SA和NSA的pass@1，淡蓝色和淡橙色标注pass@3
    colors = ['#1f77b4', '#ff7f0e', '#aec7e8', '#ffbb78']  # 蓝色、橙色、淡蓝色、淡橙色
    
    # 创建图形
    plt.figure(figsize=(10, 8))
    # 计算每个方法的x轴偏移量
    x_by_method = np.arange(len(methods))
    # 遍历每个方法
    for i, method in enumerate(methods):
        # 获取独立函数和非独立函数的pass@k字典
        SA_data, NSA_data = data[method]
        # 获取k值列表
        k_values = list(SA_data.keys())
        # 初始化x轴偏移量
        x_offset = x_by_method[i]
        # 绘制独立函数k=3的柱状图
        bars_SA = plt.bar(x_offset, SA_data['3'], width=0.3, color=colors[2], label='SA pass@3' if i == 0 else "")
        # 添加独立函数k=3的柱子具体值
        for bar in bars_SA:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')  # 调整y值以避免重叠
        # 绘制独立函数k=1的柱状图
        bars_SA = plt.bar(x_offset, SA_data['1'], width=0.3, color=colors[0], label='SA pass@1' if i == 0 else "")
        # 添加独立函数k=1的柱子具体值
        for bar in bars_SA:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')  # 调整y值以避免重叠
        # 绘制非独立函数k=3的柱状图
        bars_NSA = plt.bar(x_offset + 0.3, NSA_data['3'], width=0.3, color=colors[3], label='NSA pass@3' if i == 0 else "")
        # 添加非独立函数k=3的柱子具体值
        for bar in bars_NSA:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')  # 调整y值以避免重叠
        # 绘制非独立函数k=1的柱状图
        bars_NSA = plt.bar(x_offset + 0.3, NSA_data['1'], width=0.3, color=colors[1], label='NSA pass@1' if i == 0 else "")
        # 添加非独立函数k=1的柱子具体值
        for bar in bars_NSA:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')  # 调整y值以避免重叠
    
    # 设置x轴标签
    plt.xticks(x_by_method+0.15, methods)
    # 设置y轴标签
    plt.ylabel('Pass Rate(%)')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # 添加网格
    # 保存图像
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    
def visualize_recall_by_type(save_path="/home/qikahh/projects/DynamicStructredContext/Logs/recall_by_type.png"):
    """
    绘制不同方法生成结果对类内、文件内和跨文件的recall@k
        Recall@1 inclass	Recall@1 infile	Recall@1 crossfile
    Local	6.89	4.37	3.93
    Infile	60.91	25.18	20.31
    BM25	43.88	24.11	25.11
    RepoCoder	47.17	25.32	25.21
    HierC	67.22	31.09	27.26
    
    	Recall@3 inclass	Recall@3 infile	Recall@3 crossfile
    Local	15.42	9.26	8.58
    Infile	74.07	34.68	27.83
    BM25	49.17	26.46	27.25
    RepoCoder	57.00	30.59	30.60
    HierC	77.67	38.25	35.26
    """
    data = {
        "Local": {"inclass": [6.89, 15.42], "infile": [4.37, 9.26], "crossfile": [3.93, 8.58]},
        "BM25": {"inclass": [43.88, 49.17], "infile": [24.11, 26.46], "crossfile": [25.11, 27.25]},
        "RepoCoder": {"inclass": [47.17, 57.00], "infile": [25.32, 30.59], "crossfile": [25.21, 30.60]},
        "Infile": {"inclass": [60.91, 74.07], "infile": [25.18, 34.68], "crossfile": [20.31, 27.83]},
        "HierC": {"inclass": [67.22, 77.67], "infile": [31.09, 38.25], "crossfile": [27.26, 35.26]}
    }
    methods = list(data.keys())
    # 初始化颜色列表, 分别用蓝色、橙色、绿色表示inclass、infile、crossfile的recall@1，淡蓝色、淡橙色、淡绿色表示recall@3
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#aec7e8', '#ffbb78', '#90EE90']
    
    # 创建图形
    plt.figure(figsize=(10, 8))
    # 计算每个方法的x轴偏移量
    x_by_method = np.arange(len(methods))
    # 遍历每个方法
    for i, method in enumerate(methods):
        # 获取inclass、infile、crossfile的recall@1和recall@3
        inclass_recall1, inclass_recall3 = data[method]["inclass"]
        infile_recall1, infile_recall3 = data[method]["infile"]
        crossfile_recall1, crossfile_recall3 = data[method]["crossfile"]
        # 初始化x轴偏移量
        x_offset = x_by_method[i]
        # 绘制inclass的recall@1和recall@3
        bars_inclass_recall3 = plt.bar(x_offset, inclass_recall3, width=0.3, color=colors[3], label='inclass recall@3' if i == 0 else "")
        # 添加inclass的recall@3的柱子具体值
        for bar in bars_inclass_recall3:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')  # 调整y值以避免重叠
        bars_inclass_recall1 = plt.bar(x_offset, inclass_recall1, width=0.3, color=colors[0], label='inclass recall@1' if i == 0 else "")
        # 添加inclass的recall@1的柱子具体值
        for bar in bars_inclass_recall1:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')  # 调整y值以避免重叠
        # 绘制infile的recall@1和recall@3
        bars_infile_recall3 = plt.bar(x_offset + 0.3, infile_recall3, width=0.3, color=colors[4], label='infile recall@3' if i == 0 else "")
        # 添加infile的recall@3的柱子具体值
        for bar in bars_infile_recall3:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')  # 调整y值以避免重叠
        bars_infile_recall1 = plt.bar(x_offset + 0.3, infile_recall1, width=0.3, color=colors[1], label='infile recall@1' if i == 0 else "")
        # 添加infile的recall@1的柱子具体值
        for bar in bars_infile_recall1:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')  # 调整y值以避免重叠
        bars_crossfile_recall3 = plt.bar(x_offset + 0.6, crossfile_recall3, width=0.3, color=colors[5], label='crossfile recall@3' if i == 0 else "")
        # 添加crossfile的recall@3的柱子具体值
        for bar in bars_crossfile_recall3:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')  # 调整y值以避免重叠
        # 绘制crossfile的recall@1和recall@3
        bars_crossfile_recall1 = plt.bar(x_offset + 0.6, crossfile_recall1, width=0.3, color=colors[2], label='crossfile recall@1' if i == 0 else "")
        # 添加crossfile的recall@1的柱子具体值
        for bar in bars_crossfile_recall1:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')  # 调整y值以避免重叠
    
    # 设置x轴标签
    plt.xticks(x_by_method+0.3, methods)
    # 设置y轴标签
    plt.ylabel('Recall Rate(%)')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # 添加网格
    # 保存图像
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def visualize_tensor(tensor, title="Tensor Visualization", save_path="/home/qikahh/projects/Structured_Code_Context/visualize.png"):
    """
    可视化PyTorch张量
    
    Args:
        tensor (torch.Tensor): 要可视化的张量
        title (str): 图表标题
        save_path (str): 保存图片的路径,如果为None则显示图片
    """
    # 确保张量在CPU上并转换为numpy数组
    if tensor.is_cuda:
        tensor = tensor.cpu()
    data = tensor.detach().to(torch.float).numpy()
    
    # 创建新的图表
    plt.figure(figsize=(10, 8))
    
    # 如果是1D张量,显示折线图
    if len(data.shape) == 1:
        plt.plot(data)
        plt.xlabel("node")
        plt.ylabel("Value")
        plt.title(title)
        plt.show()
    
    # 如果是2D或更高维张量,显示最后两维的热力图
    else:
        # 如果维度大于2,只取最后两维
        if len(data.shape) > 2:
            # 计算需要展平的维度数
            dims_to_flatten = len(data.shape) - 2
            # 展平前面的维度
            new_shape = (-1,) + data.shape[-2:]
            data = data.reshape(new_shape)
            # 只显示第一个切片
            data = data[0]
            
        plt.imshow(data, cmap='viridis', aspect='auto')
        plt.colorbar()
    
    plt.title(title)
    
    if save_path:
        plt.savefig(save_path)
    plt.show()
    plt.close()
    
def visualize_attention(target_node, nodes, attn_scores: torch.Tensor, layer_id=0):
    target_file = target_node.file_path
    node_size = [node.length for node in nodes]
    node_attn = torch.zeros(len(nodes)+1, dtype=torch.float32)
    type_attn = torch.zeros(4, dtype=torch.float32)
    type_length = torch.zeros(4, dtype=torch.float32)
    now_pos = 0
    attn_scores = attn_scores[0, :, -1, :].detach().cpu()
    for i, node in enumerate(nodes):
        node_scores = attn_scores[:, now_pos:now_pos+node_size[i]]
        now_pos += node_size[i]
        try:
            node_attn[i] = node_scores[:,:].mean(dim=0).sum(dim=-1)
        except:
            node_attn[i] = 0
        if node.file_path and node.file_path == target_file:
            type_attn[2] += node_attn[i]
            type_length[2] += node_size[i]
        else:
            type_attn[3] += node_attn[i]
            type_length[3] += node_size[i]
    type_attn[1] = attn_scores[:, now_pos:-1].mean(dim=0).sum(dim=-1)
    type_length[1] = attn_scores[:, now_pos:-1].shape[-1]

    type_attn[0] = attn_scores[:, -1:].mean(dim=0).sum(dim=-1)
    type_length[0] = attn_scores[:, -1:].shape[-1]
    
    mean_type_attn = type_attn
    # visualize_tensor(node_attn, layer_id)
    
    return mean_type_attn

def visualize_cost(save_path="/home/qikahh/projects/DynamicStructredContext"):
    """
    绘制随上下文长度增加，编码的时间成本和显存成本的变化
    最后一项为项目平均长度，距离其他项差距过大，需要用锯齿状分开显示
    """
    length = [64, 128, 256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 9216, 12000, 402696]
    time = [207.7, 245.7, 281.4, 429.8, 780.1, 1595.0, 2423.5, 3438.0, 5794.4, 8632.1, 10328.2, 15319, 9758072.7]
    memory = [6818, 6836, 6880, 6990, 7306, 8500, 10136, 11246, 16332, 23613, 28058, 41709, 36396528]

    # 绘制折线图
    plt.figure(figsize=(8, 8))
    plt.plot(length[:-1], memory[:-1], marker='o', linestyle='-', color='r')
    
    plt.xlabel('Context Length')
    plt.ylabel('Memory Cost(MB)')
    
    if save_path:
        plt.savefig(os.path.join(save_path, "visualize_memory.png"))
    plt.show()
    plt.close()
    
    plt.figure(figsize=(8, 8))
    plt.plot(length[:-1], time[:-1], marker='o', linestyle='-', color='b')
    plt.xlabel('Context Length')
    plt.ylabel('Time Cost(ms)')
    plt.savefig(os.path.join(save_path, "visualize_time.png"))
    plt.show()
    plt.close()

if __name__ == "__main__":
    visualize_cost()
    pass