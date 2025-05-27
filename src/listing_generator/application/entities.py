from dataclasses import dataclass
from pathlib import Path


@dataclass
class ListingSource:
    path: Path
    text: str
