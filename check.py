from PIL import Image

img = Image.open("D:/python/my-workspace2/pythonDevPu/output_cmyk_300dpi.jpg")
print("DPI:", img.info.get('dpi'))  # 应输出 (300, 300)
print("Mode:", img.mode)           # 应输出 'CMYK'