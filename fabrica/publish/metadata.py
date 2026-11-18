"""Título, descripción, hashtags, comentario fijado y miniatura."""
from __future__ import annotations

import json
import re

from ..core.config import load_config
from ..core.log import get_logger
from ..llm.client import NoLLMAvailable, complete
from ..script.schema import Story

log = get_logger("metadata")


def _template(story: Story, duration: float) -> dict:
    cfg = load_config()["channel"]
    m = story.metadata
    title = m.get("title") or story.title
    if len(title) > 70:
        title = title[:67].rstrip() + "…"
    facts = [c for s in story.scenes for c in s.claims if c.kind == "fact"]
    fact_lines = "\n".join(f"• {c.text}" for c in facts[:10])
    sources = list(dict.fromkeys(x.strip() for c in facts for x in re.split(r"[;/]", c.source) if x.strip()))
    tags = list(dict.fromkeys(m.get("hashtags", []) + cfg["default_hashtags"]))[:8]
    desc = (f"{m.get('description_intro', story.title)}\n\n"
            f"Datos reales que aparecen en el vídeo:\n{fact_lines}\n\n"
            "⚠️ La historia del protagonista es ficción (nadie sobreviviría); los datos científicos son reales "
            "y aproximados.\n\n"
            f"Fuentes: {'; '.join(sources)}\n\n"
            "Música y efectos: originales, generados por el canal.\n\n" + " ".join(tags))
    return {
        "title": title,
        "description": desc,
        "hashtags": tags,
        "tags": m.get("tags", [w.strip("#") for w in tags]),
        "pinned_comment": m.get("pinned_comment") or (story.question + " 👇"),
        "thumbnail_text": m.get("thumbnail_text", story.title.upper()),
        "category_id": load_config()["youtube"]["category_id"],
        "language": "es",
        "duration_s": round(duration, 2),
        "made_for_kids": False,
        "contains_synthetic_media": True,
    }


def build_metadata(story: Story, duration: float) -> dict:
    meta = _template(story, duration)
    if story.metadata.get("title"):
        return meta
    try:
        alt = complete(
            "Eres experto en YouTube Shorts en español de España. Respondes solo JSON.",
            "Propón para este Short: title (<=60 caracteres, curiosidad sin clickbait engañoso), "
            "pinned_comment (pregunta que invite a comentar), hashtags (5, con #). "
            f"Guion: {story.full_text}", temperature=0.7)
        meta.update({k: v for k, v in alt.items() if k in ("title", "pinned_comment", "hashtags") and v})
    except NoLLMAvailable:
        pass
    except Exception as e:
        log.warning("Metadatos LLM fallaron: %s", e)
    return meta


def make_thumbnail(pipe, meta: dict) -> None:
    """Fotograma promocional: escena marcada (o clímax) + texto grande."""
    from ..visuals.scene import SceneRenderer
    items = pipe.scene_items()
    want = pipe.story.metadata.get("thumbnail_scene")
    item = next((i for i in items if i["id"] == want), None) or \
        next((i for i, s in zip(items, pipe.story.scenes) if s.beat == "climax"), items[0])
    item = json.loads(json.dumps(item))
    item["trans_in"] = item["trans_out"] = "cut"
    words = meta["thumbnail_text"].split()
    half = (len(words) + 1) // 2
    lines = [" ".join(words[:half]), " ".join(words[half:])] if len(words) > 3 else [meta["thumbnail_text"]]
    item["scene"]["visual"]["overlays"] = [
        {"type": "vignette", "alpha": 0.45},
        {"type": "title", "lines": lines, "y": 300, "size": 130, "at": -5}]
    r = SceneRenderer(item, pipe.fps)
    r.frame(int(item["frames"] * 0.6)).write_to_png(str(pipe.paths.thumbnail))
