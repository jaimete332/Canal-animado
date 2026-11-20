"""Integers → English words, for TTS (e.g. 1348 → 'thirteen forty-eight' as a year, '1,000' → 'one thousand')."""
from __future__ import annotations

import re

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def to_words(n: int) -> str:
    if n < 0:
        return "minus " + to_words(-n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    if n < 1000:
        return ONES[n // 100] + " hundred" + (" and " + to_words(n % 100) if n % 100 else "")
    for div, name in ((10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand")):
        if n >= div:
            rest = n % div
            sep = " and " if 0 < rest < 100 else " "
            return to_words(n // div) + " " + name + (sep + to_words(rest) if rest else "")
    return str(n)


def year_words(n: int) -> str:
    """1348 → 'thirteen forty-eight', 1900 → 'nineteen hundred', 2005 → 'two thousand and five'."""
    if 1010 <= n <= 1999 and n % 1000:
        hi, lo = divmod(n, 100)
        return to_words(hi) + (" hundred" if lo == 0 else (" oh " + ONES[lo] if lo < 10 else " " + to_words(lo)))
    return to_words(n)


def normalize(text: str) -> str:
    """Numbers in an English sentence → words the TTS reads naturally."""
    def dec(m):
        a, b = m.group(1).replace(",", ""), m.group(2)
        return f"{to_words(int(a))} point {' '.join(ONES[int(d)] for d in b)}"

    text = re.sub(r"(\d[\d,]*)\.(\d+)", dec, text)
    text = re.sub(r"(\d+)%", lambda m: m.group(1) + " percent", text)

    def num(m):
        raw = m.group(0)
        v = int(raw.replace(",", ""))
        if "," not in raw and 1000 <= v <= 2099 and len(raw) == 4:
            return year_words(v)
        return to_words(v)

    text = re.sub(r"\d[\d,]*\d|\d", num, text)
    return text
