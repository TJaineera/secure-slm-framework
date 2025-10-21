import sanitizer.sanitize as s

def test_remove_zero_width():
    txt = "Hello\u200bWorld"
    out = s.remove_zero_width(txt)
    assert "\u200b" not in out
    assert out == "HelloWorld"

def test_strip_html_and_whitespace():
    txt = "   <b>Hello</b>\n<p>World</p>   "
    out = s.sanitize(txt)
    assert "<" not in out and ">" not in out
    assert "Hello" in out and "World" in out
    # normalized whitespace: single spaces, no leading/trailing
    assert out == "Hello World" or out == "Hello World"

def test_quick_stats_counts_zero_width():
    txt = "a\u200bb\u200c"
    length, z = s.quick_stats(txt)
    assert length == len(txt)
    assert z == 2
