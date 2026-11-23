"""Voz de ElevenLabs («Mario») para los vídeos nuevos del canal.

La voz se genera con el conector de ElevenLabs de Claude (una toma por escena), no con la API directa, así
que este script solo prepara y aplica el resultado:

  python3 scripts/voz_elevenlabs.py list  <slug>          # texto exacto de cada escena a sintetizar + caracteres
  python3 scripts/voz_elevenlabs.py apply <slug> <carpeta> # <carpeta>/<id_escena>.mp3 -> clips + voice_clip en la historia

`apply` acelera cada clip (config tts.eleven_connector.speed, sin cambiar el tono), lo guarda en
assets/voice_eleven/<slug>/<id>.wav y apunta `voice_clip` de cada escena a él. Después `python -m fabrica make`
alinea las palabras con las pausas reales del audio y renderiza con subtítulos y boca sincronizados.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fabrica.core.config import load_config  # noqa: E402
from fabrica.tts.narrator import normalize_numbers  # noqa: E402


def _cfg() -> dict:
    return load_config()["tts"]["eleven_connector"]


def _spoken(text: str, lexicon: dict) -> str:
    import re
    t = normalize_numbers(text)
    for k, v in lexicon.items():
        t = re.sub(rf"\b{re.escape(k)}\b", v, t)
    return t


def _story(slug: str) -> tuple[Path, dict]:
    f = ROOT / "stories" / f"{slug}.json"
    return f, json.loads(f.read_text(encoding="utf-8"))


def cmd_list(slug: str) -> None:
    c = _cfg()
    lex = load_config()["tts"].get("lexicon", {}) or {}
    _, d = _story(slug)
    total = 0
    for s in d["scenes"]:
        t = _spoken(s["narration"], lex)
        total += len(t)
        print(f"{s['id']}\t{len(t)}\t{t}")
    print(f"\nTOTAL {total} caracteres en {len(d['scenes'])} escenas · voz {c['voice_id']} · modelo {c['model_id']}")


def cmd_apply(slug: str, folder: str) -> None:
    c = _cfg()
    f, d = _story(slug)
    src = Path(folder)
    out = ROOT / "assets" / "voice_eleven" / slug
    out.mkdir(parents=True, exist_ok=True)
    missing = [s["id"] for s in d["scenes"] if not (src / f"{s['id']}.mp3").exists()]
    if missing:
        sys.exit(f"Faltan clips para: {', '.join(missing)}")
    for s in d["scenes"]:
        wav = out / f"{s['id']}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src / f"{s['id']}.mp3"), "-filter:a",
                        f"atempo={c['speed']}", "-ar", "24000", "-ac", "1", str(wav)], check=True)
        s["voice_clip"] = str(wav.relative_to(ROOT))
    f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(d['scenes'])} escenas con voice_clip → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "list":
        cmd_list(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "apply":
        cmd_apply(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
