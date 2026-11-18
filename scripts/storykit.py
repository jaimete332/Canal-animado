"""Utilidades para escribir guiones a mano en Python (se exportan a stories/<slug>.json)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUIT = {"outfit": "suit", "helmet": "dome"}


class Story:
    def __init__(self):
        self.scenes = []

    def sc(self, id, beat, narration, visual, claims=(), sfx=(), transition="whip", emphasis=(), pause=0.06):
        self.scenes.append({"id": id, "beat": beat, "narration": narration, "visual": visual, "claims": list(claims),
                            "sfx": list(sfx), "transition": transition, "emphasis": list(emphasis),
                            "pause_after": pause})

    def save(self, slug, title, idea, category, question, metadata, mood="adventure"):
        d = {"title": title, "idea": idea, "slug": slug, "category": category, "question": question,
             "music_mood": mood, "scenes": self.scenes, "metadata": metadata}
        out = ROOT / "stories" / f"{slug}.json"
        out.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
        words = sum(len(s["narration"].split()) for s in self.scenes)
        for s in self.scenes:  # comprueba índices de palabra
            n = len(s["narration"].split())
            for coll in (s["visual"].get("props", []), s["visual"].get("overlays", []), s["sfx"]):
                for x in coll:
                    if x.get("at_word") is not None and x["at_word"] >= n:
                        raise ValueError(f"{s['id']}: at_word {x['at_word']} fuera de rango ({n} palabras)")
        print(out, len(self.scenes), "escenas,", words, "palabras")


def F(text, source, kind="fact"):
    return {"text": text, "kind": kind, "source": source}
