from __future__ import annotations
import subprocess, shlex, tempfile, pathlib, json
from .dataset import csv_to_jsonl

_DEFAULT_MODEL      = "numind/NuExtract-2-4B"
_DEFAULT_MODEL_TYPE = "internvl2_5"

# ---------- flexible swift command builder ----------
# uniform_vlm/train/run.py
def _swift_sft_cmd(
    data: pathlib.Path,
    *,
    adapter: str | None,
    output_dir: str,
    resume: str | None,
    freeze_base: bool,
    model: str = _DEFAULT_MODEL,
    model_type: str = _DEFAULT_MODEL_TYPE,
    extra: dict[str, str] | None = None,
) -> list[str]:
    """Return a swift sft command where `extra` cleanly overrides defaults."""
    # ---- defaults in a dict ----
    flags = {
        "model": model,
        "model_type": model_type,
        "use_hf": "",
        "train_type": "lora",
        "tuner_backend": "peft",
        "dataset": str(data),
        "output_dir": output_dir,
        "per_device_train_batch_size": "1",
        "gradient_accumulation_steps": "4",
        "learning_rate": "5e-5",
        "num_train_epochs": "20",
        "fp16": "true",
        "gradient_checkpointing": "true",
        "logging_steps": "10",
        "save_steps": "50",
        "save_total_limit": "2",
    }

    # merge/override with extra
    if extra:
        flags.update(extra)

    # adapter / resume handled separately
    cmd = ["swift", "sft"]
    for k, v in flags.items():
        flag = f"--{k}"
        cmd += [flag] if v == "" else [flag, str(v)]

    if adapter:
        cmd += ["--adapters", adapter]
        if freeze_base:
            cmd += ["--unfreeze_lora", "false"]

    if resume:
        cmd += ["--resume_from_checkpoint", resume]

    return cmd
# ------------------------------------------------------

def train_lora(
    csv_path: str | pathlib.Path,
    *,
    image_col="image",
    label_col="label",
    adapter=None,
    output_dir="output/lora",
    resume=None,
    freeze_base=False,
    extra: dict[str, str] | None = None,  
):
    data = csv_to_jsonl(csv_path, image_col, label_col)
    cmd  = _swift_sft_cmd(
        data,
        adapter=adapter,
        output_dir=output_dir,
        resume=resume,
        freeze_base=freeze_base,
        extra=extra,                       
    )
    subprocess.run(cmd, check=True)

class cli_train:
    @staticmethod
    def add_args(p):
        p.add_argument("csv")
        p.add_argument("--image-col", default="image")
        p.add_argument("--label-col", default="label")
        p.add_argument("--output-dir", default="output/lora")
        p.add_argument("--resume")
        p.add_argument("--base-adapter", dest="adapter")
        p.add_argument("--freeze-base", action="store_true")
        # catch-all for arbitrary swift flags:  --arg num_train_epochs=10
        p.add_argument(
            "--arg",
            action="append",
            default=[],
            metavar="KEY=VALUE",
            help="Extra swift sft argument (e.g., --arg num_train_epochs=10)",
        )

    @staticmethod
    def run(a):
        # convert --arg key=value pairs into a dict
        extra = {}
        for kv in a.arg:
            k, v = kv.split("=", 1)
            extra[k] = v
        train_lora(
            a.csv,
            image_col=a.image_col,
            label_col=a.label_col,
            adapter=a.adapter,
            output_dir=a.output_dir,
            resume=a.resume,
            freeze_base=a.freeze_base,
            extra=extra,
        )
        print("✅ Training finished; checkpoints in", a.output_dir)
