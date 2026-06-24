#!/usr/bin/env python3
"""Build and validate a normalized content catalog used by docs, generated artifacts and webapp."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class JsonTableSpec:
    name: str
    primary_key: str
    unique_columns: tuple[str, ...] | None = None


@dataclass(frozen=True)
class ForeignKeySpec:
    table: str
    column: str
    ref_table: str
    ref_column: str


@dataclass(frozen=True)
class PipelinePaths:
    repo_root: Path
    source_dir: Path
    generated_catalog_json: Path
    generated_catalog_md: Path
    generated_redundancy_md: Path
    webapp_catalog_json: Path


class ContentDbError(RuntimeError):
    """Domain specific validation failure."""


class JsonTable:
    def __init__(
        self,
        name: str,
        primary_key: str,
        rows: list[dict[str, Any]],
        unique_columns: tuple[str, ...] | None = None,
    ) -> None:
        self.name = name
        self.primary_key = primary_key
        self.rows = rows
        self.unique_columns = unique_columns

    def key_set(self) -> set[str]:
        if self.unique_columns:
            return self._composite_key_set()

        keys: set[str] = set()
        for row in self.rows:
            if self.primary_key not in row:
                raise ContentDbError(f"[{self.name}] Missing primary key: {self.primary_key}")
            key_value = str(row[self.primary_key])
            if key_value in keys:
                raise ContentDbError(f"[{self.name}] Duplicate primary key: {key_value}")
            keys.add(key_value)
        return keys

    def _composite_key_set(self) -> set[str]:
        assert self.unique_columns is not None
        keys: set[str] = set()
        for row in self.rows:
            parts: list[str] = []
            for column in self.unique_columns:
                if column not in row:
                    raise ContentDbError(f"[{self.name}] Missing unique column: {column}")
                parts.append(str(row[column]))

            key_value = "::".join(parts)
            if key_value in keys:
                raise ContentDbError(
                    f"[{self.name}] Duplicate composite key ({', '.join(self.unique_columns)}): {key_value}"
                )
            keys.add(key_value)

        return keys


class ContentDatabase:
    TABLES = (
        JsonTableSpec("contexts", "context_id"),
        JsonTableSpec("topics", "topic_id"),
        JsonTableSpec("keywords", "keyword_id"),
        JsonTableSpec("documents", "document_id"),
        JsonTableSpec("tasks", "task_id"),
        JsonTableSpec("solutions", "solution_id"),
        JsonTableSpec("document_topics", "document_id", ("document_id", "topic_id")),
        JsonTableSpec("task_topics", "task_id", ("task_id", "topic_id")),
        JsonTableSpec("topic_keywords", "topic_id", ("topic_id", "keyword_id")),
        JsonTableSpec("task_keywords", "task_id", ("task_id", "keyword_id")),
    )

    FOREIGN_KEYS = (
        ForeignKeySpec("documents", "context_id", "contexts", "context_id"),
        ForeignKeySpec("tasks", "context_id", "contexts", "context_id"),
        ForeignKeySpec("solutions", "task_id", "tasks", "task_id"),
        ForeignKeySpec("document_topics", "document_id", "documents", "document_id"),
        ForeignKeySpec("document_topics", "topic_id", "topics", "topic_id"),
        ForeignKeySpec("task_topics", "task_id", "tasks", "task_id"),
        ForeignKeySpec("task_topics", "topic_id", "topics", "topic_id"),
        ForeignKeySpec("topic_keywords", "topic_id", "topics", "topic_id"),
        ForeignKeySpec("topic_keywords", "keyword_id", "keywords", "keyword_id"),
        ForeignKeySpec("task_keywords", "task_id", "tasks", "task_id"),
        ForeignKeySpec("task_keywords", "keyword_id", "keywords", "keyword_id"),
    )

    def __init__(self, repo_root: Path, source_dir: Path) -> None:
        self.repo_root = repo_root
        self.source_dir = source_dir
        self.tables: dict[str, JsonTable] = {}

    def load(self) -> None:
        for spec in self.TABLES:
            table_path = self.source_dir / f"{spec.name}.json"
            if not table_path.exists():
                raise ContentDbError(f"Missing table file: {table_path}")
            rows = json.loads(table_path.read_text(encoding="utf-8"))
            if not isinstance(rows, list):
                raise ContentDbError(f"[{spec.name}] Table file must contain a JSON array")
            normalized_rows: list[dict[str, Any]] = []
            for row in rows:
                if not isinstance(row, dict):
                    raise ContentDbError(f"[{spec.name}] Every row must be a JSON object")
                normalized_rows.append(row)
            self.tables[spec.name] = JsonTable(
                spec.name,
                spec.primary_key,
                normalized_rows,
                unique_columns=spec.unique_columns,
            )

    def validate(self) -> None:
        if not self.tables:
            self.load()

        key_index: dict[str, set[str]] = {}
        for table in self.tables.values():
            key_index[table.name] = table.key_set()

        for fk in self.FOREIGN_KEYS:
            source = self.tables[fk.table]
            target_keys = key_index[fk.ref_table]
            for row in source.rows:
                if fk.column not in row:
                    raise ContentDbError(f"[{fk.table}] Missing foreign key column: {fk.column}")
                value = str(row[fk.column])
                if value not in target_keys:
                    raise ContentDbError(
                        f"[{fk.table}] Foreign key violation: {fk.column}={value} references missing "
                        f"{fk.ref_table}.{fk.ref_column}"
                    )

        for table in ("documents", "solutions"):
            for row in self.tables[table].rows:
                source_path = Path(str(row.get("source_path", "")))
                if not source_path:
                    raise ContentDbError(f"[{table}] source_path is mandatory")
                if not (self.repo_root / source_path).exists():
                    raise ContentDbError(f"[{table}] source_path does not exist: {source_path}")

    def _rows(self, name: str) -> list[dict[str, Any]]:
        return self.tables[name].rows

    def build_domain_view(self) -> dict[str, Any]:
        contexts = {row["context_id"]: dict(row) for row in self._rows("contexts")}
        topics = {row["topic_id"]: dict(row) for row in self._rows("topics")}
        keywords = {row["keyword_id"]: dict(row) for row in self._rows("keywords")}
        documents = {row["document_id"]: dict(row) for row in self._rows("documents")}
        tasks = {row["task_id"]: dict(row) for row in self._rows("tasks")}

        for context in contexts.values():
            context["documents"] = []
            context["tasks"] = []

        for document in documents.values():
            document["topics"] = []
            context_id = str(document["context_id"])
            contexts[context_id]["documents"].append(document)

        for relation in self._rows("document_topics"):
            document = documents[str(relation["document_id"])]
            topic = topics[str(relation["topic_id"])]
            document["topics"].append(topic)

        for task in tasks.values():
            task["topics"] = []
            task["keywords"] = []
            task["solutions"] = []
            context_id = str(task["context_id"])
            contexts[context_id]["tasks"].append(task)

        for relation in self._rows("task_topics"):
            task = tasks[str(relation["task_id"])]
            topic = topics[str(relation["topic_id"])]
            task["topics"].append(topic)

        for relation in self._rows("task_keywords"):
            task = tasks[str(relation["task_id"])]
            keyword = keywords[str(relation["keyword_id"])]
            task["keywords"].append(keyword)

        solutions_by_task: dict[str, list[dict[str, Any]]] = {}
        for solution in self._rows("solutions"):
            task_id = str(solution["task_id"])
            solutions_by_task.setdefault(task_id, []).append(dict(solution))

        for task_id, solution_rows in solutions_by_task.items():
            tasks[task_id]["solutions"] = solution_rows

        return {
            "contexts": sorted(contexts.values(), key=lambda item: str(item["code"])),
            "topics": sorted(topics.values(), key=lambda item: str(item["code"])),
            "keywords": sorted(keywords.values(), key=lambda item: str(item["label"]).lower()),
        }


class RedundancyAnalyzer:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    @staticmethod
    def _normalize_markdown(content: str) -> str:
        content = re.sub(r"```[\s\S]*?```", "", content)
        content = re.sub(r"`[^`\n]+`", "", content)
        content = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", content)
        content = re.sub(r"\[[^\]]+\]\([^)]*\)", "", content)
        content = re.sub(r"\s+", " ", content).strip().lower()
        return content

    def find_exact_duplicates(self) -> list[dict[str, Any]]:
        candidates = sorted(self.repo_root.glob("docs/handbuch/**/*.md")) + sorted(
            self.repo_root.glob("generated/**/*.md")
        )
        digest_map: dict[str, list[Path]] = {}
        for path in candidates:
            text = path.read_text(encoding="utf-8")
            normalized = self._normalize_markdown(text)
            if len(normalized) < 250:
                continue
            digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
            digest_map.setdefault(digest, []).append(path)

        duplicates: list[dict[str, Any]] = []
        for digest, paths in digest_map.items():
            if len(paths) < 2:
                continue
            duplicates.append(
                {
                    "digest": digest,
                    "paths": [p.relative_to(self.repo_root).as_posix() for p in paths],
                }
            )

        return sorted(duplicates, key=lambda item: len(item["paths"]), reverse=True)


class CatalogArtifactWriter:
    def __init__(self, paths: PipelinePaths) -> None:
        self.paths = paths

    @staticmethod
    def _to_pretty_json(payload: Any) -> str:
        return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    def build_catalog_json(self, domain_view: dict[str, Any], duplicate_groups: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "meta": {
                "schema": "content-db-3nf-v1",
                "managed_by": "scripts/content_db_pipeline.py",
                "generated_artifacts": [
                    "generated/content/learning-catalog.json",
                    "generated/content/learning-catalog.md",
                    "generated/content/redundancy-report.md",
                    "webapp/public/data/learning-content.json",
                ],
            },
            "contexts": domain_view["contexts"],
            "topic_count": len(domain_view["topics"]),
            "keyword_count": len(domain_view["keywords"]),
            "redundancy": {
                "exact_duplicate_groups": duplicate_groups,
                "group_count": len(duplicate_groups),
            },
        }

    def build_markdown_catalog(self, catalog_payload: dict[str, Any]) -> str:
        lines: list[str] = []
        lines.append("# Learning Content Catalog")
        lines.append("")
        lines.append("Diese Datei wird aus der normalisierten JSON-Datenbank unter data/content-db erzeugt.")
        lines.append("")
        lines.append(f"- Kontextanzahl: {len(catalog_payload['contexts'])}")
        lines.append(f"- Themenanzahl: {catalog_payload['topic_count']}")
        lines.append(f"- Stichwortanzahl: {catalog_payload['keyword_count']}")
        lines.append("")

        for context in catalog_payload["contexts"]:
            lines.append(f"## {context['code']}: {context['title']}")
            lines.append("")
            lines.append(f"{context['description']}")
            lines.append("")
            lines.append(f"- Zeithorizont: {context['time_horizon']}")
            lines.append(f"- Dokumente: {len(context['documents'])}")
            lines.append(f"- Aufgaben: {len(context['tasks'])}")
            lines.append("")

            if context["documents"]:
                lines.append("### Dokumente")
                lines.append("")
                for document in context["documents"]:
                    topic_codes = ", ".join(topic["code"] for topic in document["topics"]) or "-"
                    lines.append(
                        f"- {document['title']} ({document['kind']}) -> {document['source_path']} | Themen: {topic_codes}"
                    )
                lines.append("")

            if context["tasks"]:
                lines.append("### Aufgaben und Loesungen")
                lines.append("")
                for task in context["tasks"]:
                    topics = ", ".join(topic["code"] for topic in task["topics"]) or "-"
                    keywords = ", ".join(keyword["label"] for keyword in task["keywords"]) or "-"
                    lines.append(f"- Aufgabe: {task['title']} ({task['difficulty']})")
                    lines.append(f"  - Prompt: {task['prompt']}")
                    lines.append(f"  - Themen: {topics}")
                    lines.append(f"  - Stichworte: {keywords}")
                    for solution in task["solutions"]:
                        lines.append(f"  - Loesung {solution['version']}: {solution['source_path']}")
                lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def build_redundancy_report(duplicate_groups: list[dict[str, Any]]) -> str:
        lines: list[str] = []
        lines.append("# Redundancy Report")
        lines.append("")
        lines.append("Analyse auf inhaltlich exakt gleiche Markdown-Inhalte zwischen docs/handbuch und generated.")
        lines.append("")
        lines.append(f"- Exakte Duplikatgruppen: {len(duplicate_groups)}")
        lines.append("")

        if not duplicate_groups:
            lines.append("Keine exakten Duplikatgruppen erkannt.")
            lines.append("")
            return "\n".join(lines)

        for index, group in enumerate(duplicate_groups, start=1):
            lines.append(f"## Gruppe {index}")
            lines.append("")
            lines.append(f"- Fingerprint: {group['digest']}")
            lines.append("- Dateien:")
            for path in group["paths"]:
                lines.append(f"  - {path}")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def build_webapp_payload(catalog_payload: dict[str, Any]) -> dict[str, Any]:
        learning_paths: list[dict[str, Any]] = []
        practice_cards: list[dict[str, Any]] = []
        interactive_exercises: list[dict[str, Any]] = []

        for context in catalog_payload["contexts"]:
            learning_paths.append(
                {
                    "title": f"{context['code']}: {context['title']}",
                    "focus": context["description"],
                    "steps": [
                        "Kontext lesen und Ziele identifizieren",
                        "Passende Dokumente bearbeiten",
                        "Aufgaben bearbeiten und mit Loesungen spiegeln",
                        "Ergebnisse gegen 3NF- und SQL-Kriterien absichern",
                    ],
                }
            )

            for task in context["tasks"]:
                practice_cards.append(
                    {
                        "title": task["title"],
                        "goal": task["prompt"],
                        "selfCheck": "Sind Kontextbezug, Modellstruktur und SQL-Logik konsistent?",
                        "hint": "Arbeite in kleinen Schritten und begruende jedes Modell- oder Query-Element fachlich.",
                    }
                )
                interactive_exercises.append(
                    {
                        "id": task["task_id"],
                        "title": task["title"],
                        "prompt": task["prompt"],
                        "placeholder": "Schreibe hier deinen Loesungsentwurf...",
                        "checks": [keyword["label"] for keyword in task["keywords"]],
                    }
                )

        return {
            "meta": catalog_payload["meta"],
            "contexts": catalog_payload["contexts"],
            "learningPaths": learning_paths,
            "practiceCards": practice_cards,
            "interactiveExercises": interactive_exercises,
        }

    @staticmethod
    def _write_if_changed(path: Path, content: str, write: bool) -> bool:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        changed = current != content
        if write and changed:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return changed

    def render(self, catalog_payload: dict[str, Any], duplicate_groups: list[dict[str, Any]], write: bool) -> list[str]:
        markdown_catalog = self.build_markdown_catalog(catalog_payload)
        redundancy_report = self.build_redundancy_report(duplicate_groups)
        webapp_payload = self.build_webapp_payload(catalog_payload)

        outputs = {
            self.paths.generated_catalog_json: self._to_pretty_json(catalog_payload),
            self.paths.generated_catalog_md: markdown_catalog,
            self.paths.generated_redundancy_md: redundancy_report,
            self.paths.webapp_catalog_json: self._to_pretty_json(webapp_payload),
        }

        changed_files: list[str] = []
        for output_path, content in outputs.items():
            if self._write_if_changed(output_path, content, write=write):
                changed_files.append(output_path.relative_to(self.paths.repo_root).as_posix())
        return changed_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and build normalized content artifacts.")
    parser.add_argument("--check", action="store_true", help="Check artifacts and fail if out of sync")
    parser.add_argument("--write", action="store_true", help="Write generated artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    write = args.write and not args.check

    repo_root = Path(__file__).resolve().parents[1]
    paths = PipelinePaths(
        repo_root=repo_root,
        source_dir=repo_root / "data/content-db",
        generated_catalog_json=repo_root / "generated/content/learning-catalog.json",
        generated_catalog_md=repo_root / "generated/content/learning-catalog.md",
        generated_redundancy_md=repo_root / "generated/content/redundancy-report.md",
        webapp_catalog_json=repo_root / "webapp/public/data/learning-content.json",
    )

    db = ContentDatabase(repo_root=repo_root, source_dir=paths.source_dir)
    db.load()
    db.validate()

    domain_view = db.build_domain_view()
    duplicates = RedundancyAnalyzer(repo_root).find_exact_duplicates()

    writer = CatalogArtifactWriter(paths)
    catalog_payload = writer.build_catalog_json(domain_view=domain_view, duplicate_groups=duplicates)
    changed_files = writer.render(catalog_payload=catalog_payload, duplicate_groups=duplicates, write=write)

    mode = "WRITE" if write else "CHECK"
    print(f"[content-db] {mode}: contexts={len(domain_view['contexts'])}, duplicates={len(duplicates)}")

    if args.check and changed_files:
        print("[content-db] FAIL: generated artifacts out of sync")
        for file_path in changed_files:
            print(f"[content-db] NEEDS-FIX: {file_path}")
        print("[content-db] HINT: bash scripts/generate-content-catalog.sh")
        return 1

    if changed_files:
        for file_path in changed_files:
            prefix = "FIX" if write else "NEEDS-FIX"
            print(f"[content-db] {prefix}: {file_path}")

    print("[content-db] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
