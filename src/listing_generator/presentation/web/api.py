from os import getenv
import zipfile
import os
import tempfile
import shutil
import uuid

from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

templates = Jinja2Templates(directory=getenv("TEMPLATE_DIR"))


app = FastAPI()

# Temporary storage for uploads (in production, use proper storage)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Store upload data (in production, use a database)
upload_data = {}


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/upload")
async def upload_files(zip: UploadFile = File(...), docx: UploadFile = File(...)):
    upload_id = str(uuid.uuid4())
    upload_dir = os.path.join(UPLOAD_DIR, upload_id)
    os.makedirs(upload_dir, exist_ok=True)

    zip_path = os.path.join(upload_dir, "archive.zip")
    docx_path = os.path.join(upload_dir, "document.docx")

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(zip.file, buffer)

    with open(docx_path, "wb") as buffer:
        shutil.copyfileobj(docx.file, buffer)

    extract_dir = os.path.join(upload_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    zip_files = []
    for root, _, files in os.walk(extract_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), extract_dir)
            zip_files.append(rel_path.replace("\\", "/"))  # Use forward slashes

    return {"uploadId": upload_id, "files": zip_files}


@app.post("/process")
async def process_files(
    upload_id: str = Form(...),
    files: list[str] = Form(...),
    minimize_output: bool = Form(False),
    remove_blanks: bool = Form(False),
    archive_name: str = Form("result.docx"),
):
    upload_directory = upload_id
    print(files)
