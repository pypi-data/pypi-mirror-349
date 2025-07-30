"""Prevents long first-run hangs by compiling Triton CUDA kernels once on CPU."""
from transformers import AutoModelForCausalLM
import torch, gc
from huggingface_hub import snapshot_download


def force_compile_once(model_id: str) -> None:
    """Download + instantiate the model on CPU just once to pre-compile kernels."""
    snapshot_download(model_id, token=None)
    try:
        print("[uniform-vlm-infer] Warm-starting model on CPU to precompile kernels…")
        _ = AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            device_map="cpu",
            low_cpu_mem_usage=True,
            torch_dtype="auto")
        del _
        gc.collect(); torch.cuda.empty_cache()
        print("[uniform-vlm-infer] ✅ Model warmed — launching Swift…")
    except Exception as e:
        print("[uniform-vlm-infer] Warm-up skipped (non-critical):", e)