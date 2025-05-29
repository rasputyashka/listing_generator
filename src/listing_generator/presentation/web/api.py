import zipfile
import os
import shutil
import uuid
import io
from pathlib import Path
import logging

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates


from listing_generator.application.commands import (
    FormatTemplateCommand,
)
from listing_generator.application.dto import FormatTemplateDTO
from listing_generator.application.formatters import TemplateFormatter
from listing_generator.presentation.web.models import (
    FileNode,
    ProcessingConfig,
    FileListResponse,
)


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

templates = Jinja2Templates(directory=os.getenv("TEMPLATE_DIR", "templates"))
UPLOAD_DIR = Path("uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def extract_zip_structure(zip_path: str) -> list[FileNode]:
    """Extract file structure from ZIP file and return as tree structure"""
    structure = {}

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file_info in zip_ref.filelist:
            if file_info.filename.endswith("/"):
                continue

            parts = file_info.filename.split("/")
            current = structure

            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    # File
                    current[part] = {"type": "file", "size": file_info.file_size}
                else:
                    # Directory
                    if part not in current:
                        current[part] = {"type": "directory", "children": {}}
                    current = current[part]["children"]

    return convert_structure_to_nodes(structure)


def convert_structure_to_nodes(structure: dict) -> list[FileNode]:
    """Convert nested dictionary structure to FileNode objects"""
    nodes = []

    for name, info in structure.items():
        if info["type"] == "directory":
            children = convert_structure_to_nodes(info["children"])
            nodes.append(
                FileNode(
                    name=name, type="directory", children=children if children else None
                )
            )
        else:
            nodes.append(FileNode(name=name, type="file"))

    return sorted(nodes, key=lambda x: (x.type == "file", x.name))


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/api/upload-files", response_model=FileListResponse)
async def upload_files(
    zip_file: UploadFile = File(...), docx_template: UploadFile = File(...)
):
    upload_id = str(uuid.uuid4())
    upload_dir = os.path.join(UPLOAD_DIR, upload_id)
    os.makedirs(upload_dir, exist_ok=True)

    zip_path = os.path.join(upload_dir, "archive.zip")
    docx_path = os.path.join(upload_dir, "document.docx")

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(zip_file.file, buffer)

    with open(docx_path, "wb") as buffer:
        shutil.copyfileobj(docx_template.file, buffer)

    extract_dir = os.path.join(upload_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    zip_files = []
    for root, _, files in os.walk(extract_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), extract_dir)
            zip_files.append(rel_path.replace("\\", "/"))

    file_structure = extract_zip_structure(zip_path)

    return FileListResponse(
        upload_id=upload_id, files=file_structure, message="Files uploaded successfully"
    )


@app.post("/api/process-files")
async def process_files(config: ProcessingConfig):
    logger.debug(f"Processing {len(config.selected_files)} selected files")
    logger.debug(f"Options: {config.options}")
    logger.debug(f"Include files: {config.include_files}")
    logger.debug(f"Exclude files: {config.exclude_files}")
    logger.debug(f"Include extensions: {config.include_extensions}")
    logger.debug(f"Exclude extensions: {config.exclude_extensions}")

    dir_path = (UPLOAD_DIR / config.upload_id / "extracted").absolute()
    template_path = UPLOAD_DIR / config.upload_id / "document.docx"
    items = config.selected_files
    items = [Path(dir_path) / item for item in items]

    dto = FormatTemplateDTO(
        formatter_type=TemplateFormatter,
        template_path=template_path,
        source_directory=dir_path,
        file_list=items,
        excluded_extensions=config.exclude_extensions,
        excluded_filenames=config.exclude_files,
        included_extensions=config.include_extensions,
        included_filenames=config.include_files,
        minimize_line_count=config.options.minimize_line_count,
        skip_empty_files=config.options.remove_empty_files,
    )
    command = FormatTemplateCommand()
    document = command.execute(dto)

    docx_stream = io.BytesIO()
    document.save(docx_stream)

    return StreamingResponse(
        io.BytesIO(docx_stream.getvalue()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=document.docx"},
    )


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Document Processor API is running"}
