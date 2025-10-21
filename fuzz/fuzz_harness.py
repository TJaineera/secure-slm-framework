import sys
from detectors.prompt_injection_detector import is_malicious

try:
    import textattack
    from textattack.attack_recipes import TextFoolerJin2019
    from textattack.datasets import Dataset
except Exception:
    print("TextAttack not available. Install textattack from requirements and retry.", file=sys.stderr)
    sys.exit(2)

# sample benign prompts to try mutate
BENIGN_PROMPTS = [
    "Summarize this document for me in simple terms.",
    "What is the capital of France?",
    "Write a friendly e-mail declining an invitation.",
    "Explain recursion with a cooking analogy."
]

def run_fuzz(max_examples: int = 10):
    ds = Dataset([(p, None) for p in BENIGN_PROMPTS[:max_examples]])
    attack = TextFoolerJin2019.build()  # example recipe
    results = []
    for i, (example, _) in enumerate(ds):
        try:
            attack_result = attack.attack(example, None)
            if attack_result.perturbed_result:
                perturb = attack_result.perturbed_result.attacked_text.text
            else:
                perturb = example
        except Exception:
            perturb = example
        score, label = is_malicious(perturb)
        results.append((example, perturb, score, label))
        print(f"[{i}] score={score:.2f} label={label} orig='{example}'\n -> '{perturb}'\n")
    return results

if __name__ == "__main__":
    run_fuzz()
