from docxtpl import DocxTemplate
from dataclasses import dataclass
import sys




filters = [".py"]

items = []

doc = DocxTemplate("files/doc.docx")
context = {"items": "if x > 2:\nprint('x > 2')"}
doc.render(context, autoescape=True)
doc.save("generated_doc.docx")

def main():

