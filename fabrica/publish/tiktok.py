"""Publicación en TikTok mediante la Content Posting API oficial (v2) — SIEMPRE con tu aprobación.

Flujo:
  1. `python -m fabrica tiktok-auth`  → abre el login oficial de TikTok (OAuth 2.0 + PKCE) y guarda el token
     en secrets/tiktok_token.json (ignorado por git). Se hace una vez; el token se renueva solo.
  2. `python -m fabrica approve <slug>`  → la misma aprobación que para YouTube (hash del MP4).
  3. `python -m fabrica tiktok-upload <slug>`          → publicación directa (privada por defecto)
     `python -m fabrica tiktok-upload <slug> --draft`  → lo envía a tus borradores de la app de TikTok
     para que tú añadas sonido/portada y lo publiques desde el móvil.

Requisitos y límites: ver docs/TIKTOK.md (app de desarrollador, auditoría, privacidad).
"""
from __future__ import annotations

import base64
import hashlib
import json
import secrets as pysecrets
import time
import urllib.parse
from pathlib import Path

import requests

from ..core.config import ROOT, env, load_config
from ..core.log import get_logger
from ..core.paths import VideoPaths
from ..core.registry import Registry
from ..core.retry import PermanentError, retry
from .youtube import _check_approval

log = get_logger("tiktok")
API = "https://open.tiktokapis.com/v2"
AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
SCOPES = "user.info.basic,video.publish,video.upload"


def _cfg() -> dict:
    return load_config().get("tiktok", {}) or {}


def _token_file() -> Path:
    return ROOT / _cfg().get("token_file", "secrets/tiktok_token.json")


def _client():
    key, sec = env("TIKTOK_CLIENT_KEY"), env("TIKTOK_CLIENT_SECRET")
    if not key or not sec:
        raise PermissionError("Faltan TIKTOK_CLIENT_KEY / TIKTOK_CLIENT_SECRET en .env (ver docs/TIKTOK.md)")
    return key, sec


# --------------------------------------------------------------------------- OAuth
def authorize() -> None:
    """Login oficial con PKCE. Abre el navegador y captura el código en un servidor local."""
    import http.server
    import threading
    import webbrowser

    key, sec = _client()
    redirect = _cfg().get("redirect_uri", "http://localhost:8765/callback/")
    verifier = pysecrets.token_urlsafe(64)[:96]
    # TikTok (escritorio) espera el challenge en hex del SHA-256
    challenge = hashlib.sha256(verifier.encode()).hexdigest()
    state = pysecrets.token_urlsafe(16)
    url = AUTH_URL + "?" + urllib.parse.urlencode({
        "client_key": key, "scope": SCOPES, "response_type": "code", "redirect_uri": redirect, "state": state,
        "code_challenge": challenge, "code_challenge_method": "S256"})
    got: dict = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            got.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h2>Listo. Ya puedes cerrar esta pestaña.</h2>".encode())

        def log_message(self, *a):
            pass

    port = urllib.parse.urlparse(redirect).port or 8765
    srv = http.server.HTTPServer(("localhost", port), H)
    th = threading.Thread(target=srv.handle_request, daemon=True)
    th.start()
    print("Abre este enlace si no se abre solo:\n", url)
    webbrowser.open(url)
    th.join(timeout=300)
    srv.server_close()
    if got.get("state") != state or "code" not in got:
        raise PermissionError(f"Autorización cancelada o inválida: {got.get('error_description', got)}")
    r = requests.post(f"{API}/oauth/token/", timeout=30, data={
        "client_key": key, "client_secret": sec, "code": got["code"], "grant_type": "authorization_code",
        "redirect_uri": redirect, "code_verifier": verifier})
    _save_token(r)
    print("✅ Cuenta de TikTok autorizada")


def _save_token(r: requests.Response) -> dict:
    j = r.json()
    if r.status_code != 200 or "access_token" not in j:
        raise PermanentError(f"TikTok OAuth: {j}")
    j["obtained_at"] = time.time()
    f = _token_file()
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(j))
    return j


def access_token() -> str:
    f = _token_file()
    if not f.exists():
        raise PermissionError("TikTok no está autorizado: ejecuta `python -m fabrica tiktok-auth`")
    tok = json.loads(f.read_text())
    if time.time() > tok["obtained_at"] + tok.get("expires_in", 86400) - 300:
        key, sec = _client()
        tok = _save_token(requests.post(f"{API}/oauth/token/", timeout=30, data={
            "client_key": key, "client_secret": sec, "grant_type": "refresh_token",
            "refresh_token": tok["refresh_token"]}))
    return tok["access_token"]


def _post(path: str, body: dict) -> dict:
    r = requests.post(f"{API}{path}", json=body, timeout=60, headers={
        "Authorization": f"Bearer {access_token()}", "Content-Type": "application/json; charset=UTF-8"})
    j = r.json()
    err = (j.get("error") or {}).get("code", "ok")
    if r.status_code != 200 or err != "ok":
        raise PermanentError(f"TikTok {path}: {j.get('error')}")
    return j.get("data", {})


# --------------------------------------------------------------------------- subida
def caption_for(meta: dict) -> str:
    """Texto del post: título + gancho + pregunta + hashtags (máx. 2200 caracteres)."""
    tags = [h for h in meta.get("hashtags", []) if h.lower() != "#shorts"]
    tags = list(dict.fromkeys(tags + _cfg().get("extra_hashtags", [])))
    first = meta["description"].split("\n")[0]
    cap = f"{meta['title']}\n\n{first}\n\n{meta['pinned_comment']}\n\n{' '.join(tags)}"
    return cap[:2200]


@retry(tries=3)
def _put_chunk(url: str, data: bytes, start: int, total: int) -> None:
    r = requests.put(url, data=data, timeout=300, headers={
        "Content-Type": "video/mp4", "Content-Length": str(len(data)),
        "Content-Range": f"bytes {start}-{start + len(data) - 1}/{total}"})
    if r.status_code not in (200, 201, 206):
        raise RuntimeError(f"Subida de fragmento falló: {r.status_code} {r.text[:200]}")


def upload(slug: str, draft: bool = False, privacy: str | None = None) -> str:
    cfg = _cfg()
    if not cfg.get("enabled"):
        raise PermissionError("La publicación en TikTok está desactivada (tiktok.enabled: false en config.yaml)")
    _check_approval(slug)
    vp = VideoPaths(slug)
    meta = json.loads(vp.metadata.read_text())
    size = vp.final.stat().st_size
    chunk = size if size <= 64 * 1024 * 1024 else 10 * 1024 * 1024
    n = 1 if chunk == size else -(-size // chunk)
    source = {"source": "FILE_UPLOAD", "video_size": size, "chunk_size": chunk, "total_chunk_count": n}
    if draft:
        data = _post("/post/publish/inbox/video/init/", {"source_info": source})
    else:
        info = _post("/post/publish/creator_info/query/", {})
        allowed = info.get("privacy_level_options", [])
        level = privacy or cfg.get("privacy", "SELF_ONLY")
        if level not in allowed:
            log.warning("Privacidad %s no permitida para esta cuenta/app (%s); uso SELF_ONLY", level, allowed)
            level = "SELF_ONLY"
        data = _post("/post/publish/video/init/", {
            "post_info": {"title": caption_for(meta), "privacy_level": level,
                          "disable_comment": False, "disable_duet": False, "disable_stitch": False,
                          "video_cover_timestamp_ms": int(cfg.get("cover_ms", 1500)),
                          "is_aigc": True},  # contenido generado con IA (voz sintética)
            "source_info": source})
    pid, url = data["publish_id"], data["upload_url"]
    with open(vp.final, "rb") as f:
        for i in range(n):
            part = f.read(chunk if i < n - 1 else size - chunk * (n - 1))
            _put_chunk(url, part, i * chunk, size)
            log.info("TikTok: fragmento %d/%d subido", i + 1, n)
    status = "?"
    for _ in range(30):
        st = _post("/post/publish/status/fetch/", {"publish_id": pid})
        status = st.get("status")
        log.info("TikTok estado: %s", status)
        if status in ("PUBLISH_COMPLETE", "SEND_TO_USER_INBOX", "FAILED"):
            break
        time.sleep(5)
    if status == "FAILED":
        raise RuntimeError(f"TikTok rechazó el vídeo: {st.get('fail_reason')}")
    Registry().upsert_video(slug, status="uploaded_tiktok" if not draft else "tiktok_draft",
                            meta_json={**meta, "tiktok_publish_id": pid, "tiktok_status": status})
    return pid
