from PIL import Image
import os

def set_cmyk_dpi_to_300(input_path, output_path=None, dpi=300):
    """
    将 CMYK 图像的 DPI 设置为指定值（默认 300），不改变像素和颜色模式
    
    :param input_path: 输入文件路径（支持 .tiff, .jpg 等）
    :param output_path: 输出文件路径（默认在原文件名后加 _300dpi）
    :param dpi: 目标 DPI（默认 300）
    """
    # 自动设置输出路径
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_300dpi{ext}"
    
    # 打开图像
    with Image.open(input_path) as img:
        print(f"原始信息: {img.format}, {img.mode}, 尺寸: {img.size}, DPI: {img.info.get('dpi', 'N/A')}")
        
        # 确保是 CMYK 模式（如果不是，可选择转换或报错）
        if img.mode != 'CMYK':
            print(f"⚠️ 警告: 输入图像不是 CMYK 模式 ({img.mode})，将尝试转换...")
            img = img.convert('CMYK')
        
        # 保存时设置 DPI（注意：Pillow 用 (dpi, dpi) 表示水平/垂直 DPI）
        save_kwargs = {
            'format': img.format or 'TIFF',
            'dpi': (dpi, dpi),
            'compression': 'tiff_lzw' if output_path.lower().endswith(('.tiff', '.tif')) else None
        }
        
        # JPEG 需要额外参数
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True
        
        # 保存
        img.save(output_path, **save_kwargs)
set_cmyk_dpi_to_300("D:\python\my-workspace2\pythonDevPu\output_cmyk_image.tiff")