from abc import ABC, abstractmethod
from pathlib import Path
from os.path import splitext


class BaseFilter(ABC):
    @abstractmethod
    def filter(self, *args, **kwargs) -> list[Path]:
        return NotImplemented


class EmptyFilter(BaseFilter):
    def __init__(self, items):
        self.items = items

    def filter(self):
        return self.items


class ExtensionFilter(BaseFilter):
    def __init__(self, wrapee: BaseFilter, allowed_extensions: list[str]):
        self.wrapee = wrapee
        self.allowed_extensions = allowed_extensions

    def filter(self) -> list[Path]:
        items = self.wrapee.filter()
        return [item for item in items if item.suffix[1:] in self.allowed_extensions]
