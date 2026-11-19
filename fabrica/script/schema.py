"""Esquema del guion. Un guion = lista de escenas con narración + descripción visual (DSL).

La parte visual es un pequeño lenguaje declarativo que entiende `fabrica.visuals`:
  background: {type: backyard|strata|mantle|outer_core|inner_core|earth_section|space|...}
  character:  {action, expression, outfit, x, y, scale, facing}
  props:      [{type, x, y, scale, enter, loop, ...}]
  overlays:   [{type: fact|fiction|counter|depth|label|myth, ...}]
  camera:     {move: push_in|pull_out|pan_up|pan_down|static|punch, shake: 0..1}
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

Beat = Literal["hook", "setup", "development", "climax", "ending"]


class Claim(BaseModel):
    text: str
    kind: Literal["fact", "fiction", "estimate"] = "fact"
    source: str = ""
    verified: bool | None = None
    note: str = ""


class SfxCue(BaseModel):
    name: str
    at: float = 0.0          # segundos desde el inicio de la escena (o "word:<n>" con at_word)
    at_word: int | None = None
    gain_db: float = 0.0


class Visual(BaseModel):
    background: dict[str, Any] = Field(default_factory=lambda: {"type": "backyard"})
    character: dict[str, Any] | None = Field(default_factory=lambda: {"action": "idle"})
    props: list[dict[str, Any]] = Field(default_factory=list)
    overlays: list[dict[str, Any]] = Field(default_factory=list)
    camera: dict[str, Any] = Field(default_factory=lambda: {"move": "push_in"})
    image_prompt: str | None = None   # si hay generador de imágenes, fondo generado por IA


class Scene(BaseModel):
    id: str
    beat: Beat = "development"
    narration: str
    emphasis: list[str] = Field(default_factory=list)   # palabras a resaltar en subtítulos
    claims: list[Claim] = Field(default_factory=list)
    visual: Visual = Field(default_factory=Visual)
    sfx: list[SfxCue] = Field(default_factory=list)
    transition: Literal["cut", "whip", "zoom", "flash", "circle", "slide"] = "whip"
    pause_after: float = 0.08
    voice: dict[str, Any] | None = None      # cambia la voz solo en esta escena, p. ej. {"voice": "es-ES-ElviraNeural"}
    voice_clip: str | None = None            # vídeo real cuya voz sustituye al TTS (si el archivo existe)

    @field_validator("narration")
    @classmethod
    def _strip(cls, v: str) -> str:
        return re.sub(r"\s+", " ", v).strip()


class Story(BaseModel):
    title: str
    idea: str
    slug: str = ""
    category: str = "ciencia"
    hook: str = ""
    question: str = ""                  # pregunta final para comentarios
    music_mood: str = "adventure"
    scenes: list[Scene]
    metadata: dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, _ctx: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.idea)
        if not self.hook and self.scenes:
            self.hook = self.scenes[0].narration

    @property
    def full_text(self) -> str:
        return " ".join(s.narration for s in self.scenes)

    @property
    def word_count(self) -> int:
        return len(self.full_text.split())


def slugify(text: str, maxlen: int = 60) -> str:
    t = unicodedata.normalize("NFKD", text.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:maxlen].rstrip("-")
