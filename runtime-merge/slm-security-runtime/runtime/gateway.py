from typing import Dict, Any
from dataclasses import dataclass
import torch

from sanitizer.sanitize import sanitize
from detectors.prompt_injection_detector import is_malicious

SYSTEM_PROMPT = (
    "You are a helpful, security-aware assistant. "
    "Follow safety policies. If user asks for disallowed or sensitive content, refuse."
)

@dataclass
class GatewayConfig:
    inj_threshold: float = 0.6
    block_message: str = "Request blocked by security policy."

class SecureGateway:
    def __init__(self, model, tokenizer, gen_cfg, cfg: GatewayConfig = GatewayConfig()):
        self.model = model
        self.tok = tokenizer
        self.gen_cfg = gen_cfg
        self.cfg = cfg

    def compose_prompt(self, user_input: str, context: str = "") -> str:
        parts = [f"<|system|>\n{SYSTEM_PROMPT}"]
        if context:
            parts.append(f"<|context|>\n{context}")
        parts.append(f"<|user|>\n{user_input}\n<|assistant|>\n")
        return "\n".join(parts)

    def generate(self, raw_user_input: str, context: str = "") -> Dict[str, Any]:
        clean_input = sanitize(raw_user_input)
        score, label = is_malicious(clean_input, threshold=self.cfg.inj_threshold)
        if label == "malicious":
            return {
                "blocked": True,
                "reason": f"prompt-injection score={score:.2f}",
                "output": self.cfg.block_message
            }
        prompt = self.compose_prompt(clean_input, context)
        inputs = self.tok(prompt, return_tensors="pt")
        if hasattr(self.model, "device") and self.model.device.type == "cuda":
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        with torch.no_grad():
            out = self.model.generate(**inputs, **self.gen_cfg.to_dict())
        text = self.tok.decode(out[0], skip_special_tokens=True)
        return {"blocked": False, "reason": None, "output": text}
