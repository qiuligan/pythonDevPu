from PIL import Image, ImageCms

def merger(input_rgb_image_path, output_cmyk_image_path,dpi):
    """
    将RGB图像转换为CMYK图像。
    
    :param input_rgb_image_path: 输入的RGB图像路径。
    :param output_cmyk_image_path: 输出的CMYK图像路径。
    """
    # 打开RGB图像
    rgb_image = Image.open(input_rgb_image_path)
    
    # 创建sRGB和FOGRA39L（标准CMYK配置文件）的配置文件对象
    srgb_profile = ImageCms.createProfile("sRGB")
    cmyk_profile = ImageCms.getOpenProfile("D:/python/my-workspace2/pythonDevPu/ISOcoated_v2_300_eci.icc")  # 替换为实际路径
    
    # 创建转换器
    transform = ImageCms.buildTransform(srgb_profile, cmyk_profile, "RGB", "CMYK")
    
    # 应用转换
    cmyk_image = ImageCms.applyTransform(rgb_image, transform)
    
    # 保存转换后的图像
    cmyk_image.save(output_cmyk_image_path, quality=100)

    # 保存时设置 DPI（注意：Pillow 用 (dpi, dpi) 表示水平/垂直 DPI）
    save_kwargs = {
        'format': cmyk_image.format or 'tiff',
        'dpi': (dpi, dpi),
        'compression': 'tiff_lzw' if output_cmyk_image_path.lower().endswith(('.tiff', '.tif')) else None
    }
    
    # JPEG 需要额外参数
    if output_cmyk_image_path.lower().endswith('.jpg') or output_cmyk_image_path.lower().endswith('.jpeg'):
        save_kwargs['quality'] = 95
        save_kwargs['optimize'] = True
    
    # 保存
    cmyk_image.save(output_cmyk_image_path, **save_kwargs)

# 示例调用
merger("D:/python/my-workspace2/pythonDevPu/from.jpg", "D:/python/my-workspace2/pythonDevPu/output_cmyk_image.tiff",300)