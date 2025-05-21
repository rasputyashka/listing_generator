from pathlib import Path

from listing_generator.application.commands import FormatTemplateCommand
from listing_generator.application.filters import (
    ExcludeExtensionFilter,
    ExcludeFileNameFilter,
    IncludeExtensionFilter,
    EmptyFilter,
    InlcudeFileNameFilter,
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
    args = parser.parse_args()
    abs_doc_path = Path(args.i).absolute()
    abs_dir_path = Path(args.d).absolute()
    abs_output_doc_path = Path(args.o).absolute()

    items = abs_dir_path.rglob("*")
    filter = ExcludeFileNameFilter(
        InlcudeFileNameFilter(
            ExcludeExtensionFilter(
                IncludeExtensionFilter(
                    EmptyFilter(items),
                    included_extensions=args.iext,
                ),
                excluded_extensions=args.eext,
            ),
            included_filenames=args.iname,
        ),
        excluded_filenames=args.ename,
    )
    items = filter.filter()
    command = FormatTemplateCommand(
        TemplateFormatter, abs_doc_path, abs_output_doc_path, abs_dir_path
    )
    command.execute(items)
