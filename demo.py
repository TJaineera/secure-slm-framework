import argparse
from models.loader import load_model
from runtime.gateway import SecureGateway, GatewayConfig

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="microsoft/phi-3-mini-4k-instruct")
    ap.add_argument("--device", default=None)  # 'cpu' or 'cuda'
    ap.add_argument("--threshold", type=float, default=0.6)
    args = ap.parse_args()

    model, tok, gen_cfg = load_model(model_name=args.model, device=args.device)
    gate = SecureGateway(model, tok, gen_cfg, GatewayConfig(inj_threshold=args.threshold))

    print("Type a prompt (or 'exit'): ")
    while True:
        try:
            user = input("> ")
        except (EOFError, KeyboardInterrupt):
            break
        if user.strip().lower() in {"exit", "quit"}:
            break
        result = gate.generate(user)
        if result["blocked"]:
            print(f"[BLOCKED] {result['reason']}\n{result['output']}\n")
        else:
            print(result["output"], "\n")

if __name__ == "__main__":
    main()
