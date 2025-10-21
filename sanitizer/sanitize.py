import regex as re
from typing import Tuple

# Zero-width characters we want removed
ZERO_WIDTH = "".join([
    "\u200b", "\u200c", "\u200d", "\uFEFF", "\u2060", "\u180E"
])

HTML_TAG_RE = re.compile(r"<[^>]+>")
MULTI_WS_RE = re.compile(r"\s+")

def remove_zero_width(text: str) -> str:
    return "".join(ch for ch in text if ch not in ZERO_WIDTH)

def strip_html(text: str) -> str:
    return re.sub(HTML_TAG_RE, " ", text)

def normalize_whitespace(text: str) -> str:
    return re.sub(MULTI_WS_RE, " ", text).strip()

def sanitize(text: str) -> str:
    """
    Basic sanitization pipeline:
    - remove zero-width characters
    - strip HTML tags
    - normalize whitespace
    - remove other control characters (keep newlines)
    """
    if text is None:
        return ""
    t = str(text)
    t = remove_zero_width(t)
    t = strip_html(t)
    t = normalize_whitespace(t)
    # remove other control chars except common whitespace/newline
    t = "".join(ch for ch in t if (ch == "\n" or ord(ch) >= 32))
    return t

def quick_stats(text: str) -> Tuple[int,int]:
    """Return (num_chars, num_zero_width_found)"""
    z = sum(1 for ch in text if ch in ZERO_WIDTH)
    return len(text), z
