"""Run ms‑swift inside a temporary directory and return the path to a stable
JSONL copy so the caller can safely read/keep/delete it."""
from __future__ import annotations

import subprocess
import shlex
import tempfile
import shutil
from pathlib import Path
from typing import Any, Mapping
from .warmup import force_compile_once

_DEFAULT_ADAPTER = "DillonMurphy/nuextract-lora-final"
_DEFAULT_MODEL = "numind/NuExtract-2-4B"
_DEFAULT_MODEL_TYPE = "internvl2_5"

__all__ = ["run_inference"]


def _build_cmd(
    dataset_path: Path,
    *,
    adapter_repo: str = _DEFAULT_ADAPTER,
    model: str = _DEFAULT_MODEL,
    model_type: str = _DEFAULT_MODEL_TYPE,
    swift_executable: str = "swift",
    extra_swift_args: Mapping[str, Any] | None = None,
) -> list[str]:
    cmd = [
        swift_executable,
        "infer",
        "--model", model,
        "--model_type", model_type,
        "--adapters", adapter_repo,
        "--infer_backend", "pt",
        "--use_hf", "True",
        "--temperature", "0",
        "--max_new_tokens", "1028",
        "--val_dataset", str(dataset_path),
        "--max_batch_size", "1",
    ]
    if extra_swift_args:
        for k, v in extra_swift_args.items():
            flag = f"-{k}" if len(k) == 1 else f"--{k}"
            cmd.extend([flag, str(v)])
    return cmd


def run_inference(
    dataset_path: str | Path,
    *,
    adapter_repo: str = _DEFAULT_ADAPTER,
    model: str = _DEFAULT_MODEL,
    model_type: str = _DEFAULT_MODEL_TYPE,
    swift_executable: str = "swift",
    extra_swift_args: Mapping[str, Any] | None = None,
    verbose: bool = True,
) -> Path:
    """Run Swift in a tmp dir and return **a copy** of the produced JSONL."""
    dataset_path = Path(dataset_path).expanduser().resolve()
    force_compile_once(model)

    with tempfile.TemporaryDirectory(prefix="swift_run_") as td:
        tmpdir = Path(td)
        cmd = _build_cmd(
            dataset_path=dataset_path,
            adapter_repo=adapter_repo,
            model=model,
            model_type=model_type,
            swift_executable=swift_executable,
            extra_swift_args=extra_swift_args,
        )
        if verbose:
            print("[uniform-vlm-infer] running in", tmpdir, "\n", shlex.join(cmd))

        subprocess.run(cmd, check=True, cwd=tmpdir)

        jsonls = sorted(
            tmpdir.rglob("infer_result/*.jsonl"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not jsonls:
            raise FileNotFoundError("Swift produced no infer_result/*.jsonl in " + str(tmpdir))

        raw_jsonl = jsonls[0]
        # copy to a stable temp file outside the with‑block
        stable_jsonl = Path(tempfile.mkstemp(prefix="swift_out_", suffix=".jsonl")[1])
        shutil.copy2(raw_jsonl, stable_jsonl)

    # tmpdir is gone here, but stable_jsonl persists
    return stable_jsonl