"""Generación opcional de fondos con IA (OpenAI gpt-image-1, Gemini, Replicate/FLUX).

Solo se usa si `images.provider` != none y la escena tiene `visual.image_prompt`.
La IA crea un fondo estático en el estilo del canal; el movimiento (cámara, personaje, props,
partículas) lo sigue aportando el motor por código → coherencia visual y bajo coste
(~0,003-0,04 USD por imagen). Las imágenes se cachean por prompt y se valida su relación de aspecto.
"""
from __future__ import annotations

import base64
import hashlib
from pathlib import Path

import requests

from ..core.config import env, load_config
from ..core.costs import ledger, price
from ..core.log import get_logger
from ..core.retry import PermanentError, retry

log = get_logger("imagegen")


@retry(tries=3)
def _openai(prompt: str) -> bytes:
    r = requests.post("https://api.openai.com/v1/images/generations", timeout=300,
                      headers={"Authorization": f"Bearer {env('OPENAI_API_KEY')}"},
                      json={"model": "gpt-image-1", "prompt": prompt, "size": "1024x1536", "quality": "medium"})
    if r.status_code in (400, 401, 403):
        raise PermanentError(r.text)
    r.raise_for_status()
    return base64.b64decode(r.json()["data"][0]["b64_json"])


@retry(tries=3)
def _gemini(prompt: str) -> bytes:
    r = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent",
                      params={"key": env("GEMINI_API_KEY")}, timeout=300,
                      json={"contents": [{"parts": [{"text": prompt + " Vertical 9:16 composition."}]}]})
    if r.status_code in (400, 401, 403):
        raise PermanentError(r.text)
    r.raise_for_status()
    for p in r.json()["candidates"][0]["content"]["parts"]:
        if "inlineData" in p:
            return base64.b64decode(p["inlineData"]["data"])
    raise RuntimeError("Gemini no devolvió imagen")


@retry(tries=3)
def _replicate(prompt: str) -> bytes:
    r = requests.post("https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions",
                      headers={"Authorization": f"Bearer {env('REPLICATE_API_TOKEN')}", "Prefer": "wait"},
                      json={"input": {"prompt": prompt, "aspect_ratio": "9:16", "output_format": "png"}}, timeout=300)
    if r.status_code in (400, 401, 403):
        raise PermanentError(r.text)
    r.raise_for_status()
    return requests.get(r.json()["output"][0], timeout=120).content


PROVIDERS = {"openai": (_openai, "OPENAI_API_KEY", "image_openai"),
             "gemini": (_gemini, "GEMINI_API_KEY", "image_gemini"),
             "replicate": (_replicate, "REPLICATE_API_TOKEN", "image_replicate")}


def generate_backgrounds(story, out_dir: Path) -> None:
    cfg = load_config()["images"]
    prov = cfg.get("provider", "none")
    if prov == "none" or prov not in PROVIDERS:
        return
    fn, key, cost_key = PROVIDERS[prov]
    if not env(key):
        log.warning("images.provider=%s pero falta %s; uso fondos vectoriales", prov, key)
        return
    from PIL import Image
    for sc in story.scenes:
        prompt = sc.visual.image_prompt
        if not prompt:
            continue
        full = f"{prompt}. {cfg['style_prompt']}. Background only, no characters, no text."
        f = out_dir / f"bg_{hashlib.sha1(full.encode()).hexdigest()[:12]}.png"
        if not f.exists():
            ledger().check(price(cost_key))
            data = fn(full)
            ledger().add(f"image:{prov}", sc.id, price(cost_key))
            f.write_bytes(data)
            im = Image.open(f)
            ratio = im.width / im.height
            if not 0.45 < ratio < 0.8:
                log.warning("%s: imagen con proporción %.2f (esperado 9:16); se recorta", sc.id, ratio)
            im.convert("RGB").save(f)
        sc.visual.background = {"type": "image", "path": str(f), **{k: v for k, v in sc.visual.background.items()
                                                                     if k in ("kenburns",)}}
