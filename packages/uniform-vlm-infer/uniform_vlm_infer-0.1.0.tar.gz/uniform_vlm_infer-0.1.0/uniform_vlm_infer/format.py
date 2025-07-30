"""Convert the raw ms‑swift JSONL to a CSV."""
from __future__ import annotations

import json
import os
from pathlib import Path
import pandas as pd

__all__ = ["format_outputs"]


def format_outputs(infer_jsonl_path: str | Path, csv_path: str | Path, *, response_key: str = "response") -> Path:
    """Parse **ms‑swift** JSONL and save a simple 2‑column CSV.

    Each row becomes::
        image_path, response
    """
    infer_jsonl_path = Path(infer_jsonl_path).expanduser().resolve()
    csv_path = Path(csv_path).expanduser().resolve()

    rows: list[dict[str, str]] = []
    with open(infer_jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            img = rec.get("images", [{"path": ""}])[0]
            filename = os.path.basename(img["path"] if isinstance(img, dict) else img)
            rows.append({"image_path": filename, response_key: rec[response_key]})

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)
    return csv_path
