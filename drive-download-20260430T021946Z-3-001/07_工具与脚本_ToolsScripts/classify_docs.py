import os
import shutil

# 定义源目录和目标父目录
source_dir = r"e:\下载\summarize-driver\drive-download-20260430T021946Z-3-001\07_工具与脚本_ToolsScripts"
parent_dir = r"e:\下载\summarize-driver\drive-download-20260430T021946Z-3-001"

# 定义映射规则 (不带后缀的文件名 -> 目标子目录名)
mapping = {
    "FPGA的硬件特性详细描述和其用途": "04_硬件架构与平台_HardwarePlatforms",
    "LED灯是低电平为亮嘛": "06_基础知识与概念_BasicsConcepts",
    "Pcle配置空间的作用": "01_通信协议_HardwareProtocols",
    "Uart波特率计算以及串行总线协议": "01_通信协议_HardwareProtocols",
    "内存地址线和数据线计算": "06_基础知识与概念_BasicsConcepts",
    "存储器特性和分类": "04_硬件架构与平台_HardwarePlatforms",
    "音视频带宽计算": "06_基础知识与概念_BasicsConcepts"
}

def classify_files():
    # 获取目录下所有文件
    if not os.path.exists(source_dir):
        print(f"错误: 源目录不存在 {source_dir}")
        return

    files = os.listdir(source_dir)
    moved_count = 0

    print("开始分类文件...")
    
    for filename in files:
        # 提取不带后缀的文件名
        base_name, ext = os.path.splitext(filename)
        
        if ext.lower() in ['.md', '.docx']:
            # 检查是否在映射规则中
            if base_name in mapping:
                target_subdir = mapping[base_name]
                target_path = os.path.join(parent_dir, target_subdir)
                
                # 确保目标目录存在
                if not os.path.exists(target_path):
                    print(f"警告: 目标目录不存在 {target_path}，跳过 {filename}")
                    continue
                    
                src_file = os.path.join(source_dir, filename)
                dst_file = os.path.join(target_path, filename)
                
                # 如果目标文件已存在，先删除或重命名（此处选择覆盖）
                try:
                    if os.path.exists(dst_file):
                        os.remove(dst_file)
                    
                    shutil.move(src_file, dst_file)
                    print(f" [成功] 移动: {filename} -> {target_subdir}")
                    moved_count += 1
                except Exception as e:
                    print(f" [失败] 移动 {filename}: {e}")

    print(f"\n分类完成，共移动 {moved_count} 个文件。")

if __name__ == "__main__":
    classify_files()
