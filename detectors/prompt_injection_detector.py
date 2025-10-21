import re
from typing import Tuple

# Simple patterns commonly used in prompt injection / jailbreaks
INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"disregard (all )?previous instructions",
    r"forget (all )?previous instructions",
    r"please execute the following",
    r"respond only with",
    r"do not mention",
    r"system prompt",
    r"assistant should",
    r"translate the following.*instruction",
    r"follow these steps exactly",
    r"print the (password|secret|key|flag)",
    r"show me the hidden"
]

COMPILED_PATTERNS = [re.compile(p, flags=re.IGNORECASE) for p in INJECTION_PATTERNS]

def score_by_regex(text: str) -> float:
    """
    Returns a score between 0 and 1 based on heuristics:
    - more matches -> higher score
    - replace with model.predict_proba later if desired
    """
    if not text:
        return 0.0
    matches = 0
    for rx in COMPILED_PATTERNS:
        if rx.search(text):
            matches += 1
    # simple scaling: each hit adds weight, saturate at 1.0
    score = min(1.0, matches / 3.0)
    return score

def is_malicious(text: str, threshold: float = 0.6) -> Tuple[float, str]:
    """
    Returns (score, label) where label is 'malicious'/'suspicious'/'clean'
    threshold: score >= threshold -> malicious
    """
    s = score_by_regex(text)
    if s >= threshold:
        return s, "malicious"
    if s >= threshold * 0.6:
        return s, "suspicious"
    return s, "clean"
