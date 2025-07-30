"""Create the JSONL that ms‑swift expects from a plain image directory."""
from __future__ import annotations

import json
from glob import glob
from pathlib import Path
from typing import Iterable

_SYSTEM = "You are NuExtract, a vision‑language model that outputs JSON following the provided template."
_USER_TEMPLATE = """# Template:
{
  "Subject": [
    {
      "Position": "string",
      "Clothing Items": [
        {
          "Item": ["blazer","tie","shirt","trousers","skirt","dress","jacket","sweater"],
          "Pattern": ["plain","striped","dotted","tartan","checked"],
          "Colors": {
            "Primary": ["red","blue","green","yellow","black","white","gray","purple","orange","pink"],
            "Secondary": ["red","blue","green","yellow","black","white","gray","purple","orange","pink","None"]
          }
        }
      ],
      "Logo": {
        "Shapes": ["string"],
        "Colors": {
          "Primary": ["red","blue","green","yellow","black","white","gray","purple","orange","pink"],
          "Secondary": ["red","blue","green","yellow","black","white","gray","purple","orange","pink","None"]
        },
        "Objects": ["string"],
        "Text": {
          "Content": "string",
          "Font": "string",
          "Color": ["red","blue","green","yellow","black","white","gray","purple","orange","pink","None"]
        }
      }
    }
  ]
}
# Context:
<image>"""

__all__ = ["prepare_dataset"]


def _build_record(img_path: str | Path) -> dict:
    return {
        "messages": [
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": _USER_TEMPLATE},
        ],
        "images": [str(img_path)],
    }


def prepare_dataset(img_dir: str | Path, jsonl_path: str | Path | None = None) -> Path:
    """Scan *img_dir* for files and write a JSONL ready for *swift*.

    If *jsonl_path* is None, a temp file is created next to *img_dir*.
    Returns the JSONL **Path**.
    """
    img_dir = Path(img_dir).expanduser().resolve()
    assert img_dir.is_dir(), f"{img_dir} is not a directory"

    if jsonl_path is None:
        jsonl_path = img_dir.with_suffix(".jsonl")
    jsonl_path = Path(jsonl_path).expanduser().resolve()

    paths: Iterable[Path] = sorted(Path(p) for p in glob(str(img_dir / "*.*")))
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for p in paths:
            json.dump(_build_record(p), f, ensure_ascii=False)
            f.write("\n")
    return jsonl_path
