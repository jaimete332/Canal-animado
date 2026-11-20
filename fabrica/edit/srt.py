"""SubRip (.srt) captions from word timings — for long-form videos, uploaded to YouTube as exact closed captions
(better than auto-captions for search and for viewers watching muted)."""
from __future__ import annotations

import re


def _ts(t: float) -> str:
    t = max(0.0, t)
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def cues(words: list[dict], max_chars: int = 42, max_lines: int = 2, max_dur: float = 6.0) -> list[tuple[float, float, str]]:
    """Groups words into readable cues: ≤ 2 lines of ≤ 42 characters, split at sentence ends."""
    out, cur = [], []

    def flush():
        if not cur:
            return
        text = " ".join(w["word"] for w in cur)
        lines, line_ = [], ""
        for w in text.split():
            if line_ and len(line_) + 1 + len(w) > max_chars:
                lines.append(line_)
                line_ = w
            else:
                line_ = (line_ + " " + w).strip()
        lines.append(line_)
        out.append((cur[0]["start"], cur[-1]["end"], "\n".join(lines)))
        cur.clear()

    for w in words:
        cur.append(w)
        text = " ".join(x["word"] for x in cur)
        end_sentence = bool(re.search(r"[.!?…]['\")]*$", w["word"]))
        too_long = len(text) > max_chars * max_lines - 12
        if end_sentence or too_long or cur[-1]["end"] - cur[0]["start"] > max_dur:
            flush()
    flush()
    # small tail so a cue stays up until the next one (max +0.6 s)
    fixed = []
    for i, (a, b, tx) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else b + 0.6
        fixed.append((a, min(nxt - 0.02, b + 0.6), tx))
    return fixed


def build_srt(words: list[dict]) -> str:
    return "\n".join(f"{i}\n{_ts(a)} --> {_ts(b)}\n{tx}\n" for i, (a, b, tx) in enumerate(cues(words), 1))
