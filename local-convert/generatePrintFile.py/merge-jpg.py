from PIL import Image

def save_cmyk_jpeg_300dpi(input_path, output_path, quality=95):
    """
    将图像保存为 CMYK 模式的 JPEG，DPI=300
    
    :param input_path: 输入文件（RGB 或 CMYK）
    :param output_path: 输出文件（.jpg）
    :param quality: JPEG 质量 (90-98 推荐)
    """
    with Image.open(input_path) as img:
        # 确保是 CMYK 模式
        if img.mode != 'CMYK':
            img = img.convert('CMYK')
        
        # 保存为 CMYK JPEG + 300 DPI
        img.save(
            output_path,
            format='JPEG',
            dpi=(300, 300),          # 设置 DPI
            quality=quality,         # 高质量（避免压缩失真）
            optimize=True,
            icc_profile=img.info.get("D:/python/my-workspace2/pythonDevPu/ISOcoated_v2_300_eci.icc")  # 保留 ICC 配置文件（如有）
        )

# 使用示例
save_cmyk_jpeg_300dpi("D:/python/my-workspace2/pythonDevPu/from.jpg", "D:/python/my-workspace2/pythonDevPu/output_cmyk_300dpi.jpg")