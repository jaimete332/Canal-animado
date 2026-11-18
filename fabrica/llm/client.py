"""Cliente LLM multiproveedor (Anthropic / OpenAI / Gemini) vía HTTP, con reintentos y coste.

provider: auto → usa el primero con API key disponible: ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY.
Sin claves → NoLLMAvailable (el sistema usa guiones/plantillas locales).
"""
from __future__ import annotations

import json
import re

import requests

from ..core.config import env, load_config
from ..core.costs import ledger, price
from ..core.log import get_logger
from ..core.retry import PermanentError, retry

log = get_logger("llm")


class NoLLMAvailable(RuntimeError):
    pass


def available_provider() -> str | None:
    cfg = load_config()["llm"]
    p = cfg.get("provider", "auto")
    if p == "offline":
        return None
    keys = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY", "gemini": "GEMINI_API_KEY"}
    if p != "auto":
        return p if env(keys[p]) else None
    for name, k in keys.items():
        if env(k):
            return name
    return None


def _extract_json(text: str):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1)
    start = min([i for i in (text.find("{"), text.find("[")) if i >= 0], default=0)
    return json.loads(text[start:])


@retry(tries=3)
def complete(system: str, prompt: str, as_json: bool = True, max_tokens: int = 6000, temperature: float | None = None):
    cfg = load_config()["llm"]
    prov = available_provider()
    if not prov:
        raise NoLLMAvailable("No hay API key de LLM configurada (ver docs/API_KEYS.md)")
    temp = cfg.get("temperature", 0.9) if temperature is None else temperature
    if prov == "anthropic":
        r = requests.post("https://api.anthropic.com/v1/messages", timeout=180, headers={
            "x-api-key": env("ANTHROPIC_API_KEY"), "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": cfg["anthropic_model"], "max_tokens": max_tokens, "temperature": temp, "system": system,
                  "messages": [{"role": "user", "content": prompt}]})
        if r.status_code in (400, 401, 403):
            raise PermanentError(r.text)
        r.raise_for_status()
        j = r.json()
        out = "".join(b.get("text", "") for b in j["content"])
        u = j.get("usage", {})
        cost = u.get("input_tokens", 0) / 1e6 * price("anthropic_in_per_mtok") + \
            u.get("output_tokens", 0) / 1e6 * price("anthropic_out_per_mtok")
    elif prov == "openai":
        body = {"model": cfg["openai_model"], "messages": [{"role": "system", "content": system},
                                                         {"role": "user", "content": prompt}]}
        if as_json:
            body["response_format"] = {"type": "json_object"}
        r = requests.post("https://api.openai.com/v1/chat/completions", timeout=180,
                          headers={"Authorization": f"Bearer {env('OPENAI_API_KEY')}"}, json=body)
        if r.status_code in (400, 401, 403):
            raise PermanentError(r.text)
        r.raise_for_status()
        j = r.json()
        out = j["choices"][0]["message"]["content"]
        u = j.get("usage", {})
        cost = u.get("prompt_tokens", 0) / 1e6 * price("openai_in_per_mtok") + \
            u.get("completion_tokens", 0) / 1e6 * price("openai_out_per_mtok")
    else:
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{cfg['gemini_model']}:generateContent",
            params={"key": env("GEMINI_API_KEY")}, timeout=180,
            json={"systemInstruction": {"parts": [{"text": system}]},
                  "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                  "generationConfig": {"temperature": temp, "maxOutputTokens": max_tokens,
                                       **({"responseMimeType": "application/json"} if as_json else {})}})
        if r.status_code in (400, 401, 403):
            raise PermanentError(r.text)
        r.raise_for_status()
        j = r.json()
        out = "".join(p.get("text", "") for p in j["candidates"][0]["content"]["parts"])
        u = j.get("usageMetadata", {})
        cost = u.get("promptTokenCount", 0) / 1e6 * price("gemini_in_per_mtok") + \
            u.get("candidatesTokenCount", 0) / 1e6 * price("gemini_out_per_mtok")
    ledger().add(f"llm:{prov}", "completion", cost)
    return _extract_json(out) if as_json else out
