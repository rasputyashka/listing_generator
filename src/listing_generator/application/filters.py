from abc import ABC, abstractmethod
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class BaseFilter(ABC):
    @abstractmethod
    def filter(self, *args, **kwargs) -> list[Path]:
        return NotImplemented


class EmptyFilter(BaseFilter):
    def __init__(self, items):
        self.items = items

    def filter(self):
        return self.items


class IncludeExtensionFilter(BaseFilter):
    def __init__(self, wrapee: BaseFilter, included_extensions: list[str]):
        self.wrapee = wrapee
        self.included_extensions = included_extensions

    def filter(self) -> list[Path]:
        items = self.wrapee.filter()
        if self.included_extensions == ["*"]:
            return items
        return [item for item in items if item.suffix in self.included_extensions]


class ExcludeExtensionFilter(BaseFilter):
    def __init__(self, wrapee: BaseFilter, excluded_extensions: list[str]):
        self.wrapee = wrapee
        self.excluded_extensions = excluded_extensions

    def filter(self) -> list[Path]:
        items = self.wrapee.filter()
        return [item for item in items if item.suffix not in self.excluded_extensions]


class InlcudeFileNameFilter(BaseFilter):
    def __init__(self, wrapee: BaseFilter, included_filenames: list[str]):
        self.wrapee = wrapee
        self.included_filenames = included_filenames

    def filter(self) -> list[Path]:
        items = self.wrapee.filter()
        if self.included_filenames == ["*"]:
            return items
        return [item for item in items if item.name in self.included_filenames]


class ExcludeFileNameFilter(BaseFilter):
    def __init__(self, wrapee: BaseFilter, excluded_filenames: list[str]):
        self.wrapee = wrapee
        self.excluded_filenames = excluded_filenames

    def filter(self) -> list[Path]:
        items = self.wrapee.filter()
        return [item for item in items if item.name not in self.excluded_filenames]
