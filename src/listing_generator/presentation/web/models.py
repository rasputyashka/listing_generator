from typing import Optional

from pydantic import BaseModel


class ProcessingOptions(BaseModel):
    remove_empty_files: bool = False
    minimize_line_count: bool = False


class ProcessingConfig(BaseModel):
    upload_id: str
    selected_files: list[str]
    options: ProcessingOptions
    include_files: list[str] = ["*"]
    exclude_files: list[str] = []
    include_extensions: list[str] = ["*"]
    exclude_extensions: list[str] = []


class FileNode(BaseModel):
    name: str
    type: str  # "file" or "directory"
    children: Optional[list["FileNode"]] = None


class FileListResponse(BaseModel):
    upload_id: str
    files: list[FileNode]
    message: str


FileNode.model_rebuild()
