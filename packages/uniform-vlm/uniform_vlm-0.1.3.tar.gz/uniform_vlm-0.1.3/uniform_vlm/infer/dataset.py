from __future__ import annotations
import json, tempfile
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

__all__ = ["prepare_dataset"]

def prepare_dataset(img_dir: str | Path) -> Path:
    img_dir = Path(img_dir).expanduser().resolve()
    tf = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)
    with tf as f:
        for p in sorted(img_dir.glob("*.*")):
            json.dump({"messages":[{"role":"system","content":_SYSTEM},{"role":"user","content":_USER_TEMPLATE}],"images":[str(p)]},f)
            f.write("\n")
    return Path(tf.name)