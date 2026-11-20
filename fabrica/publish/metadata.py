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
    if m.get("description"):
        desc = m["description"]
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


def _mmss(t: float) -> str:
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def chapters(story: Story, timeline: list[dict] | None) -> list[dict]:
    """YouTube chapters from scenes marked with `chapter`: first at 0:00, each ≥ 10 s (YouTube's rules)."""
    if not timeline:
        return []
    out = []
    for it, sc in zip(timeline, story.scenes):
        if sc.chapter is not None or it["index"] == 0:
            title = sc.chapter or story.metadata.get("intro_chapter", "Intro")
            start = 0.0 if not out else it["start"]
            if out and start - out[-1]["start"] < 10:
                continue
            out.append({"start": round(start, 2), "time": _mmss(start), "title": title})
    return out if len(out) >= 3 else []


def _template_en(story: Story, duration: float, timeline: list[dict] | None) -> dict:
    """English long-form metadata: hook paragraph, chapters, facts with sources, disclaimer, hashtags."""
    cfg = load_config()["channel"]
    m = story.metadata
    title = m.get("title") or story.title
    if len(title) > 70:
        title = title[:67].rstrip() + "…"
    chs = chapters(story, timeline)
    facts = [c for s in story.scenes for c in s.claims if c.kind == "fact"]
    sources = list(dict.fromkeys(x.strip() for c in facts for x in re.split(r";", c.source) if x.strip()))
    tags_h = list(dict.fromkeys(m.get("hashtags", []) + cfg["default_hashtags"]))
    parts = [m.get("description_intro", story.title)]
    if chs:
        parts.append("CHAPTERS\n" + "\n".join(f"{c['time']} {c['title']}" for c in chs))
    if m.get("description_facts", True) and facts:
        parts.append("REAL HISTORY IN THIS VIDEO\n" + "\n".join(f"• {c.text}" for c in facts[:12]))
    parts.append(m.get("disclaimer", "Stan's story is a dramatization; the historical facts are real, simplified "
                                     "for the video, and sourced below. Numbers are estimates — historians argue "
                                     "about the details, and that's part of the fun."))
    if sources:
        parts.append("SOURCES & FURTHER READING\n" + "\n".join(f"• {x}" for x in sources))
    parts.append(m.get("cta", f"💬 {story.question}\n🔔 Subscribe to {cfg['name']} for a new stickman "
                              "what-if every week."))
    parts.append("Animation, voice and music made by the channel. Narration uses a synthetic voice.")
    parts.append(" ".join(tags_h[:3]))   # YouTube shows the first 3 hashtags above the title
    desc = "\n\n".join(parts)
    if m.get("description"):
        desc = m["description"]
    tags = m.get("tags") or [w.strip("#") for w in tags_h]
    return {
        "title": title, "description": desc[:5000], "hashtags": tags_h[:3], "tags": tags,
        "pinned_comment": m.get("pinned_comment") or story.question,
        "thumbnail_text": m.get("thumbnail_text", story.title.upper()),
        "category_id": load_config()["youtube"]["category_id"], "language": "en",
        "duration_s": round(duration, 2), "chapters": chs, "made_for_kids": False,
        "contains_synthetic_media": True,
    }


def build_metadata(story: Story, duration: float, timeline: list[dict] | None = None) -> dict:
    from ..core.config import lang
    if lang() == "en":
        return _template_en(story, duration, timeline)
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
    if load_config()["channel"].get("engine") == "stick":
        from ..stick.thumbnail import stick_thumbnail
        return stick_thumbnail(pipe, meta)
    if pipe.story.metadata.get("custom_thumbnail"):
        return  # miniatura diseñada a mano (scripts/thumbnail_*.py)
    if pipe.story.metadata.get("thumbnail"):
        return designed_thumbnail(pipe, pipe.story.metadata["thumbnail"])
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


def designed_thumbnail(pipe, spec: dict) -> None:
    """Miniatura diseñada a partir de una escena:
    spec = {"scene": "s07", "t": 0.6, "lines": ["¿Y SI...", "..."], "badge": "6.371 km",
            "character": {...overrides...}, "props": [...extra...], "zoom": 1.1, "focus": [0.5, 0.6]}
    Genera thumbnail.png (1080x1920) y thumbnail_16x9.png (1280x720)."""
    import cairo

    from ..visuals.draw import OUT, PAL, fill_stroke, rrect, saved, text
    from ..visuals.scene import SceneRenderer
    items = {i["id"]: i for i in pipe.scene_items()}
    item = json.loads(json.dumps(items[spec["scene"]]))
    item["trans_in"] = item["trans_out"] = "cut"
    vis = item["scene"]["visual"]
    vis["overlays"] = []
    if spec.get("character") and vis.get("character"):
        vis["character"].update(spec["character"])
        for k in ("enter", "path", "actions", "expressions"):
            if k not in spec["character"]:
                vis["character"].pop(k, None)
    vis["props"] = [p for p in vis.get("props", []) if p.get("type") not in spec.get("drop_props", [])]
    vis["props"] += spec.get("props", [])
    vis["camera"] = {"move": "static", "zoom_from": spec.get("zoom", 1.0), "focus": spec.get("focus", [0.5, 0.5])}
    if spec.get("zoom"):
        vis["camera"] = {"move": "push_in", "zoom_from": spec["zoom"], "zoom_to": spec["zoom"],
                         "focus": spec.get("focus", [0.5, 0.5])}
    r = SceneRenderer(item, pipe.fps)
    base = r.frame(int(item["frames"] * spec.get("t", 0.6)))
    colors = spec.get("colors", ["white", PAL["yellow"], PAL["yellow"]])
    lines = spec["lines"]

    def badge(ctx, x, y, size, rot=0.1, left=False):
        if not spec.get("badge"):
            return
        ctx.select_font_face("Lilita One")
        ctx.set_font_size(size)
        w = ctx.text_extents(spec["badge"]).width
        if left:
            x = x + w / 2 + 40
        with saved(ctx):
            ctx.translate(x, y)
            ctx.rotate(rot)
            rrect(ctx, -w / 2 - 40, -size * 0.8, w + 80, size * 1.6, size * 0.5)
            fill_stroke(ctx, spec.get("badge_color", PAL["red"]), OUT * 1.2)
            text(ctx, spec["badge"], 0, 2, size, outline=7, shadow_off=0)

    # vertical
    v = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920)
    c = cairo.Context(v)
    c.set_source_surface(base)
    c.paint()
    from ..visuals.draw import linear_grad
    c.rectangle(0, 0, 1080, 700)
    c.set_source(linear_grad(c, 0, 0, 0, 700, [(0, (0, 0, 0), 0.55), (1, (0, 0, 0), 0)]))
    c.fill()
    size = spec.get("size", 150)
    for i, ln in enumerate(lines):
        with saved(c):
            c.translate(540, spec.get("y", 250) + i * size * 1.05)
            c.rotate(-0.03)
            text(c, ln, 0, 0, size, color=colors[i % len(colors)], outline=16, max_w=1010)
    bx, by = spec.get("badge_pos", [760, 1350])
    badge(c, bx, by, 82)
    v.write_to_png(str(pipe.paths.thumbnail))
    # horizontal 16:9: escena a la derecha, texto a la izquierda
    h = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720)
    c = cairo.Context(h)
    c.set_source_rgb(0.08, 0.07, 0.16)
    c.paint()
    with saved(c):
        sc = spec.get("h_scale", 0.95)
        c.translate(spec.get("h_shift", 560), 0)
        c.scale(sc, sc)
        c.translate(-540, -(1920 * spec.get("crop_y", 0.45)) + 720 / sc / 2)
        c.set_source_surface(base)
        c.paint()
    c.rectangle(0, 0, 1280, 720)
    c.set_source(linear_grad(c, 0, 0, 1280, 0, [(0, (0.08, 0.07, 0.16), 1), (0.38, (0.08, 0.07, 0.16), 0.85),
                                                (0.62, (0, 0, 0), 0)]))
    c.fill()
    hs = 86
    for i, ln in enumerate(lines):
        text(c, ln, 40, 220 + i * hs * 1.08, hs, color=colors[i % len(colors)], outline=11, align="left", max_w=700)
    badge(c, 40, 220 + len(lines) * hs * 1.08 + 40, 60, rot=-0.04, left=True)
    h.write_to_png(str(pipe.paths.root / "thumbnail_16x9.png"))
