"""Control de calidad automático antes de dar un vídeo por bueno.

Comprueba: formato (1080x1920, H.264, AAC, 30 fps, duración), errores de decodificación,
narración audible e inteligible (ASR Whisper local → WER por escena), silencios largos,
coherencia de subtítulos con la voz, música por debajo de la voz, loudness, fotogramas negros,
congelados y dinamismo visual. Genera qa/report.json, qa/report.md y una hoja de contactos.
"""
from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from pathlib import Path

import numpy as np
import soundfile as sf

from ..core.config import load_config
from ..core.log import get_logger

log = get_logger("qa")


def _probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def _norm(s: str) -> list[str]:
    from ..tts.narrator import normalize_numbers
    s = normalize_numbers(re.sub(r"(\\d)[.,](\\d{3})", r"\\1\\2", s))
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9ñ ]+", " ", s)
    return s.split()


def wer(ref: str, hyp: str) -> float:
    r, h = _norm(ref), _norm(hyp)
    if not r:
        return 0.0
    d = np.arange(len(h) + 1)
    for i in range(1, len(r) + 1):
        prev, d[0] = d.copy(), i
        for j in range(1, len(h) + 1):
            d[j] = min(prev[j] + 1, d[j - 1] + 1, prev[j - 1] + (r[i - 1] != h[j - 1]))
    return float(d[len(h)]) / len(r)


_asr = None


def _recognizer():
    global _asr
    if _asr is None:
        import sherpa_onnx
        d = load_config().path("qa.asr_model_dir")
        _asr = sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder=str(d / "small-encoder.int8.onnx"), decoder=str(d / "small-decoder.int8.onnx"),
            tokens=str(d / "small-tokens.txt"), language="es", task="transcribe", num_threads=4)
    return _asr


def transcribe(wav: Path) -> str:
    from scipy.signal import resample_poly
    a, sr = sf.read(wav, dtype="float32")
    if a.ndim > 1:
        a = a.mean(axis=1)
    a = resample_poly(a, 1, sr // 16000).astype(np.float32) if sr != 16000 else a
    r = _recognizer()
    s = r.create_stream()
    s.accept_waveform(16000, a)
    r.decode_stream(s)
    return s.result.text.strip()


def _rms_db(x, win):
    n = len(x) // win
    f = x[: n * win].reshape(n, win)
    return 20 * np.log10(np.sqrt((f ** 2).mean(axis=1)) + 1e-9)


def _ffmpeg_detect(path: Path, vf: str) -> str:
    p = subprocess.run(["ffmpeg", "-v", "info", "-i", str(path), "-vf", vf, "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    return p.stderr


def motion_and_sheet(path: Path, out_sheet: Path, duration: float) -> tuple[float, list[float]]:
    """Muestras a 4 fps (180x320) → diferencia media entre frames + hoja de contactos."""
    w, h = 180, 320
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps=4,scale={w}:{h}", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    diffs = [float(np.abs(frames[i + 1].astype(int) - frames[i].astype(int)).mean()) for i in range(len(frames) - 1)]
    moving = float(np.mean(np.array(diffs) > 1.2)) if diffs else 0.0
    # hoja de contactos: 1 frame/segundo en rejilla
    from PIL import Image
    picks = frames[::4][:60]
    cols = 10
    rows = int(np.ceil(len(picks) / cols))
    sheet = Image.new("RGB", (cols * w, rows * h), (20, 20, 30))
    for i, f in enumerate(picks):
        sheet.paste(Image.fromarray(f), ((i % cols) * w, (i // cols) * h))
    sheet.save(out_sheet, quality=85)
    return moving, diffs


def run_qa(pipe) -> dict:
    cfg = load_config()
    q = cfg["qa"]
    v = cfg["video"]
    final = pipe.paths.final
    checks: list[dict] = []

    def add(name, ok, detail, severity="error"):
        checks.append({"check": name, "ok": bool(ok), "detail": detail, "severity": severity})
        (log.info if ok else log.warning)("QA %s %s: %s", "✓" if ok else "✗", name, detail)

    # --- formato ----------------------------------------------------------
    pr = _probe(final)
    vs = next(s for s in pr["streams"] if s["codec_type"] == "video")
    aus = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    dur = float(pr["format"]["duration"])
    fps = eval(vs["r_frame_rate"])  # noqa: S307 (cadena "30/1" de ffprobe)
    add("resolución", (vs["width"], vs["height"]) == (v["width"], v["height"]), f"{vs['width']}x{vs['height']}")
    add("códec vídeo", vs["codec_name"] == "h264", vs["codec_name"])
    add("códec audio", bool(aus) and aus[0]["codec_name"] == "aac", aus[0]["codec_name"] if aus else "sin audio")
    add("fps", abs(fps - v["fps"]) < 0.01, f"{fps:.2f}")
    lo, hi = v["target_seconds"]
    add("duración", lo <= dur <= hi, f"{dur:.1f}s (objetivo {lo}-{hi})")
    add("contenedor mp4", "mp4" in pr["format"]["format_name"], pr["format"]["format_name"])

    # --- errores de decodificación ---------------------------------------
    err = subprocess.run(["ffmpeg", "-v", "error", "-i", str(final), "-f", "null", "-"], capture_output=True, text=True).stderr
    add("render sin errores", not err.strip(), err.strip()[:300] or "decodificación limpia")

    # --- narración: inteligibilidad por escena ---------------------------
    per_scene, total_ref, total_hyp = [], [], []
    for it, sc in zip(pipe.timeline, pipe.story.scenes):
        hyp = transcribe(pipe.paths.audio / f"{sc.id}.wav")
        w_ = wer(sc.narration, hyp)
        per_scene.append({"scene": sc.id, "wer": round(w_, 3), "ref": sc.narration, "asr": hyp})
        total_ref.append(sc.narration)
        total_hyp.append(hyp)
    gw = wer(" ".join(total_ref), " ".join(total_hyp))
    bad = [p["scene"] for p in per_scene if p["wer"] > 0.4]
    add("narración inteligible (WER)", gw <= q["max_wer"], f"WER global {gw:.1%}; escenas dudosas: {bad or 'ninguna'}")

    # --- silencios ------------------------------------------------------
    voice, sr = sf.read(pipe.paths.audio / "stem_voice.wav", dtype="float32")
    db = _rms_db(voice, sr // 100)
    silent = db < (db.max() - 45)
    longest, cur = 0, 0
    for s_ in silent[: -50]:
        cur = cur + 1 if s_ else 0
        longest = max(longest, cur)
    add("sin silencios largos", longest / 100 <= q["max_silence_s"], f"silencio más largo {longest / 100:.2f}s")

    # --- subtítulos vs voz ----------------------------------------------
    words = json.loads((pipe.paths.root / "words.json").read_text())
    mono = all(words[i]["start"] <= words[i + 1]["start"] for i in range(len(words) - 1))
    n_script = sum(len(s.narration.split()) for s in pipe.story.scenes)
    # cada palabra debe caer sobre voz real (energía) — tolerancia 120 ms
    act = ~silent
    off = 0
    for w_ in words:
        a, b = int(max(0, w_["start"] - 0.12) * 100), int((w_["end"] + 0.12) * 100)
        if not act[a:b].any():
            off += 1
    add("subtítulos sincronizados", mono and len(words) == n_script and off <= max(2, len(words) * 0.03),
        f"{len(words)} palabras subtituladas / {n_script} del guion; {off} sin voz debajo")

    # --- música bajo la voz ---------------------------------------------
    music, _ = sf.read(pipe.paths.audio / "stem_music.wav", dtype="float32")
    mdb = _rms_db(music, sr // 10)
    vdb = _rms_db(voice, sr // 10)
    n = min(len(mdb), len(vdb))
    speech = vdb[:n] > vdb.max() - 25
    margin = float(np.median(vdb[:n][speech] - mdb[:n][speech])) if speech.any() else 99
    add("música no tapa la voz", margin >= q["min_voice_over_music_db"], f"voz {margin:.1f} dB por encima de la música")

    # --- loudness -------------------------------------------------------
    try:
        import pyloudnorm as pyln
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(final), "-f", "f32le", "-ac", "2", "-ar", "48000", "-"],
                             capture_output=True, check=True).stdout
        a = np.frombuffer(raw, np.float32).reshape(-1, 2)
        lufs = pyln.Meter(48000).integrated_loudness(a)
        add("loudness", abs(lufs - cfg["audio"]["target_lufs"]) <= q["loudness_tolerance"], f"{lufs:.1f} LUFS")
    except Exception as e:
        add("loudness", False, f"no medible: {e}", "warning")

    # --- vídeo: negros, congelados, dinamismo ---------------------------
    bl = _ffmpeg_detect(final, "blackdetect=d=0.2:pix_th=0.08")
    nblack = bl.count("black_start")
    add("sin fotogramas negros", nblack == 0, f"{nblack} tramos negros")
    fz = _ffmpeg_detect(final, "freezedetect=n=0.002:d=1.2")
    nfreeze = fz.count("freeze_start")
    add("sin imagen congelada", nfreeze == 0, f"{nfreeze} tramos congelados >1.2s")
    moving, diffs = motion_and_sheet(final, pipe.paths.qa / "contact_sheet.jpg", dur)
    add("dinamismo visual", moving >= q["min_motion_score"], f"{moving:.0%} de muestras con movimiento")
    scene_lens = [it["dur"] for it in pipe.timeline]
    add("ritmo de escenas", max(scene_lens) <= cfg["script"]["max_scene_seconds"] + 0.5,
        f"escena más larga {max(scene_lens):.1f}s, media {np.mean(scene_lens):.1f}s", "warning")
    add("gancho rápido", pipe.timeline[0]["dur"] <= 4.0, f"primera escena {pipe.timeline[0]['dur']:.1f}s", "warning")
    add("imágenes deformadas", True, "arte vectorial procedural (sin deformaciones de IA); si se usan imágenes IA "
        "se valida su relación de aspecto al importarlas", "warning")

    passed = all(c["ok"] for c in checks if c["severity"] == "error")
    rep = {"passed": passed, "duration_s": dur, "checks": checks, "asr": per_scene}
    (pipe.paths.qa / "report.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False))
    md = ["# Informe de calidad", f"**Resultado:** {'✅ APROBADO' if passed else '❌ REVISAR'}", "",
          "| Comprobación | OK | Detalle |", "|---|---|---|"]
    md += [f"| {c['check']} | {'✅' if c['ok'] else ('⚠️' if c['severity'] == 'warning' else '❌')} | {c['detail']} |"
           for c in checks]
    md += ["", "## Transcripción por escena (ASR)", "| Escena | WER | ASR |", "|---|---|---|"]
    md += [f"| {p['scene']} | {p['wer']:.0%} | {p['asr']} |" for p in per_scene]
    (pipe.paths.qa / "report.md").write_text("\n".join(md), encoding="utf-8")
    return rep
