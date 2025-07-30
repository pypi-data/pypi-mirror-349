from transformers import AutoModelForCausalLM
from huggingface_hub import snapshot_download
import torch, gc

def force_compile_once(model_id: str):
    snapshot_download(model_id, token=None)
    try:
        _ = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True,
                                                 device_map="cpu", low_cpu_mem_usage=True, torch_dtype="auto")
        del _; gc.collect(); torch.cuda.empty_cache()
    except Exception:
        pass
