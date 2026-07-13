#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import urllib.request
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATED_ROOT = REPO_ROOT / "generated" / "teacher-ui"
WEBAPP_PLAN_PATH = REPO_ROOT / "webapp" / "public" / "data" / "teacher-ui-module-plan.json"


def load_build_recommendations():
    module_path = REPO_ROOT / "services" / "python-api" / "learning_api" / "recommendations.py"
    spec = importlib.util.spec_from_file_location("teacher_ui_recommendations", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Konnte recommendations.py nicht laden: {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_recommendations


build_recommendations = load_build_recommendations()

REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATED_ROOT = REPO_ROOT / "generated" / "teacher-ui"
WEBAPP_PLAN_PATH = REPO_ROOT / "webapp" / "public" / "data" / "teacher-ui-module-plan.json"
SHARE_TOKEN = '\\"content_type\\",\\"text\\",\\"parts\\",['
ENQUEUE_PATTERN = re.compile(r'window\.__reactRouterContext\.streamController\.enqueue\("((?:[^"\\]|\\.)*)"\);')
PAYLOAD_MESSAGE_PATTERN = re.compile(
    r'"content_type","text","parts",\[\d+\],"((?:[^"\\]|\\.)*)","role","(assistant|user)"'
)


@dataclass(frozen=True)
class ShareMessage:
    role: str
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Importiert eine ChatGPT-Share-Quelle in die Teacher-UI-Analyse- und Reporting-Pipeline."
    )
    parser.add_argument("url", help="ChatGPT-Share-URL")
    parser.add_argument("--batch-id", default="BATCH-CHATGPT-SHARE-001", help="Batch-ID fuer das Teacher-UI-Backlog")
    parser.add_argument("--source-id", default="CHATGPT-SHARE-001", help="Quellen-ID fuer Artefakte und UI-Plan")
    return parser.parse_args()


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Safari/537.36",
            "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_title(html: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE)
    if not match:
        return "ChatGPT Share"
    return unescape(match.group(1)).strip()


def decode_share_string(raw_text: str) -> str:
    decoded = bytes(raw_text, "utf-8").decode("unicode_escape")
    decoded = unescape(decoded)
    if "Ã" in decoded or "â" in decoded:
        try:
            decoded = decoded.encode("latin1").decode("utf-8")
        except UnicodeError:
            pass
    return decoded.replace("\r\n", "\n").replace("\r", "\n").strip()


def extract_messages(html: str) -> list[ShareMessage]:
    payloads = [decode_share_string(raw_payload) for raw_payload in ENQUEUE_PATTERN.findall(html)]
    messages: list[ShareMessage] = []

    for payload in payloads:
        for raw_text, role in PAYLOAD_MESSAGE_PATTERN.findall(payload):
            text = decode_share_string(raw_text)
            if not text or text.startswith("[{") or text.count('"_') > 5:
                continue
            messages.append(ShareMessage(role=role, text=text))

    deduplicated: list[ShareMessage] = []
    seen: set[tuple[str, str]] = set()
    for message in messages:
        key = (message.role, message.text)
        if key in seen:
            continue
        seen.add(key)
        deduplicated.append(message)

    return deduplicated


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_directory(path.parent)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "share"


def build_source_briefing(title: str) -> str:
    return (
        f"Quelle: {title}. "
        "Lehrkraefte sollen paedagogische Ideen, Aenderungswuensche und Funktionsvorschlaege frei per Text oder Sprache erfassen koennen. "
        "Das System soll die Eingaben automatisch sprachlich bereinigen, strukturieren, in Einzelanforderungen zerlegen, Beduerfnisse und Prozesse erkennen, "
        "geeignete Funktionalitaeten ableiten, UI-Bereiche pro Taetigkeit zuordnen, Module fuer Backend und Frontend planen, Meilensteine bestimmen, Tests festlegen "
        "und Wochenberichte mit aktuellem Stand, umgesetzten Modulen und naechsten logischen Schritten erzeugen. "
        "Lehrplaene, Kompetenzziele, Differenzierung, Kursveroeffentlichung, Bewertungsraster, Musterloesungen und KI-Feedback muessen als wiederholbare Prozesskette beruecksichtigt werden."
    )


def load_curriculum_recommendations() -> list[dict[str, object]]:
    index_path = REPO_ROOT / "generated" / "lehrplaene" / "index.json"
    if not index_path.exists():
        return []

    index_payload = json.loads(index_path.read_text(encoding="utf-8"))
    documents = index_payload.get("documents", [])
    if not isinstance(documents, list):
        return []

    recommendations: list[dict[str, object]] = []
    for document in documents:
        if not isinstance(document, dict):
            continue

        doc_recommendations = build_recommendations(document.get("tag_summary", {}))
        recommendations.append(
            {
                "slug": str(document.get("slug", "")),
                "source_pdf": str(document.get("source_pdf", "")),
                "tag_summary": document.get("tag_summary", {}),
                "recommendations": doc_recommendations,
            }
        )

    return recommendations


def build_plan_payload(source_id: str, title: str, url: str, messages: list[ShareMessage]) -> dict[str, object]:
    imported_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    user_turns = [message.text for message in messages if message.role == "user"]
    assistant_turns = [message.text for message in messages if message.role == "assistant"]
    curriculum_recommendations = load_curriculum_recommendations()

    source_summary = {
        "title": title,
        "source_url": url,
        "idea": "Paeadagogische Ideen automatisch in didaktisch tragfaehige digitale Lernmodule uebersetzen.",
        "ausgangspunkt": "Freiform-Ideen und Sprachinput sind vorhanden, aber bisher nicht als durchgaengige Quellkette im Repo angedockt.",
        "ziel": "Eine wiederholbare Teacher-UI- und Kurseditor-Pipeline, die Ideen aufnimmt, analysiert, Module plant, testbar macht und transparent fortschreibt.",
        "philosophie": "Bedarfsgesteuerte Softwareentwicklung: erst den Lehrerprozess verstehen, dann Funktionen pro Taetigkeit kapseln und sichtbar machen.",
    }

    needs = [
        "Freiform- und Spracheingaben ohne Vorstruktur aufnehmen",
        "Ideen in Prozesse, Bedürfnisse und Module zerlegen",
        "Didaktik, Lehrplan und Differenzierung automatisch mitdenken",
        "Backend- und Frontend-Bausteine pro Lehrerprozess planen",
        "Meilensteine, Tests und Wochenberichte aus derselben Quelle ableiten",
        "Lehrkraft als finale Entscheidungstraegerin im Review behalten",
    ]

    modules = [
        {
            "id": "MOD-SRC-001",
            "title": "Share-Quellenimport",
            "process": "Quelle andocken",
            "status": "implemented",
            "goal": "Externe ChatGPT-Share-Quellen reproduzierbar importieren und als Repo-Artefakt sichern.",
            "backend_components": [
                "scripts/import_teacher_ui_share.py",
                "generated/teacher-ui/sources/*.md",
                "generated/teacher-ui/batches/*-input.txt",
            ],
            "frontend_components": [
                "Teacher-UI Modulplan im Informationsfenster",
            ],
            "tests": [
                "Share-URL ist abrufbar",
                "Nach dem Import existieren Quellen-, Plan- und Reportdateien",
            ],
        },
        {
            "id": "MOD-ANL-002",
            "title": "Bedarfs- und Prozessanalyse",
            "process": "Ideen analysieren",
            "status": "implemented",
            "goal": "Aus Rohideen Bedürfnisse, Prozesse, UI-Zuordnung und technische Aufgaben ableiten.",
            "backend_components": [
                "scripts/teacher-ui-intake.sh",
                "scripts/teacher-ui-routing.sh",
                "scripts/teacher-ui-todo.sh",
                "scripts/teacher-ui-context.sh",
            ],
            "frontend_components": [
                "Prozessgruppen im Modulplan",
                "Status- und Testangaben pro Modul",
            ],
            "tests": [
                "Intake erzeugt strukturierte Anforderungen",
                "Routing ordnet Prozesse und UI-Hauptbereiche zu",
                "To-do-Datei enthaelt Testschritte",
            ],
        },
        {
            "id": "MOD-DID-003",
            "title": "Didaktik- und Lehrplan-Mapping",
            "process": "Unterricht planen",
            "status": "implemented",
            "goal": "Kompetenzziele, Differenzierung, Altersstufe und Lehrplanhinweise aus der Quelle auf Kursbausteine mappen.",
            "backend_components": [
                "Curriculum-Service mit Tagging und Empfehlungen",
                "Mapping-Regeln fuer Kompetenzziele",
                "Lehrplanindex aus generated/lehrplaene/index.json",
            ],
            "frontend_components": [
                "Planungskarte mit Lehrplan- und Kompetenzhinweisen",
                "Kontext-Hinweise im Kurseditor",
                "Curriculum-Empfehlungen im Strategiepanel",
            ],
            "tests": [
                "Lehrplanhinweise erscheinen pro Modulkontext",
                "Empfehlungen sind pro Curriculum-Dokument nachvollziehbar",
                "Curriculum-Empfehlungen werden im Web-Frontend gerendert",
            ],
        },
        {
            "id": "MOD-GEN-004",
            "title": "Unterrichtsmodul-Generator",
            "process": "Module generieren",
            "status": "planned",
            "goal": "Aus validierten Anforderungen Kursmodule, Aufgaben, Bewertungsraster und Lernhilfen zusammenstellen.",
            "backend_components": [
                "Generator fuer Materialpakete und Bewertungsraster",
                "Versionsierte Moduldefinitionen",
            ],
            "frontend_components": [
                "Modul-Composer pro Arbeitsprozess",
                "Vorschau fuer Aufgaben, Hinweise und Veroeffentlichung",
            ],
            "tests": [
                "Jedes Modul hat Aufgabe, Hilfe, Bewertung und Publikationsstatus",
                "Fehlende Daten brechen die Vorschau nicht",
            ],
        },
        {
            "id": "MOD-OPS-005",
            "title": "Milestone- und Testorchestrierung",
            "process": "Qualitaet sichern",
            "status": "implemented",
            "goal": "Naechste Meilensteine, Regressionstests und Qualitaets-Gates automatisch fortschreiben.",
            "backend_components": [
                "scripts/weiter.sh",
                "scripts/teacher-ui-milestone.sh",
            ],
            "frontend_components": [
                "Milestone- und Testlisten im Modulplan",
            ],
            "tests": [
                "Weiter-Report wird aktualisiert",
                "Milestone-Datei verweist auf Regressionstestpfad",
            ],
        },
        {
            "id": "MOD-REP-006",
            "title": "Wochenbericht-Automat",
            "process": "Transparenz herstellen",
            "status": "implemented",
            "goal": "Aktuellen Stand, umgesetzte Module und naechste Schritte als wiederholbaren Wochenbericht ausgeben.",
            "backend_components": [
                "generated/teacher-ui/reports/*.md",
                "webapp/public/data/teacher-ui-module-plan.json",
            ],
            "frontend_components": [
                "Wochenberichtskarte im Informationsfenster",
            ],
            "tests": [
                "Bericht nennt Stand, umgesetzte Module und naechste Schritte",
                "Bericht bleibt auch ohne externe Quelle konsistent lesbar",
            ],
        },
    ]

    milestones = [
        {
            "id": "MS-01",
            "title": "Quelle ingestieren und strukturieren",
            "status": "done",
            "tests": ["Share-Import", "Intake", "Routing", "To-do"],
        },
        {
            "id": "MS-02",
            "title": "Strategieplan im UI sichtbar machen",
            "status": "done",
            "tests": ["Repository-Load", "PHP-Rendering", "CSS-Sichtbarkeit"],
        },
        {
            "id": "MS-03",
            "title": "Didaktisches Mapping und Modulgenerator vertiefen",
            "status": "next",
            "tests": ["Curriculum-Mapping", "Modul-Vorschau", "Fallback-Pfade"],
        },
    ]

    weekly_report = {
        "headline": "Wochenbericht Teacher-UI Strategieimport",
        "current_state": "Die externe Strategiequelle ist nun als Artefakt importiert, analysiert und in einen sichtbaren Modulplan fuer die Webapp ueberfuehrt.",
        "implemented_modules": [module["title"] for module in modules if module["status"] == "implemented"],
        "next_steps": [
            "Modul-Generator fuer Aufgaben, Bewertungsraster und Publikation konkretisieren",
            "Curriculum-Mapping von Empfehlungen auf konkrete Modulvorlagen verfeinern",
            "Wochenberichte optional zeitgesteuert aus demselben Datenmodell erzeugen",
        ],
        "source_findings": {
            "user_turns": user_turns[:6],
            "assistant_turns": assistant_turns[:6],
        },
    }

    return {
        "meta": {
            "managed_by": "scripts/import_teacher_ui_share.py",
            "source_connected": True,
            "imported_at": imported_at,
            "source_id": source_id,
            "message_count": len(messages),
            "title": title,
        },
        "source": source_summary,
        "needs": needs,
        "curriculum_recommendations": curriculum_recommendations,
        "modules": modules,
        "milestones": milestones,
        "weekly_report": weekly_report,
    }


def render_source_markdown(title: str, url: str, messages: list[ShareMessage]) -> str:
    lines = [f"# Quellenimport: {title}", "", f"Quelle: {url}", ""]
    lines.append("## Extrahierte Konversation")
    lines.append("")
    for index, message in enumerate(messages, start=1):
        role_title = "Nutzer" if message.role == "user" else "Assistent"
        lines.append(f"### {index}. {role_title}")
        lines.append("")
        lines.append(message.text)
        lines.append("")
    return "\n".join(lines)


def render_plan_markdown(plan: dict[str, object]) -> str:
    source = dict(plan.get("source", {}))
    modules = [entry for entry in plan.get("modules", []) if isinstance(entry, dict)]
    milestones = [entry for entry in plan.get("milestones", []) if isinstance(entry, dict)]
    weekly_report = dict(plan.get("weekly_report", {}))
    needs = [entry for entry in plan.get("needs", []) if isinstance(entry, str)]

    lines = [f"# Strategieplan: {source.get('title', 'Teacher-UI Quelle')}", ""]
    lines.append("## Kernbild")
    lines.append("")
    lines.append(f"- Idee: {source.get('idea', '-')}")
    lines.append(f"- Ausgangspunkt: {source.get('ausgangspunkt', '-')}")
    lines.append(f"- Ziel: {source.get('ziel', '-')}")
    lines.append(f"- Philosophie: {source.get('philosophie', '-')}")
    lines.append("")
    lines.append("## Erkannte Bedürfnisse")
    lines.append("")
    for need in needs:
        lines.append(f"- {need}")
    lines.append("")
    lines.append("## Module")
    lines.append("")
    for module in modules:
        lines.append(f"### {module.get('id', 'MOD')}: {module.get('title', 'Unbenannt')}")
        lines.append("")
        lines.append(f"- Prozess: {module.get('process', '-')}")
        lines.append(f"- Status: {module.get('status', '-')}")
        lines.append(f"- Ziel: {module.get('goal', '-')}")
        backend_components = module.get("backend_components", [])
        frontend_components = module.get("frontend_components", [])
        tests = module.get("tests", [])
        if isinstance(backend_components, list):
            for item in backend_components:
                lines.append(f"- Backend: {item}")
        if isinstance(frontend_components, list):
            for item in frontend_components:
                lines.append(f"- Frontend: {item}")
        if isinstance(tests, list):
            for item in tests:
                lines.append(f"- Test: {item}")
        lines.append("")
    lines.append("## Meilensteine")
    lines.append("")
    for milestone in milestones:
        lines.append(f"- {milestone.get('id', 'MS')}: {milestone.get('title', '-') } ({milestone.get('status', '-')})")
    lines.append("")
    lines.append("## Wochenbericht")
    lines.append("")
    lines.append(f"- Stand: {weekly_report.get('current_state', '-')}")
    for item in weekly_report.get("implemented_modules", []):
        lines.append(f"- Umgesetzt: {item}")
    for item in weekly_report.get("next_steps", []):
        lines.append(f"- Naechster Schritt: {item}")
    lines.append("")
    return "\n".join(lines)


def render_weekly_report(plan: dict[str, object], next_milestone: str) -> str:
    source = dict(plan.get("source", {}))
    weekly_report = dict(plan.get("weekly_report", {}))
    implemented = weekly_report.get("implemented_modules", [])
    next_steps = weekly_report.get("next_steps", [])

    lines = ["# Wochenbericht Teacher-UI", ""]
    lines.append(f"## Quelle\n\n- {source.get('title', '-')}")
    lines.append(f"- URL: {source.get('source_url', '-')}")
    lines.append("")
    lines.append("## Aktueller Stand\n")
    lines.append(f"- {weekly_report.get('current_state', '-')}")
    lines.append(f"- Nächster Milestone laut Repo: {next_milestone}")
    lines.append("")
    lines.append("## Umgesetzte Funktionalitäten\n")
    if isinstance(implemented, list):
        for item in implemented:
            lines.append(f"- {item}")
    lines.append("")
    lines.append("## Nächste logische Schritte\n")
    if isinstance(next_steps, list):
        for item in next_steps:
            lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def extract_next_milestone(report_path: Path) -> str:
    if not report_path.exists():
        return "Kein Report vorhanden"
    text = report_path.read_text(encoding="utf-8")
    match = re.search(r"## Naechster Milestone\s*\n\s*(.+)", text, flags=re.MULTILINE)
    if not match:
        return "Kein Milestone erkannt"
    return match.group(1).strip()


def run_command(arguments: list[str]) -> None:
    subprocess.run(arguments, cwd=REPO_ROOT, check=True)


def main() -> int:
    args = parse_args()
    html = fetch_text(args.url)
    title = extract_title(html)
    messages = extract_messages(html)
    if not messages:
        raise SystemExit("[share-import] Keine verwertbaren Nachrichten in der Share-Quelle gefunden")

    source_slug = slugify(args.source_id)
    source_dir = GENERATED_ROOT / "sources"
    report_dir = GENERATED_ROOT / "reports"
    analysis_dir = GENERATED_ROOT / "analysen"
    batch_input_path = GENERATED_ROOT / "batches" / f"{args.batch_id}-input.txt"
    source_markdown_path = source_dir / f"{source_slug}.md"
    strategy_markdown_path = analysis_dir / f"{source_slug}-strategie.md"
    weekly_report_path = report_dir / f"wochenbericht-{source_slug}.md"

    write_text(source_markdown_path, render_source_markdown(title, args.url, messages))
    write_text(batch_input_path, build_source_briefing(title))

    run_command(["bash", "scripts/teacher-ui-batch.sh", args.batch_id])

    intake_path = GENERATED_ROOT / "intake" / f"{args.source_id}-structured.md"
    routing_path = GENERATED_ROOT / "routing" / f"{args.source_id}-routing.md"
    todo_path = GENERATED_ROOT / "todos" / f"{args.source_id}-todo.md"
    context_path = GENERATED_ROOT / "context" / f"{args.source_id}-context.md"
    milestone_path = GENERATED_ROOT / "milestones" / f"{args.source_id}-milestone.md"

    run_command([
        "bash",
        "scripts/teacher-ui-intake.sh",
        "--id",
        args.source_id,
        "--input",
        str(batch_input_path),
        "--output",
        str(intake_path),
    ])
    run_command([
        "bash",
        "scripts/teacher-ui-routing.sh",
        "--id",
        args.source_id,
        "--input",
        str(intake_path),
        "--output",
        str(routing_path),
    ])
    run_command([
        "bash",
        "scripts/teacher-ui-todo.sh",
        "--id",
        args.source_id,
        "--input",
        str(routing_path),
        "--output",
        str(todo_path),
    ])
    run_command([
        "bash",
        "scripts/teacher-ui-context.sh",
        "--id",
        args.source_id,
        "--routing",
        str(routing_path),
        "--todo",
        str(todo_path),
        "--output",
        str(context_path),
    ])
    run_command([
        "bash",
        "scripts/teacher-ui-milestone.sh",
        "--id",
        args.source_id,
        "--output",
        str(milestone_path),
    ])

    plan = build_plan_payload(args.source_id, title, args.url, messages)
    write_text(strategy_markdown_path, render_plan_markdown(plan))

    ensure_directory(WEBAPP_PLAN_PATH.parent)
    WEBAPP_PLAN_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    next_milestone = extract_next_milestone(REPO_ROOT / "generated" / "weiter-status.md")
    write_text(weekly_report_path, render_weekly_report(plan, next_milestone))

    print(f"[share-import] OK: Quelle importiert: {args.url}")
    print(f"[share-import] OK: Quellenartefakt: {source_markdown_path.relative_to(REPO_ROOT)}")
    print(f"[share-import] OK: Modulplan: {WEBAPP_PLAN_PATH.relative_to(REPO_ROOT)}")
    print(f"[share-import] OK: Wochenbericht: {weekly_report_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())