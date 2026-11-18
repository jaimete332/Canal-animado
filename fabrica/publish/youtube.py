"""Integración con YouTube Data API v3 (subida) — SIEMPRE requiere tu aprobación.

Seguridad:
  1. `python -m fabrica approve <slug>` crea output/<slug>/APPROVED con el hash del MP4.
     Si el vídeo cambia después, la aprobación deja de valer.
  2. `upload` se niega si no hay aprobación válida o si `youtube.enabled` es false.
  3. Privacidad por defecto: private (cámbiala tú en YouTube Studio o con --privacy).

Credenciales: ver docs/YOUTUBE.md (OAuth de escritorio; el token se guarda en secrets/).
"""
from __future__ import annotations

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


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def approve(slug: str) -> None:
    vp = VideoPaths(slug)
    if not vp.final.exists():
        raise FileNotFoundError(vp.final)
    (vp.root / "APPROVED").write_text(json.dumps({"sha256": _sha(vp.final), "at": time.time()}))


def _check_approval(slug: str) -> None:
    vp = VideoPaths(slug)
    f = vp.root / "APPROVED"
    if not f.exists():
        raise PermissionError(f"'{slug}' no está aprobado. Revísalo y ejecuta: python -m fabrica approve {slug}")
    if json.loads(f.read_text())["sha256"] != _sha(vp.final):
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


def upload(slug: str, privacy: str | None = None) -> str:
    cfg = load_config()["youtube"]
    if not cfg.get("enabled"):
        raise PermissionError("La publicación está desactivada (youtube.enabled: false en config.yaml)")
    _check_approval(slug)
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    vp = VideoPaths(slug)
    meta = json.loads(vp.metadata.read_text())
    yt = build("youtube", "v3", credentials=credentials())
    body = {
        "snippet": {"title": meta["title"][:100], "description": meta["description"][:5000],
                    "tags": meta.get("tags", [])[:30], "categoryId": meta.get("category_id", "27"),
                    "defaultLanguage": "es", "defaultAudioLanguage": "es-ES"},
        "status": {"privacyStatus": privacy or cfg.get("privacy", "private"), "selfDeclaredMadeForKids": False,
                   "containsSyntheticMedia": bool(meta.get("contains_synthetic_media", True))},
    }
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(str(vp.final), chunksize=8 << 20, resumable=True))
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            log.info("Subiendo… %d%%", int(status.progress() * 100))
    vid = resp["id"]
    log.info("Subido: %s", vid)
    try:  # comentario fijado (YouTube no permite fijarlo por API: se publica y lo fijas en Studio)
        yt.commentThreads().insert(part="snippet", body={"snippet": {"videoId": vid, "topLevelComment": {
            "snippet": {"textOriginal": meta["pinned_comment"]}}}}).execute()
    except Exception as e:
        log.warning("No se pudo publicar el comentario: %s", e)
    Registry().upsert_video(slug, status="uploaded", youtube_id=vid)
    return vid
