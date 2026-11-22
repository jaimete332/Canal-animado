"""Capítulos de YouTube para vídeos largos: calcula la marca de tiempo de cada escena listada en
metadata["chapters"] (id de escena -> título) usando output/<slug>/timeline.json, y sustituye {CAPITULOS} en la
descripción de output/<slug>/metadata.json (y en PARA_SUBIR si ya se entregó).

Uso: python3 scripts/chapters.py <slug>
YouTube exige que el primer capítulo empiece en 00:00, al menos 3 capítulos y de 10 s o más cada uno.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def stamp(sec: float) -> str:
    sec = int(sec)
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def build(slug: str) -> str:
    out = ROOT / "output" / slug
    tl = {it["id"]: it["start"] for it in json.loads((out / "timeline.json").read_text())}
    chapters = json.loads((out / "script.json").read_text())["metadata"]["chapters"]
    rows = sorted((tl[k], v) for k, v in chapters.items() if k in tl)
    rows[0] = (0.0, rows[0][1])
    for (a, _), (b, t) in zip(rows, rows[1:]):
        if b - a < 10:
            raise ValueError(f"El capítulo «{t}» empieza a menos de 10 s del anterior")
    return "⏱️ CAPÍTULOS\n" + "\n".join(f"{stamp(t)} {title}" for t, title in rows)


def main(slug: str) -> None:
    text = build(slug)
    targets = [ROOT / "output" / slug / "metadata.json"]
    targets += list((ROOT / "PARA_SUBIR").glob(f"*_{slug}/extra/metadata.json"))
    for f in targets:
        m = json.loads(f.read_text(encoding="utf-8"))
        m["description"] = m["description"].replace("{CAPITULOS}", text)
        f.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1])
