from pathlib import Path
from docxtpl import DocxTemplate

from listing_generator.filters import BaseFilter
from main import ListingSource


class TemplateFormatter:
    def __init__(self, template_path: Path):
        self.in_file = template_path

    def render(self, context, autoescape=True):
        document = DocxTemplate(self.in_file)
        document.render(context, autoescape=autoescape)
        return document

    def save_to_file(self, out_file, document):
        document.save(out_file)

    def get_rendered_text(self, document):
        return "foo"
