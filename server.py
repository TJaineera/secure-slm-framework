import os
from fastapi import FastAPI
from pydantic import BaseModel
from models.loader import load_model
from runtime.gateway import SecureGateway, GatewayConfig

MODEL_NAME = os.environ.get("SLM_MODEL", "microsoft/phi-3-mini-4k-instruct")
DEVICE = os.environ.get("SLM_DEVICE")  # cpu/cuda/None
THRESHOLD = float(os.environ.get("SLM_INJECTION_THRESHOLD", "0.6"))

app = FastAPI(title="Secure SLM Gateway")

model, tok, gen_cfg = load_model(model_name=MODEL_NAME, device=DEVICE)
gateway = SecureGateway(model, tok, gen_cfg, GatewayConfig(inj_threshold=THRESHOLD))

class InferenceReq(BaseModel):
    prompt: str
    context: str | None = None

class InferenceResp(BaseModel):
    blocked: bool
    reason: str | None
    output: str

@app.post("/generate", response_model=InferenceResp)
def generate(req: InferenceReq):
    result = gateway.generate(req.prompt, context=req.context or "")
    return InferenceResp(**result)
