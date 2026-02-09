from logging import log
import os
import uuid
from datetime import datetime
import oss2

# 从环境变量读取（推荐）
ACCESS_KEY_ID = "11"
ACCESS_KEY_SECRET = "22"
ENDPOINT = "https://oss-cn-shenzhen.aliyuncs.com"
BUCKET_NAME = "jxe-env-dev-outside"
FILE_PATH_PREFIX = "outside/fms/python-file-convert/img/"

def upload_file_to_oss(local_file_path: str, remote_dir: str = "uploads/") -> str:
    """
    上传本地文件到 OSS
    
    :param local_file_path: 本地文件路径（如 "/tmp/photo.jpg"）
    :param remote_dir: OSS 目录前缀（如 "user/avatar/"）
    :return: 文件的公网访问 URL
    """

    # 初始化 Bucket
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)

    # 生成唯一文件名（保留原扩展名）
    ext = os.path.splitext(local_file_path)[1]  # .jpg
    filename = f"{uuid.uuid4().hex}{ext}"
    object_key = f"{remote_dir.rstrip('/')}/{filename}"

    # 上传文件
    with open(local_file_path, 'rb') as f:
        bucket.put_object(object_key, f)

    # 返回公网 URL（要求 Bucket 读权限为 public-read）
    file_url = f"https://{BUCKET_NAME}.{ENDPOINT.replace('https://', '')}/{object_key}"
    return file_url


def upload_bytes_to_oss(file_bytes: bytes, original_filename: str, remote_dir: str = "uploads/") -> str:
    """
    上传字节流（如 FastAPI/Flask 接收的上传文件）到 OSS
    
    :param file_bytes: 文件字节内容
    :param original_filename: 原始文件名（用于提取扩展名）
    :param remote_dir: OSS 目录前缀
    :return: 文件的公网访问 URL
    """
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)

    file_name = os.path.splitext(original_filename)[0]
    ext = os.path.splitext(original_filename)[1].lower()
    if not ext:
        ext = ".bin"
    
    filename = f"{FILE_PATH_PREFIX}{file_name}{ext}"
    print(filename)
    object_key = f"{filename}"
    print(object_key)

     # 上传文件

    bucket.put_object(object_key, file_bytes)
    
    file_url = f"https://{BUCKET_NAME}.{ENDPOINT.replace('https://', '')}/{object_key}"
    return file_url