"""Orquestador: idea → guion → revisión → voz → audio → escenas → subtítulos → render → QA → metadatos.

Cada paso guarda sus archivos intermedios en output/<slug>/ y es reanudable:
si un paso ya está hecho y sus entradas no han cambiado, se reutiliza.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

import numpy as np
import soundfile as sf

from .audio import music as musiclib
from .audio.mixer import Cue, mix
from .core.config import ROOT, load_config
from .core.costs import reset_ledger
from .core.log import get_logger, setup_logging
from .core.paths import VideoPaths
from .core.registry import Registry
from .edit.subtitles import build_ass
from .script.schema import Story
from .tts.narrator import SR, Narrator
from .visuals.fonts import ensure_fonts

log = get_logger("pipeline")

AUTO_SFX = {"whip": "whoosh", "zoom": "whoosh", "slide": "whoosh", "circle": "whoosh", "flash": "pop"}


def _h(obj) -> str:
    return hashlib.sha1(json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()[:16]


def _render_job(item: dict, out: str, fps: int) -> str:
    from .visuals.fonts import ensure_fonts as _ef
    from .visuals.scene import render_scene
    _ef()
    render_scene(item, Path(out), fps)
    return out


class Pipeline:
    def __init__(self, story: Story, workers: int = 4, force: set[str] | None = None):
        self.cfg = load_config()
        self.story = story
        self.paths = VideoPaths(story.slug)
        self.paths.root.mkdir(parents=True, exist_ok=True)
        setup_logging(logfile=self.paths.log)
        self.workers = workers
        self.force = force or set()
        self.fps = self.cfg["video"]["fps"]
        self.ledger = reset_ledger()
        self.timeline: list[dict] = []

    # 1) guion -------------------------------------------------------------
    def save_script(self):
        self.paths.script.write_text(self.story.model_dump_json(indent=2), encoding="utf-8")

    # 2) narración ---------------------------------------------------------
    def narrate(self):
        nar = Narrator(self.paths.audio / "cache")
        t = 0.0
        voice_parts = []
        self.timeline = []
        nscenes = len(self.story.scenes)
        for i, sc in enumerate(self.story.scenes):
            clip = (ROOT / sc.voice_clip) if sc.voice_clip else None
            if clip is not None and clip.exists():
                audio, words = nar.narrate_clip(sc.narration, clip, sc.pause_after)
                log.info("%s: usando la voz del clip real %s", sc.id, clip.name)
            else:
                audio, words = nar.narrate_scene(sc.narration, sc.pause_after, sc.voice)
            # duración en frames exactos para que vídeo y audio no deriven
            f0 = round(t * self.fps)
            dur = len(audio) / SR
            min_d = 1.0
            if dur < min_d:
                audio = np.concatenate([audio, np.zeros(int((min_d - dur) * SR), np.float32)])
                dur = min_d
            f1 = round((t + dur) * self.fps)
            frames = f1 - f0
            # ajusta audio al número exacto de frames
            need = int(round(frames / self.fps * SR))
            audio = np.pad(audio, (0, max(0, need - len(audio))))[:need]
            sf.write(self.paths.audio / f"{sc.id}.wav", audio, SR)
            voice_parts.append(audio)
            nxt = self.story.scenes[i + 1].transition if i + 1 < nscenes else "cut"
            self.timeline.append({
                "id": sc.id, "index": i, "start": f0 / self.fps, "dur": frames / self.fps, "frames": frames,
                "words": [{"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)} for w in words],
                "trans_in": sc.transition if i > 0 else "cut", "trans_out": nxt,
            })
            t = f1 / self.fps
        voice = np.concatenate(voice_parts)
        sf.write(self.paths.audio / "voice.wav", voice, SR)
        self.voice = voice
        self.duration = len(voice) / SR
        log.info("Narración: %.1f s, %d escenas", self.duration, nscenes)
        self.paths.timeline.write_text(json.dumps(self.timeline, indent=1, ensure_ascii=False))

    # 3) audio (música + efectos + mezcla) ----------------------------------
    def sound(self):
        acfg = self.cfg["audio"]
        beats = {s.id: s.beat for s in self.story.scenes}
        sections, last = [], None
        for it in self.timeline:
            b = beats[it["id"]]
            name = {"hook": "intro", "setup": "groove", "development": "groove", "climax": "climax",
                    "ending": "outro"}[b]
            if it["index"] == 0:
                name = "groove"
            if name != last:
                sections.append((it["start"], name))
                last = name
        music = None
        if acfg.get("music") == "library":
            music = self._library_music()
        if music is None:
            music = musiclib.compose(self.duration, self.story.music_mood, sections)
        cues: list[Cue] = [Cue("hit", 0.0, 2.0)]
        for it, sc in zip(self.timeline, self.story.scenes):
            if it["index"] > 0 and sc.transition in AUTO_SFX:
                cues.append(Cue(AUTO_SFX[sc.transition], max(0, it["start"] - 0.12), -3))
            for c in sc.sfx:
                tt = c.at
                if c.at_word is not None and it["words"]:
                    tt = it["words"][min(c.at_word, len(it["words"]) - 1)]["start"]
                cues.append(Cue(c.name, it["start"] + tt, c.gain_db))
        out, info = mix(self.voice, music, cues, acfg["music_gain_db"], acfg["duck_db"], acfg["sfx_gain_db"],
                        acfg["target_lufs"])
        sf.write(self.paths.audio / "mix.wav", out, SR)
        for k, v in info["stems"].items():
            sf.write(self.paths.audio / f"stem_{k}.wav", v, SR)
        log.info("Mezcla lista (LUFS de entrada %.1f)", info["input_lufs"] or 0)

    def _library_music(self):
        files = sorted((ROOT / "assets" / "music").glob("*.mp3")) + sorted((ROOT / "assets" / "music").glob("*.wav"))
        if not files:
            log.warning("No hay música en assets/music; uso música procedural")
            return None
        reg = Registry()
        f = files[len(reg.videos()) % len(files)]  # rota pistas entre vídeos
        from .tts.narrator import _resample
        from .tts.providers import _decode
        a, sr = _decode(f.read_bytes())
        a = _resample(a, sr)
        if len(a) < len(self.voice):
            a = np.tile(a, int(np.ceil(len(self.voice) / len(a))))
        return a[: len(self.voice)] / (np.abs(a).max() + 1e-9) * 0.8

    # 4) escenas -----------------------------------------------------------
    def scene_items(self) -> list[dict]:
        from .visuals.scene import mouth_curve
        items = []
        for it, sc in zip(self.timeline, self.story.scenes):
            item = dict(it)
            item["scene"] = sc.model_dump()
            item["mouth"] = mouth_curve(self.voice, SR, it["start"], it["frames"], self.fps)
            items.append(item)
        return items

    def render_scenes(self):
        items = self.scene_items()
        jobs = []
        code_ver = _h([p.stat().st_mtime for p in (ROOT / "fabrica" / "visuals").glob("*.py")])
        for item in items:
            out = self.paths.scenes / f"{item['id']}.mp4"
            hfile = out.with_suffix(".hash")
            h = _h([item, code_ver])
            if out.exists() and hfile.exists() and hfile.read_text() == h and item["id"] not in self.force:
                continue
            jobs.append((item, out, h))
        log.info("Renderizando %d/%d escenas (%d procesos)", len(jobs), len(items), self.workers)
        t0 = time.time()
        if jobs:
            with ProcessPoolExecutor(self.workers) as ex:
                futs = {ex.submit(_render_job, it, str(out), self.fps): (out, h) for it, out, h in
                        sorted(jobs, key=lambda j: -j[0]["frames"])}
                for f in as_completed(futs):
                    out, h = futs[f]
                    f.result()
                    out.with_suffix(".hash").write_text(h)
                    log.info("  ✓ %s", out.name)
        log.info("Escenas listas en %.0fs", time.time() - t0)

    # 5) subtítulos + montaje final ----------------------------------------
    def captions(self):
        words = []
        emphasis = set()
        for it, sc in zip(self.timeline, self.story.scenes):
            emphasis |= {e.lower() for e in sc.emphasis}
            for w in it["words"]:
                words.append({"word": w["word"], "start": it["start"] + w["start"], "end": it["start"] + w["end"]})
        self.paths.captions.write_text(build_ass(words, emphasis, self.duration), encoding="utf-8")
        (self.paths.root / "words.json").write_text(json.dumps(words, ensure_ascii=False, indent=0))

    def assemble(self):
        v = self.cfg["video"]
        lst = self.paths.root / "concat.txt"
        lst.write_text("".join(f"file 'scenes/{it['id']}.mp4'\n" for it in self.timeline))
        concat = self.paths.root / "video_concat.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                        str(concat)], check=True, cwd=self.paths.root)
        fonts = ROOT / "assets" / "fonts"
        vf = f"ass={self.paths.captions.name}:fontsdir={fonts}"
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-i", str(concat), "-i", str(self.paths.audio / "mix.wav"),
            "-vf", vf, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", v["preset"], "-crf", str(v["crf"]),
            "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(self.fps), "-c:a", "aac",
            "-b:a", v["audio_bitrate"], "-ar", str(v["sample_rate"]), "-movflags", "+faststart", "-shortest",
            str(self.paths.final)], check=True, cwd=self.paths.root)
        log.info("Vídeo final: %s", self.paths.final)

    # orquestación ---------------------------------------------------------
    def run(self, qa: bool = True) -> dict:
        ensure_fonts()
        t0 = time.time()
        reg = Registry()
        self.save_script()
        from .script.factcheck import review
        review_report = review(self.story)
        (self.paths.qa / "factcheck.json").write_text(json.dumps(review_report, indent=2, ensure_ascii=False))
        if review_report["blocking"]:
            raise RuntimeError(f"Revisión de datos bloqueante: {review_report['blocking']}")
        from .visuals.imagegen import generate_backgrounds
        generate_backgrounds(self.story, self.paths.images)
        self.narrate()
        self.sound()
        self.render_scenes()
        self.captions()
        self.assemble()
        from .publish.metadata import build_metadata, make_thumbnail
        meta = build_metadata(self.story, self.duration)
        self.paths.metadata.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
        make_thumbnail(self, meta)
        report = {}
        if qa:
            from .qa.checks import run_qa
            report = run_qa(self)
        self.ledger.save(self.paths.costs)
        status = "rendered" if (not report or report.get("passed")) else "qa_failed"
        reg.upsert_video(self.story.slug, title=meta["title"], idea=self.story.idea, category=self.story.category,
                         hook=self.story.hook, status=status, duration_s=self.duration, cost_usd=self.ledger.total,
                         qa_json=report, meta_json=meta)
        log.info("Hecho en %.0fs — estado: %s — coste: %.3f USD", time.time() - t0, status, self.ledger.total)
        return {"final": str(self.paths.final), "status": status, "qa": report, "metadata": meta}


def load_story(path: Path) -> Story:
    return Story.model_validate_json(Path(path).read_text(encoding="utf-8"))
