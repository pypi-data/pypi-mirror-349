from __future__ import annotations

import argparse
from pathlib import Path
from .dataset import prepare_dataset
from .infer import run_inference
from .format import format_outputs


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run uniform LoRA VLM inference and format to CSV")
    p.add_argument("source", type=Path, help="Image directory *or* JSONL dataset")
    p.add_argument("--csv", dest="csv", type=Path, default=Path("predictions.csv"), help="Output CSV path")
    p.add_argument("--adapter", default="DillonMurphy/nuextract-lora-final", help="HF repo of LoRA adapter")
    p.add_argument("--model", default="numind/NuExtract-2-4B", help="Base VLM (HF id)")
    p.add_argument("--model-type", default="internvl2_5", help="Model type for swift")
    return p


def main(argv: list[str] | None = None) -> None:
    args = _build_parser().parse_args(argv)

    if args.source.is_dir():
        jsonl = prepare_dataset(args.source)
    else:
        jsonl = args.source

    result_jsonl = run_inference(
        dataset_path=jsonl,
        adapter_repo=args.adapter,
        model=args.model,
        model_type=args.model_type,
    )
    csv_path = format_outputs(result_jsonl, args.csv)
    print(f"\n✅ Saved tidy results to {csv_path}\n")