# file_processor.py
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

def process_file(filepath):
    """示例：读取文件并生成报告"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        report = f"文件: {os.path.basename(filepath)}\n行数: {len(lines)}\n大小: {os.path.getsize(filepath)} 字节"
        return report
    except Exception as e:
        return f"错误: {str(e)}"

def main():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 弹出文件选择框
    filepath = filedialog.askopenfilename(
        title="请选择一个文本文件",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if filepath:
        result = process_file(filepath)
        messagebox.showinfo("处理结果", result)
    else:
        messagebox.showwarning("警告", "未选择文件")

if __name__ == "__main__":
    main()