from pathlib import Path

from listing_generator.application.commands import (
    FormatTemplateAndSaveCommand,
)
from listing_generator.application.dto import (
    FormatTemplateAndSaveDTO,
)
from listing_generator.application.formatters import TemplateFormatter

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="path to template document", required=True)
    parser.add_argument(
        "-d", help="path to directory with files needed for listing", required=True
    )
    parser.add_argument(
        "-iext", nargs="+", help="list of included extensions", default=["*"]
    )
    parser.add_argument(
        "-eext", nargs="+", help="list of excluded extensions", default=[]
    )
    parser.add_argument(
        "-iname", nargs="+", help="list of included filenames", default=["*"]
    )
    parser.add_argument(
        "-ename", nargs="+", help="list of excluded filenames", default=[]
    )
    parser.add_argument(
        "-o",
        help="path to result .docx file (explicit extension is required)",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--minimize",
        help="reduce amount of code by replacing doubled line breaks with one line break",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-s", "--skip-empty-files", help="skip empty files", action="store_true"
    )

    args = parser.parse_args()
    abs_doc_path = Path(args.i).absolute()
    abs_dir_path = Path(args.d).absolute()
    abs_output_doc_path = Path(args.o).absolute()
    minimize = args.minimize

    items = abs_dir_path.rglob("*")
    command = FormatTemplateAndSaveCommand()
    dto = FormatTemplateAndSaveDTO(
        formatter_type=TemplateFormatter,
        template_path=abs_doc_path,
        source_directory=abs_dir_path,
        file_list=items,
        excluded_extensions=args.eext,
        excluded_filenames=args.ename,
        included_extensions=args.iext,
        included_filenames=args.iname,
        minimize_line_count=minimize,
        skip_empty_files=args.skip_empty_files,
        out_file_path=abs_output_doc_path,
    )
    command.execute(dto)
