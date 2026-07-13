#!/usr/bin/env python3
"""Erzeugt Unterrichtsmodul-Definitionen aus dem Teacher-UI-Strategieplan,
der Content-DB und den Curriculum-Empfehlungen.

MOD-GEN-004 – Unterrichtsmodul-Generator.

Ausgaben:
  webapp/public/data/teaching-modules.json
  generated/teacher-ui/modules/MODULE-*.md
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT_DB = REPO_ROOT / "data" / "content-db"
PLAN_PATH = REPO_ROOT / "webapp" / "public" / "data" / "teacher-ui-module-plan.json"
MODULES_JSON_PATH = REPO_ROOT / "webapp" / "public" / "data" / "teaching-modules.json"
MODULES_MD_DIR = REPO_ROOT / "generated" / "teacher-ui" / "modules"

DIFFICULTY_ORDER = {"einfach": 0, "mittel": 1, "hoch": 2}


@dataclass
class TaskEntry:
    task_id: str
    context_id: str
    title: str
    prompt: str
    difficulty: str


@dataclass
class TeachingModule:
    module_id: str
    title: str
    context_id: str
    context_title: str
    learning_goals: list[str]
    tasks: list[dict[str, Any]]
    evaluation_criteria: list[str]
    hints: list[str]
    publication_status: str = "draft"
    tags: list[str] = field(default_factory=list)


def load_json(path: Path) -> Any:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def build_learning_goals(context_id: str, curriculum_recs: list[dict[str, Any]]) -> list[str]:
    """Leitet Lernziele aus Curriculum-Empfehlungen und Kontext ab."""
    tag_goals: dict[str, str] = {
        "eerm": "Entitäten, Attribute und Beziehungen aus dem Sachverhalt ableiten und Kardinalitäten begründen.",
        "normalisierung": "Tabellenmodelle bis zur 3. Normalform überführen und Abhängigkeiten dokumentieren.",
        "datenintegritaet": "Datenintegritätsbedingungen benennen und Anomalien bei Verstößen erläutern.",
        "sql-select": "Einfache SELECT-Abfragen mit Projektion und Selektion formulieren und begründen.",
        "sql-join": "Tabellen über Fremdschlüssel per JOIN verbinden und Ergebnismengen fachlich interpretieren.",
        "sql-group-by": "Aggregation und Gruppierung mit GROUP BY / HAVING auf reale Fragestellungen anwenden.",
        "sql-where": "Filterbedingungen in WHERE korrekt formulieren und von HAVING abgrenzen.",
        "sql-order-by": "Abfrageergebnisse mit ORDER BY sinnvoll sortieren und Sortierrichtung begründen.",
        "begruendung": "Fachliche Entscheidungen schriftlich begründen und Alternativlösungen bewerten.",
    }

    goals: list[str] = []
    all_tags: set[str] = set()

    for rec_entry in curriculum_recs:
        if not isinstance(rec_entry, dict):
            continue
        for tag in rec_entry.get("tag_summary", {}).keys():
            all_tags.add(tag)

    context_tag_map = {
        "ctx_eerm_modelling": ["eerm", "normalisierung", "datenintegritaet", "begruendung"],
        "ctx_sql_queries": ["sql-select", "sql-join", "sql-group-by", "sql-where", "sql-order-by", "begruendung"],
        "ctx_exam_assets": ["eerm", "sql-select", "sql-join", "begruendung"],
    }

    relevant_tags = context_tag_map.get(context_id, list(all_tags))
    for tag in relevant_tags:
        if tag in tag_goals and tag in all_tags:
            goal = tag_goals[tag]
            if goal not in goals:
                goals.append(goal)

    return goals or ["Grundlegende Konzepte des Kontexts durchdringen und fachlich korrekt anwenden."]


def build_evaluation_criteria(tasks: list[TaskEntry]) -> list[str]:
    criteria = [
        "Fachsprache wird korrekt und präzise verwendet.",
        "Modell- oder Abfrageentscheidungen werden schriftlich begründet.",
        "Ergebnisse sind fachlich vollständig und ohne Redundanz.",
    ]
    has_hard = any(t.difficulty == "hoch" for t in tasks)
    if has_hard:
        criteria.append("Komplexe Abhängigkeiten und Randfälle werden erkannt und behandelt.")
    return criteria


def build_hints(context_id: str) -> list[str]:
    hint_map: dict[str, list[str]] = {
        "ctx_eerm_modelling": [
            "Beginne mit den Entitätstypen – was sind die zentralen Fachgegenstände?",
            "Prüfe jede Beziehung mit einem Einmal-Satz (z. B. 'Ein Kunde hat mehrere Buchungen').",
            "3NF: Gibt es Attribute, die nur transitiv vom Primärschlüssel abhängen?",
        ],
        "ctx_sql_queries": [
            "Starte mit SELECT und FROM – welche Spalten und Tabellen braucht die Aufgabe?",
            "JOIN nur dann, wenn Daten aus mehr als einer Tabelle benötigt werden.",
            "GROUP BY-Spalten müssen in SELECT erscheinen oder aggregiert sein.",
        ],
        "ctx_exam_assets": [
            "Lies die Aufgabenstellung vollständig, bevor du mit der Lösung beginnst.",
            "Skizziere das Modell oder die Abfragestruktur zuerst auf Papier.",
        ],
    }
    return hint_map.get(context_id, ["Lies die Anforderung genau und arbeite schrittweise."])


def generate_modules(
    tasks_raw: list[dict[str, Any]],
    contexts_raw: list[dict[str, Any]],
    curriculum_recs: list[dict[str, Any]],
) -> list[TeachingModule]:
    tasks_by_context: dict[str, list[TaskEntry]] = {}
    for raw in tasks_raw:
        entry = TaskEntry(
            task_id=str(raw.get("task_id", "")),
            context_id=str(raw.get("context_id", "")),
            title=str(raw.get("title", "")),
            prompt=str(raw.get("prompt", "")),
            difficulty=str(raw.get("difficulty", "mittel")),
        )
        tasks_by_context.setdefault(entry.context_id, []).append(entry)

    context_map = {c["context_id"]: c for c in contexts_raw if isinstance(c, dict)}

    modules: list[TeachingModule] = []
    module_counter = 1

    for context_id, task_entries in tasks_by_context.items():
        ctx = context_map.get(context_id)
        if not ctx:
            continue

        ctx_code = str(ctx.get("code", ""))
        if ctx_code in ("", "CTX-GOV"):
            continue

        sorted_tasks = sorted(
            task_entries,
            key=lambda t: DIFFICULTY_ORDER.get(t.difficulty, 1),
        )

        task_defs = [
            {
                "task_id": t.task_id,
                "title": t.title,
                "prompt": t.prompt,
                "difficulty": t.difficulty,
            }
            for t in sorted_tasks
        ]

        module = TeachingModule(
            module_id=f"MODULE-{module_counter:03d}",
            title=f"Lernmodul: {ctx['title']}",
            context_id=context_id,
            context_title=str(ctx.get("title", "")),
            learning_goals=build_learning_goals(context_id, curriculum_recs),
            tasks=task_defs,
            evaluation_criteria=build_evaluation_criteria(sorted_tasks),
            hints=build_hints(context_id),
            publication_status="draft",
            tags=[str(ctx.get("code", ""))],
        )
        modules.append(module)
        module_counter += 1

    return modules


def to_dict(module: TeachingModule) -> dict[str, Any]:
    return {
        "module_id": module.module_id,
        "title": module.title,
        "context_id": module.context_id,
        "context_title": module.context_title,
        "learning_goals": module.learning_goals,
        "tasks": module.tasks,
        "evaluation_criteria": module.evaluation_criteria,
        "hints": module.hints,
        "publication_status": module.publication_status,
        "tags": module.tags,
    }


def render_markdown(module: TeachingModule, generated_at: str) -> str:
    lines = [
        f"# {module.module_id}: {module.title}",
        "",
        f"Generiert am (UTC): {generated_at}",
        f"Kontext: {module.context_id}",
        f"Status: {module.publication_status}",
        "",
        "## Lernziele",
        "",
    ]
    for goal in module.learning_goals:
        lines.append(f"- {goal}")
    lines.append("")
    lines.append("## Aufgaben")
    lines.append("")
    for task in module.tasks:
        lines.append(f"### {task['title']} ({task['difficulty']})")
        lines.append("")
        lines.append(task["prompt"])
        lines.append("")
    lines.append("## Bewertungskriterien")
    lines.append("")
    for criterion in module.evaluation_criteria:
        lines.append(f"- {criterion}")
    lines.append("")
    lines.append("## Lernhilfen")
    lines.append("")
    for hint in module.hints:
        lines.append(f"- {hint}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    tasks_raw = load_json(CONTENT_DB / "tasks.json")
    contexts_raw = load_json(CONTENT_DB / "contexts.json")
    plan = load_json(PLAN_PATH)
    curriculum_recs = [entry for entry in plan.get("curriculum_recommendations", []) if isinstance(entry, dict)]

    modules = generate_modules(tasks_raw, contexts_raw, curriculum_recs)

    MODULES_MD_DIR.mkdir(parents=True, exist_ok=True)
    for module in modules:
        md_path = MODULES_MD_DIR / f"{module.module_id}.md"
        md_path.write_text(render_markdown(module, generated_at), encoding="utf-8")
        print(f"[module-gen] OK: {md_path.relative_to(REPO_ROOT)}")

    payload: dict[str, Any] = {
        "meta": {
            "managed_by": "scripts/generate_teaching_module.py",
            "generated_at": generated_at,
            "module_count": len(modules),
        },
        "modules": [to_dict(m) for m in modules],
    }

    MODULES_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODULES_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[module-gen] OK: {MODULES_JSON_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
