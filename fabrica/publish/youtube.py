"""Integración con YouTube Data API v3 (subida) — SIEMPRE requiere tu aprobación.

Seguridad:
  1. `python -m fabrica approve <slug>` crea output/<slug>/APPROVED con el hash del MP4.
     Si el vídeo cambia después, la aprobación deja de valer.
  2. `upload` se niega si no hay aprobación válida o si `youtube.enabled` es false.
  3. Privacidad por defecto: private (cámbiala tú en YouTube Studio o con --privacy).

Credenciales: ver docs/YOUTUBE.md (OAuth de escritorio; el token se guarda en secrets/).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import time
from pathlib import Path

from ..core.config import ROOT, load_config
from ..core.log import get_logger
from ..core.paths import VideoPaths
from ..core.registry import Registry

log = get_logger("youtube")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/yt-analytics.readonly"]


def _files(slug: str) -> dict[str, Path]:
    """Vídeo, metadatos, miniatura y aprobación: de output/<slug>/ o, si no existe (p. ej. en otra máquina
    tras `git pull`), de samples/<slug>/."""
    vp = VideoPaths(slug)
    root = vp.root if vp.final.exists() else ROOT / "samples" / slug
    return {"root": root, "final": root / "final.mp4", "metadata": root / "metadata.json",
            "thumbnail": root / "thumbnail.png", "approved": root / "APPROVED"}


def parse_when(when: str, tz: str | None = None) -> dt.datetime:
    """'2026-11-21 18:00' (hora local de `youtube.timezone`, por defecto Europe/Madrid) o ISO con zona → UTC."""
    from zoneinfo import ZoneInfo
    tz = tz or load_config()["youtube"].get("timezone", "Europe/Madrid")
    w = when.strip().replace("T", " ")
    try:
        d = dt.datetime.fromisoformat(w)
    except ValueError:
        raise ValueError(f"Fecha no válida: {when!r}. Usa 'AAAA-MM-DD HH:MM', p. ej. '2026-11-21 18:00'")
    if d.tzinfo is None:
        d = d.replace(tzinfo=ZoneInfo(tz))
    d = d.astimezone(dt.timezone.utc)
    if d < dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15):
        raise ValueError(f"La hora {when} ya ha pasado o está a menos de 15 minutos: elige una más tarde")
    return d


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def approve(slug: str) -> None:
    f = _files(slug)
    if not f["final"].exists():
        raise FileNotFoundError(f["final"])
    f["approved"].write_text(json.dumps({"sha256": _sha(f["final"]), "at": time.time()}))


def _check_approval(slug: str) -> None:
    fs = _files(slug)
    f = fs["approved"]
    if not f.exists():
        raise PermissionError(f"'{slug}' no está aprobado. Revísalo y ejecuta: python -m fabrica approve {slug}")
    if json.loads(f.read_text())["sha256"] != _sha(fs["final"]):
        raise PermissionError("El vídeo cambió después de aprobarlo: vuelve a revisarlo y aprobarlo")


def credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    cfg = load_config()["youtube"]
    tok = ROOT / cfg["token_file"]
    creds = Credentials.from_authorized_user_file(str(tok), SCOPES) if tok.exists() else None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        sec = ROOT / cfg["client_secrets"]
        if not sec.exists():
            raise FileNotFoundError(f"Falta {sec} (ver docs/YOUTUBE.md)")
        creds = InstalledAppFlow.from_client_secrets_file(str(sec), SCOPES).run_local_server(port=0)
        tok.parent.mkdir(parents=True, exist_ok=True)
        tok.write_text(creds.to_json())
    return creds


def build_body(slug: str, privacy: str | None = None, publish_at: dt.datetime | None = None) -> dict:
    """Cuerpo de videos.insert. Con `publish_at`, el vídeo se sube privado y YouTube lo publica solo a esa hora."""
    cfg = load_config()["youtube"]
    meta = json.loads(_files(slug)["metadata"].read_text())
    status = {"privacyStatus": privacy or cfg.get("privacy", "private"), "selfDeclaredMadeForKids": False,
              "containsSyntheticMedia": bool(meta.get("contains_synthetic_media", True))}
    if publish_at:
        status["privacyStatus"] = "private"  # requisito de la API para programar
        status["publishAt"] = publish_at.strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "snippet": {"title": meta["title"][:100], "description": meta["description"][:5000],
                    "tags": meta.get("tags", [])[:30], "categoryId": meta.get("category_id", "27"),
                    "defaultLanguage": "es", "defaultAudioLanguage": "es-ES"},
        "status": status,
    }


def upload(slug: str, privacy: str | None = None, publish_at: str | None = None, dry_run: bool = False) -> str:
    """Sube un vídeo aprobado. `publish_at` ('AAAA-MM-DD HH:MM', hora local) lo deja programado en YouTube."""
    cfg = load_config()["youtube"]
    when = parse_when(publish_at) if publish_at else None
    fs = _files(slug)
    body = build_body(slug, privacy, when)
    if dry_run:
        _check_approval(slug)
        log.info("Simulación (no se sube nada): %s", json.dumps(body["status"]))
        return "dry-run"
    if not cfg.get("enabled"):
        raise PermissionError("La publicación está desactivada (youtube.enabled: false en config.yaml)")
    _check_approval(slug)
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    meta = json.loads(fs["metadata"].read_text())
    yt = build("youtube", "v3", credentials=credentials())
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(str(fs["final"]), chunksize=8 << 20, resumable=True))
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            log.info("Subiendo… %d%%", int(status.progress() * 100))
    vid = resp["id"]
    log.info("Subido: %s%s", vid, f" (se publicará el {body['status']['publishAt']} UTC)" if when else "")
    if fs["thumbnail"].exists():  # requiere canal verificado por teléfono
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(fs["thumbnail"]))).execute()
        except Exception as e:
            log.warning("No se pudo poner la miniatura (¿canal sin verificar por teléfono?): %s", e)
    try:  # comentario fijado (YouTube no permite fijarlo por API: se publica y lo fijas en Studio)
        yt.commentThreads().insert(part="snippet", body={"snippet": {"videoId": vid, "topLevelComment": {
            "snippet": {"textOriginal": meta["pinned_comment"]}}}}).execute()
    except Exception as e:
        log.warning("No se pudo publicar el comentario (si está programado, publícalo cuando salga): %s", e)
    Registry().upsert_video(slug, status="scheduled" if when else "uploaded", youtube_id=vid)
    return vid
