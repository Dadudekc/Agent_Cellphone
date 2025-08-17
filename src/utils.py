from __future__ import annotations
from pathlib import Path
from typing import Union


def atomic_write(path: Union[str, Path], data: str) -> None:
    """Atomically write text data to a file.

    The data is first written to a temporary file in the same directory and
    then moved into place. This prevents readers from observing a partially
    written file.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(data, encoding="utf-8")
    tmp.replace(p)
