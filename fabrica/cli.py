"""Línea de comandos de la fábrica.

  python -m fabrica auto                      # todo automático: idea → vídeo terminado
  python -m fabrica auto --idea "¿Qué pasaría si vivieras 100 días en Marte?"
  python -m fabrica make stories/centro-de-la-tierra.json   # desde un guion existente
  python -m fabrica regen centro-de-la-tierra s07           # rehace solo una escena (y el montaje)
  python -m fabrica still stories/x.json s07 1.5             # PNG de una escena en t=1.5s (previsualizar)
  python -m fabrica ideas [--n 10]                           # ideas puntuadas y sin repetir
  python -m fabrica list                                     # registro de vídeos
  python -m fabrica approve centro-de-la-tierra              # tu aprobación (obligatoria para subir)
  python -m fabrica upload centro-de-la-tierra               # sube a YouTube (privado por defecto)
  python -m fabrica metrics                                  # descarga métricas de YouTube
  python -m fabrica insights                                 # aprendizajes para próximos guiones
  python -m fabrica doctor                                   # comprueba dependencias, modelos y claves
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core.config import ROOT, load_config
from .core.log import get_logger, setup_logging

log = get_logger("cli")


def cmd_make(a):
    from .pipeline import Pipeline, load_story
    story = load_story(Path(a.story))
    res = Pipeline(story, workers=a.workers, force=set(a.force or [])).run(qa=not a.no_qa)
    _summary(res)


def cmd_auto(a):
    from .ideas.bank import pick_idea
    from .pipeline import Pipeline
    from .script.writer import write_story
    idea = a.idea or pick_idea()
    log.info("Idea elegida: %s", idea)
    story = write_story(idea)
    path = load_config().path("paths.stories") / f"{story.slug}.json"
    path.write_text(story.model_dump_json(indent=2), encoding="utf-8")
    res = Pipeline(story, workers=a.workers).run()
    _summary(res)


def cmd_regen(a):
    from .pipeline import Pipeline, load_story
    p = load_config().path("paths.output") / a.slug / "script.json"
    src = Path(a.story) if a.story else p
    story = load_story(src)
    res = Pipeline(story, workers=a.workers, force=set(a.scenes)).run(qa=not a.no_qa)
    _summary(res)


def cmd_still(a):
    from .pipeline import Pipeline, load_story
    from .visuals.fonts import ensure_fonts
    from .visuals.scene import render_still
    ensure_fonts()
    story = load_story(Path(a.story))
    pipe = Pipeline(story)
    pipe.narrate()
    items = {i["id"]: i for i in pipe.scene_items()}
    ids = [a.scene] if a.scene != "all" else list(items)
    for sid in ids:
        out = pipe.paths.qa / f"still_{sid}.png"
        t = a.t if a.t is not None else items[sid]["dur"] * 0.6
        render_still(items[sid], t, out)
        print(out)


def cmd_ideas(a):
    from .ideas.bank import ranked_ideas
    for score, idea in ranked_ideas(a.n):
        print(f"{score:5.1f}  {idea}")


def cmd_list(a):
    from .core.registry import Registry
    for r in Registry().videos():
        print(f"{r['slug']:40s} {r['status']:10s} {r['duration_s'] or 0:5.1f}s  {r['cost_usd'] or 0:.3f}$  "
              f"{r['youtube_id'] or '-'}  {r['title']}")


def cmd_approve(a):
    from .core.registry import Registry
    from .publish.youtube import approve
    approve(a.slug)
    Registry().upsert_video(a.slug, status="approved")
    print(f"Aprobado: {a.slug}")


def cmd_upload(a):
    from .publish.youtube import upload
    vid = upload(a.slug, privacy=a.privacy)
    print(f"Subido: https://youtube.com/shorts/{vid}")


def cmd_metrics(a):
    from .analytics.metrics import fetch_all
    fetch_all()


def cmd_insights(a):
    from .analytics.metrics import insights
    print(json.dumps(insights(), indent=2, ensure_ascii=False))


def cmd_doctor(a):
    import shutil
    from .core.config import env
    cfg = load_config()
    ok = lambda b: "✅" if b else "❌"  # noqa: E731
    print(ok(shutil.which("ffmpeg")), "ffmpeg")
    for k in ("tts.kokoro.model", "tts.piper.model_dir", "qa.asr_model_dir"):
        print(ok(cfg.path(k).exists()), k, cfg.path(k))
    for mod in ("cairo", "kokoro_onnx", "sherpa_onnx", "pyloudnorm", "scipy", "soundfile"):
        try:
            __import__(mod)
            print("✅", mod)
        except ImportError:
            print("❌", mod)
    for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "ELEVENLABS_API_KEY"):
        print("🔑" if env(k) else "  ", k, "configurada" if env(k) else "no configurada (opcional)")
    print(ok((ROOT / cfg["youtube"]["client_secrets"]).exists()), "YouTube OAuth client_secret.json (opcional)")


def _summary(res: dict):
    print("\n" + "=" * 60)
    print("Vídeo:", res["final"])
    print("Estado:", res["status"])
    if res.get("qa"):
        for c in res["qa"]["checks"]:
            print(("  ✅ " if c["ok"] else ("  ⚠️ " if c["severity"] == "warning" else "  ❌ ")) + f"{c['check']}: {c['detail']}")
    print("Título:", res["metadata"]["title"])
    print("=" * 60)


def main(argv=None):
    setup_logging()
    ap = argparse.ArgumentParser(prog="fabrica", description="Fábrica de YouTube Shorts animados")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("make"); s.add_argument("story"); s.add_argument("--workers", type=int, default=4)
    s.add_argument("--force", nargs="*"); s.add_argument("--no-qa", action="store_true"); s.set_defaults(f=cmd_make)
    s = sub.add_parser("auto"); s.add_argument("--idea"); s.add_argument("--workers", type=int, default=4); s.set_defaults(f=cmd_auto)
    s = sub.add_parser("regen"); s.add_argument("slug"); s.add_argument("scenes", nargs="+")
    s.add_argument("--story", help="guion editado (por defecto output/<slug>/script.json)")
    s.add_argument("--workers", type=int, default=4); s.add_argument("--no-qa", action="store_true"); s.set_defaults(f=cmd_regen)
    s = sub.add_parser("still"); s.add_argument("story"); s.add_argument("scene"); s.add_argument("t", type=float, nargs="?")
    s.set_defaults(f=cmd_still)
    s = sub.add_parser("ideas"); s.add_argument("--n", type=int, default=15); s.set_defaults(f=cmd_ideas)
    sub.add_parser("list").set_defaults(f=cmd_list)
    s = sub.add_parser("approve"); s.add_argument("slug"); s.set_defaults(f=cmd_approve)
    s = sub.add_parser("upload"); s.add_argument("slug"); s.add_argument("--privacy", default=None); s.set_defaults(f=cmd_upload)
    sub.add_parser("metrics").set_defaults(f=cmd_metrics)
    sub.add_parser("insights").set_defaults(f=cmd_insights)
    sub.add_parser("doctor").set_defaults(f=cmd_doctor)
    a = ap.parse_args(argv)
    try:
        a.f(a)
    except (RuntimeError, PermissionError, FileNotFoundError) as e:
        log.error("%s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
