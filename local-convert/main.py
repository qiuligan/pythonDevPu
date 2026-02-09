from http.client import HTTPException
import shutil
import zipfile
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uploadFileToOSS import upload_bytes_to_oss
from pathlib import Path

app = FastAPI()

ALLOWED_EXTENSIONS = {".zip"}
BASE_DIR = Path(__file__).parent
print("Base directory:", BASE_DIR)
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = Path(BASE_DIR / "uploads")
EXTRACT_DIR = Path(BASE_DIR / "extracted")

def is_safe_path(basedir: Path, path: Path) -> bool:
    """防止路径遍历攻击（Zip Slip 漏洞）"""
    try:
        resolved = basedir.resolve()
        return str(path.resolve()).startswith(str(resolved))
    except Exception:
        return False
    
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    url = upload_bytes_to_oss(contents, file.filename, "")
    return {"file_url": url}

@app.post("/upload-zip/")
async def upload_and_extract(file: UploadFile = File(...)):
    # 1. 验证文件扩展名
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="仅支持 .zip 文件")
    
    # 2. 保存上传的 ZIP 文件
    zip_path = UPLOAD_DIR / file.filename
    with open(zip_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 4. 安全解压
    extract_subdir = EXTRACT_DIR / Path(file.filename).stem
    extract_subdir.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 检查每个文件路径是否安全
            for member in zip_ref.namelist():
                member_path = extract_subdir / member
                if not is_safe_path(extract_subdir, member_path):
                    raise HTTPException(status_code=400, detail="ZIP 文件包含非法路径（可能为 Zip Slip 攻击）")
            # 执行解压
            zip_ref.extractall(extract_subdir)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="无效的 ZIP 文件")

    # 5. 返回结果（可选：列出解压的文件）
    extracted_files = [
        str(p.relative_to(EXTRACT_DIR)) 
        for p in extract_subdir.rglob("*") if p.is_file()
    ]

    return JSONResponse({
        "message": "上传并解压成功",
        "extracted_to": str(extract_subdir),
        "files": extracted_files
    })