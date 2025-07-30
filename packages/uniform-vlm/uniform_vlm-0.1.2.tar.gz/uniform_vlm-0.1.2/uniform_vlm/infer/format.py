from __future__ import annotations
import json, os
from pathlib import Path
import pandas as pd

__all__ = ["format_outputs"]

def format_outputs(infer_jsonl: str | Path, csv_path: str | Path) -> Path:
    rows = []
    with open(infer_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            img_rec = rec.get("images", [{"path": ""}])[0]
            image_path = img_rec["path"] if isinstance(img_rec, dict) else img_rec
            rows.append({"image_path": image_path, "response": rec["response"]})
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    return Path(csv_path)