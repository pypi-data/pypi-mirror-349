from __future__ import annotations
import argparse, sys
from .infer.run import cli_infer
from .train.run import cli_train


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser("uniform-vlm")
    sub = p.add_subparsers(dest="command", required=True)

    infer_p = sub.add_parser("infer", help="Run inference")
    cli_infer.add_args(infer_p)

    train_p = sub.add_parser("train", help="Train / fine‑tune LoRA")
    cli_train.add_args(train_p)
    return p


def main(argv: list[str] | None = None):
    args = build_parser().parse_args(argv)
    if args.command == "infer":
        cli_infer.run(args)
    else:
        cli_train.run(args)
