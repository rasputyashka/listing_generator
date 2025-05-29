from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class FormatTemplateAndSaveDTO:
    formatter_type: type
    template_path: Path
    source_directory: Path
    file_list: Iterable[Path]
    out_file_path: Path
    excluded_extensions: list[str]
    excluded_filenames: list[str]
    included_extensions: list[str]
    included_filenames: list[str]
    minimize_line_count: bool
    skip_empty_files: bool


@dataclass
class FormatTemplateDTO:
    formatter_type: type
    template_path: Path
    source_directory: Path
    file_list: Iterable[Path]
    excluded_extensions: list[str]
    excluded_filenames: list[str]
    included_extensions: list[str]
    included_filenames: list[str]
    minimize_line_count: bool
    skip_empty_files: bool
