from __future__ import annotations
from pathlib import Path
import subprocess, shlex, tempfile, shutil
from ..warmup import force_compile_once
from .dataset import prepare_dataset
from .format import format_outputs

_DEFAULT_ADAPTER = "DillonMurphy/nuextract-lora-final"
_DEFAULT_MODEL = "numind/NuExtract-2-4B"

# --- low‑level ---

def _swift_cmd(dataset: Path, *,
               adapter=_DEFAULT_ADAPTER,
               model=_DEFAULT_MODEL,
               model_type="internvl2_5",
               swift="swift",
               extra: dict|None=None):

    use_hf = "True"
    # Check if adapter is a local path (not HF repo)
    if adapter and Path(adapter).exists():
        use_hf = "False"

    cmd = [
        swift, "infer",
        "--model", model,
        "--model_type", model_type,
        "--adapters", adapter,
        "--infer_backend", "pt",
        "--use_hf", use_hf,
        "--temperature", "0",
        "--max_new_tokens", "1028",
        "--val_dataset", str(dataset),
        "--max_batch_size", "1"
    ]

    if extra:
        for k, v in extra.items():
            cmd.extend([f"--{k}", str(v)])
    return cmd



def run_inference(dataset_path: str|Path, **kw) -> Path:
    force_compile_once(kw.get("model", _DEFAULT_MODEL))
    
    adapter_path = kw.get("adapter")
    if adapter_path and Path(adapter_path).exists():
        kw["adapter"] = str(Path(adapter_path).resolve())

    with tempfile.TemporaryDirectory(prefix="swift_run_") as td:
        cmd = _swift_cmd(Path(dataset_path), **kw)
        subprocess.run(cmd, check=True, cwd=td)
        # 1️⃣ search inside the temp dir
        results = list(Path(td).rglob("infer_result/*.jsonl"))

        # 2️⃣ if nothing found, search next to the adapter (new behavior)
        if not results and "adapter" in kw and kw["adapter"]:
            adapter_dir = Path(kw["adapter"]).resolve()
            if adapter_dir.is_dir():
                results = list(adapter_dir.rglob("infer_result/*.jsonl"))

        # 3️⃣ still nothing?  raise an error
        if not results:
            raise FileNotFoundError("No infer_result/*.jsonl produced by swift")

        jsonl = max(results, key=lambda p: p.stat().st_mtime)
        tmp   = Path(tempfile.mkstemp(suffix=".jsonl")[1])
        shutil.copy2(jsonl, tmp)
    return tmp

# --- high‑level helper ---

def images_to_csv(img_dir: str|Path, csv_path: str|Path="predictions.csv", **kw) -> Path:
    ds = prepare_dataset(img_dir)
    res = run_inference(ds, **kw)
    out = format_outputs(res, csv_path)
    Path(res).unlink(missing_ok=True)
    return out

# --- CLI glue ---
class cli_infer:
    @staticmethod
    def add_args(p):
        p.add_argument("source")
        p.add_argument("--csv", default="predictions.csv")
        p.add_argument("--adapter", default = _DEFAULT_ADAPTER, help="LoRA adapter path or HF repo")
        p.add_argument("--model", default=_DEFAULT_MODEL)
        p.add_argument("--model-type", default="internvl2_5")

    @staticmethod
    def run(a):
        out = images_to_csv(
            a.source,
            a.csv,
            adapter=a.adapter or _DEFAULT_ADAPTER,
            model=a.model,
            model_type=a.model_type,
        )
        print("✅ CSV saved to", out)
