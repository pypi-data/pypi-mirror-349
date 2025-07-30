# uniform‑vlm
A lightweight wrapper Python package for **training** and **inference** with NuExtract‑style LoRA adapters.

```bash
pip install uniform-vlm
```

### Inference
```bash
# CLI
uniform-vlm infer images/ --csv preds.csv

# Python
from uniform_vlm.infer import images_to_csv
images_to_csv("images", "preds.csv")
```

### Training (continue fine‑tuning existing adapter by default)
```bash
uniform-vlm train data/train.csv --image-col path --label-col label_json \
             --output-dir output/my_adapter
```

See the Colab walkthrough ➜ <https://colab.research.google.com/drive/1ndRcS9EMcunvrLorQdP97InvCvkEETjJ?usp=sharing>

---