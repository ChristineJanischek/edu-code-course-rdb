#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = REPO_ROOT / "uploads" / "lehrplaene"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "generated" / "lehrplaene"

TAG_RULES = {
    "eerm": ["entity relationship", "erm", "eer", "eerm", "entitaet", "beziehung", "kardinal"],
    "normalisierung": ["normalform", "normalisierung", "1. normalform", "2. normalform", "3. normalform", "3nf"],
    "sql-select": ["select", "projektion", "selektion", "abfrage"],
    "sql-from": ["from", "basistabelle", "quelltabelle", "datenquelle"],
    "sql-join": ["join", "left join", "left outer join", "verbund", "verknuepf", "fremdschluessel"],
    "sql-where": ["where", "filter", "bedingung", "vergleich", "like"],
    "sql-group-by": ["group by", "aggregation", "summe", "anzahl", "mittelwert"],
    "sql-having": ["having", "gruppenfilter", "aggregatbedingung"],
    "sql-order-by": ["order by", "sortierung", "aufsteigend", "absteigend", "asc", "desc"],
    "sql-ddl": ["create table", "alter table", "ddl", "schema"],
    "sql-dml": ["insert", "update", "delete", "dml"],
    "begruendung": ["begruenden", "begruendung", "erlaeutern", "bewerten"],
    "datenintegritaet": ["integritaet", "konsistenz", "anomal", "redundanz"],
    "pruefung": ["abitur", "pruefung", "klassenarbeit", "erwartungshorizont"],
}


@dataclass
class CurriculumChunk:
    chunk_id: str
    page_start: int
    page_end: int
    text: str
    tags: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "chunk_id": self.chunk_id,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "text": self.text,
            "tags": self.tags,
        }


def slugify(value: str) -> str:
    lowered = value.lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", lowered)
    return normalized.strip("-") or "curriculum"


def normalize_whitespace(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_pages(pdf_path: Path) -> list[str]:
    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(normalize_whitespace(text))
    return pages


def paragraph_units(pages: Iterable[str]) -> list[tuple[int, str]]:
    units: list[tuple[int, str]] = []
    for page_number, page_text in enumerate(pages, start=1):
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", page_text) if part.strip()]
        for paragraph in paragraphs:
            compact = re.sub(r"\s+", " ", paragraph).strip()
            if len(compact) >= 80:
                units.append((page_number, compact))
    return units


def infer_tags(text: str) -> list[str]:
    lowered = text.lower()
    tags = {tag for tag, keywords in TAG_RULES.items() if any(keyword in lowered for keyword in keywords)}

    # SQL-Klauseln didaktisch konsistent zusammenfassen.
    # SELECT-Kompetenzen implizieren immer die FROM-Komponente.
    if "sql-select" in tags:
        tags.add("sql-from")

    # GROUP BY wird in der Praxis mit HAVING-Logik trainiert (Gruppenfilter).
    if "sql-group-by" in tags:
        tags.add("sql-having")

    if "datenbank" in lowered and "relational" in lowered and "normalisierung" not in tags:
        tags.add("relationale-datenbanken")
    return sorted(tags)


def build_chunks(units: list[tuple[int, str]], max_chars: int = 900) -> list[CurriculumChunk]:
    chunks: list[CurriculumChunk] = []
    current_parts: list[str] = []
    current_pages: list[int] = []

    def flush() -> None:
        if not current_parts:
            return
        text = "\n\n".join(current_parts).strip()
        chunk_number = len(chunks) + 1
        chunks.append(
            CurriculumChunk(
                chunk_id=f"chunk-{chunk_number:03d}",
                page_start=min(current_pages),
                page_end=max(current_pages),
                text=text,
                tags=infer_tags(text),
            )
        )

    for page_number, paragraph in units:
        proposed_length = len("\n\n".join(current_parts + [paragraph]))
        if current_parts and proposed_length > max_chars:
            flush()
            current_parts = []
            current_pages = []
        current_parts.append(paragraph)
        current_pages.append(page_number)

    flush()
    return chunks


def summarize_tags(chunks: list[CurriculumChunk]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for chunk in chunks:
        for tag in chunk.tags:
            counts[tag] = counts.get(tag, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def import_curriculum(pdf_path: Path, output_dir: Path) -> Path:
    pdf_path = pdf_path.resolve()
    pages = extract_pdf_pages(pdf_path)
    units = paragraph_units(pages)
    chunks = build_chunks(units)
    slug = slugify(pdf_path.stem)
    output_dir.mkdir(parents=True, exist_ok=True)

    document_payload = {
        "source_pdf": str(pdf_path.relative_to(REPO_ROOT)),
        "slug": slug,
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "tag_summary": summarize_tags(chunks),
        "chunks": [chunk.to_dict() for chunk in chunks],
    }
    document_path = output_dir / f"{slug}.json"
    document_path.write_text(json.dumps(document_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    index_path = output_dir / "index.json"
    existing_index = {"documents": []}
    if index_path.exists():
        existing_index = json.loads(index_path.read_text(encoding="utf-8"))

    documents = [doc for doc in existing_index.get("documents", []) if doc.get("slug") != slug]
    documents.append(
        {
            "slug": slug,
            "source_pdf": str(pdf_path.relative_to(REPO_ROOT)),
            "document_json": str(document_path.relative_to(REPO_ROOT)),
            "page_count": len(pages),
            "chunk_count": len(chunks),
            "tag_summary": summarize_tags(chunks),
        }
    )
    documents.sort(key=lambda doc: doc["slug"])
    index_path.write_text(json.dumps({"documents": documents}, ensure_ascii=False, indent=2), encoding="utf-8")
    return document_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Importiert Lehrplan-PDFs und erzeugt strukturierte JSON-Artefakte.")
    parser.add_argument("pdf", nargs="?", help="Optionale PDF-Datei. Ohne Angabe werden alle PDFs in uploads/lehrplaene verarbeitet.")
    parser.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR), help="Quellverzeichnis fuer Lehrplan-PDFs")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Zielverzeichnis fuer JSON-Artefakte")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_dir = Path(args.source_dir)
    output_dir = Path(args.output_dir)

    if args.pdf:
        pdf_paths = [Path(args.pdf)]
    else:
        pdf_paths = sorted(source_dir.glob("*.pdf"))

    if not pdf_paths:
        print("[curriculum-import] Keine PDF-Dateien gefunden")
        return 1

    for pdf_path in pdf_paths:
        output_path = import_curriculum(pdf_path, output_dir)
        print(f"[curriculum-import] OK: {pdf_path.name} -> {output_path.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())