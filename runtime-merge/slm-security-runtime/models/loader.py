from typing import Optional, Dict, Any
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

DEFAULT_MODEL = "microsoft/phi-3-mini-4k-instruct"  # easy start

def load_model(
    model_name: str = DEFAULT_MODEL,
    device: Optional[str] = None,
    dtype: Optional[torch.dtype] = None,
    trust_remote_code: bool = False,
    **kwargs: Dict[str, Any]
):
    """
    Loads a Causal LM + tokenizer for inference.
    Defaults to CPU-friendly settings.
    Set device='cuda' and dtype=torch.float16 if you have a GPU.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if dtype is None:
        dtype = torch.float16 if device == "cuda" else torch.float32

    tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=trust_remote_code)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=dtype,
        device_map="auto" if device == "cuda" else None,
        low_cpu_mem_usage=True,
        trust_remote_code=trust_remote_code
    )
    if device == "cpu":
        model = model.to(device)

    gen_cfg = GenerationConfig(
        max_new_tokens=256,
        temperature=0.4,
        top_p=0.9,
        do_sample=True
    )
    return model, tok, gen_cfg
