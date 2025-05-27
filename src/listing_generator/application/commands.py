from pathlib import Path

from listing_generator.application.entities import ListingSource


class FormatTemplateAndSaveCommand:
    def __init__(
        self,
        formatter_type,
        template_path: Path,
        out_path: Path,
        source_directory: Path,
    ):
        self.formatter_type = formatter_type
        self.template_path = template_path
        self.out_path = out_path
        self.source_directory = source_directory

    def execute(self, paths: list[Path], minimize=False):
        items = []
        for path in paths:
            path_text = path.read_text(encoding="utf-8")
            if minimize:
                path_text = path_text.replace("\n\n", "\n")
            items.append(
                ListingSource(
                    path=path.relative_to(self.source_directory),
                    text=path_text,
                )
            )
        formatter = self.formatter_type(self.template_path)
        document = formatter.render(items)
        document.save(self.out_path)


class FormatTemplateCommand:
    def __init__(
        self,
        formatter_type,
        template_path: Path,
        source_directory: Path,
    ):
        self.formatter_type = formatter_type
        self.template_path = template_path
        self.source_directory = source_directory

    def execute(self, paths: list[Path], minimize=False):
        items = []
        for path in paths:
            path_text = path.read_text(encoding="utf-8")
            if minimize:
                path_text = path_text.replace("\n\n", "\n")
            items.append(
                ListingSource(
                    path=path.relative_to(self.source_directory),
                    text=path_text,
                )
            )
        formatter = self.formatter_type(self.template_path)
        document = formatter.render(items)
        return document
