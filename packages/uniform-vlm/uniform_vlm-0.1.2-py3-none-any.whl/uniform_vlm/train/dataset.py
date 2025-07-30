from __future__ import annotations
import csv, json, tempfile
from pathlib import Path

_SYSTEM = "You are NuExtract, a vision-language model that outputs JSON following the provided template."
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

def csv_to_jsonl(csv_path: str | Path,
                 image_col: str = "image",
                 label_col: str = "label") -> Path:
    """
    Convert a CSV into ms-swift training JSONL.

    Each CSV row must have:
      • image_col  – path to image
      • label_col  – JSON string containing the ground-truth structured output
    """
    csv_path = Path(csv_path).expanduser().resolve()
    tf = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)

    with open(csv_path, newline="", encoding="utf-8") as f, tf as out:
        reader = csv.DictReader(f)
        for row in reader:
            record = {
                "messages": [
                    {"role": "system",    "content": _SYSTEM},
                    {"role": "user",      "content": _USER_TEMPLATE},
                    {"role": "assistant", "content": row[label_col]},
                ],
                "images": [row[image_col]],
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    return Path(tf.name)