from pathlib import Path

from docxtpl import DocxTemplate

from listing_generator.application.entities import ListingSource


class TemplateFormatter:
    def __init__(self, template_path: Path):
        self.in_file = template_path

    def render(self, items: list[ListingSource]):
        context = {"items": items, "blank": ""}
        document = DocxTemplate(self.in_file)
        document.render(context, autoescape=True)
        return document
