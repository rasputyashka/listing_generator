from docxtpl import DocxTemplate
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ListingSource:
    path: str
    text: str


filters = [".py"]

items = []

doc = DocxTemplate("files/doc.docx")
context = {"items": "if x > 2:\nprint('x > 2')"}
doc.render(context, autoescape=True)
doc.save("generated_doc.docx")
