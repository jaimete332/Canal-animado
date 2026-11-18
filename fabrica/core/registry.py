"""Registro SQLite: vídeos creados, ideas usadas y métricas de YouTube."""
from __future__ import annotations

import json
import re
import sqlite3
import time
import unicodedata
from pathlib import Path

from .config import load_config

SCHEMA = """
CREATE TABLE IF NOT EXISTS videos (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  idea TEXT NOT NULL,
  idea_norm TEXT NOT NULL,
  category TEXT,
  hook TEXT,
  created_at REAL,
  status TEXT,               -- rendered | qa_failed | approved | uploaded
  duration_s REAL,
  cost_usd REAL,
  qa_json TEXT,
  youtube_id TEXT,
  meta_json TEXT
);
CREATE TABLE IF NOT EXISTS metrics (
  youtube_id TEXT,
  fetched_at REAL,
  views INTEGER, likes INTEGER, comments INTEGER, shares INTEGER,
  avg_view_duration_s REAL, avg_view_pct REAL, subscribers_gained INTEGER,
  raw_json TEXT,
  PRIMARY KEY (youtube_id, fetched_at)
);
"""


def normalize(text: str) -> str:
    t = unicodedata.normalize("NFKD", text.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    stop = {"que", "pasaria", "si", "te", "tu", "un", "una", "el", "la", "los", "las", "de", "del",
            "a", "al", "en", "y", "o", "ocurriria", "sucederia", "como", "seria", "vida", "hasta", "fueras"}
    return " ".join(w for w in t.split() if w not in stop)


def similarity(a: str, b: str) -> float:
    """Jaccard sobre palabras significativas (0..1)."""
    sa, sb = set(normalize(a).split()), set(normalize(b).split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


class Registry:
    def __init__(self, path: Path | None = None):
        cfg = load_config()
        self.path = path or cfg.path("paths.data") / "registry.sqlite"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)

    # --- vídeos -------------------------------------------------
    def upsert_video(self, slug: str, **fields) -> None:
        fields = {k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
                  for k, v in fields.items()}
        if "idea" in fields:
            fields["idea_norm"] = normalize(fields["idea"])
        exists = self.db.execute("SELECT 1 FROM videos WHERE slug=?", (slug,)).fetchone()
        if exists:
            sets = ", ".join(f"{k}=?" for k in fields)
            self.db.execute(f"UPDATE videos SET {sets} WHERE slug=?", (*fields.values(), slug))
        else:
            fields.setdefault("created_at", time.time())
            cols = ", ".join(["slug", *fields])
            qs = ", ".join("?" * (len(fields) + 1))
            self.db.execute(f"INSERT INTO videos ({cols}) VALUES ({qs})", (slug, *fields.values()))
        self.db.commit()

    def videos(self) -> list[sqlite3.Row]:
        return self.db.execute("SELECT * FROM videos ORDER BY created_at DESC").fetchall()

    def is_duplicate(self, idea: str, threshold: float = 0.6) -> str | None:
        for row in self.videos():
            if similarity(idea, row["idea"]) >= threshold:
                return row["slug"]
        return None

    # --- métricas -----------------------------------------------
    def add_metrics(self, youtube_id: str, m: dict) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO metrics VALUES (?,?,?,?,?,?,?,?,?,?)",
            (youtube_id, time.time(), m.get("views"), m.get("likes"), m.get("comments"), m.get("shares"),
             m.get("averageViewDuration"), m.get("averageViewPercentage"), m.get("subscribersGained"),
             json.dumps(m)))
        self.db.commit()

    def latest_metrics(self) -> list[sqlite3.Row]:
        return self.db.execute("""
            SELECT v.slug, v.title, v.category, v.hook, v.duration_s, m.* FROM videos v
            JOIN metrics m ON m.youtube_id = v.youtube_id
            WHERE m.fetched_at = (SELECT MAX(fetched_at) FROM metrics WHERE youtube_id = v.youtube_id)
        """).fetchall()
