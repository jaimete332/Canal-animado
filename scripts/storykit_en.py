"""Helpers to write long-form English stickman scripts in Python (exported to stories_en/<slug>.json).

    from storykit_en import Story, F, cast
    st = Story()
    st.chapter("The Deal")                     # next scene opens a YouTube chapter
    st.sc("intro01", "hook", "Meet Stan.", {"background": {...}, "cast": [cast("stan", action="wave")]})
    st.save("slug", title=..., idea=..., question=..., metadata={...})
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUND = 0.84


def cast(id, preset=None, x=0.5, y=GROUND, scale=1.4, **kw):
    """One stickman in a scene. `preset` defaults to `id` (stan, peasant, lord, priest, knight...)."""
    d = {"id": id, "x": x, "y": y, "scale": scale, **kw}
    if preset:
        d["preset"] = preset
    return d


def F(text, source, kind="fact"):
    return {"text": text, "kind": kind, "source": source}


class Story:
    def __init__(self):
        self.scenes = []
        self._chapter = None
        self._n = 0

    def chapter(self, title):
        self._chapter = title

    def sc(self, id, beat, narration, visual, claims=(), sfx=(), transition="cut", emphasis=(), pause=0.25):
        self._n += 1
        sid = id or f"s{self._n:03d}"
        d = {"id": sid, "beat": beat, "narration": narration, "visual": visual, "claims": list(claims),
             "sfx": list(sfx), "transition": transition, "emphasis": list(emphasis), "pause_after": pause}
        if self._chapter:
            d["chapter"] = self._chapter
            self._chapter = None
        self.scenes.append(d)
        return d

    def save(self, slug, title, idea, question, metadata, category="history", mood="medieval"):
        d = {"title": title, "idea": idea, "slug": slug, "category": category, "question": question,
             "music_mood": mood, "scenes": self.scenes, "metadata": metadata}
        ids = [s["id"] for s in self.scenes]
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            raise ValueError(f"duplicated scene ids: {dup}")
        for s in self.scenes:   # word indices must exist
            n = len(s["narration"].split())
            v = s["visual"]
            items = list(v.get("props", [])) + list(v.get("overlays", [])) + list(s["sfx"])
            for c in v.get("cast", []):
                items += list(c.get("say", []))
                for k in ("actions", "expressions"):
                    for tt, _ in c.get(k, []):
                        if isinstance(tt, str) and tt.startswith("w") and int(tt[1:]) >= n:
                            raise ValueError(f"{s['id']}: {k} word {tt} out of range ({n} words)")
            for x in items:
                for key in ("at_word", "until_word"):
                    if x.get(key) is not None and x[key] >= n:
                        raise ValueError(f"{s['id']}: {key} {x[key]} out of range ({n} words)")
        out = ROOT / "stories_en" / f"{slug}.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
        words = sum(len(s["narration"].split()) for s in self.scenes)
        chapters = [s["chapter"] for s in self.scenes if s.get("chapter")]
        print(f"{out}: {len(self.scenes)} scenes, {words} words (~{words / 155:.1f} min), "
              f"{len(chapters)} chapters")
        return out
