#!/usr/bin/env python3
"""Inject SQL practice runtime into generated UE and KA HTML pages."""

from __future__ import annotations

import argparse
from pathlib import Path

SCRIPT_TAG = '<script type="module" src="/js/sql-practice-runtime.mjs"></script>'
TARGET_GLOBS = (
    "generated/uebungen/UE*_sql_abfragen.html",
    "generated/klassenarbeiten/KA*_aufg.html",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inject SQL runtime script in generated pages")
    parser.add_argument("--check", action="store_true", help="Check only, do not modify files")
    parser.add_argument("--write", action="store_true", help="Write missing script tags")
    return parser.parse_args()


def collect_targets(repo_root: Path) -> list[Path]:
    targets: list[Path] = []
    for pattern in TARGET_GLOBS:
        targets.extend(sorted(repo_root.glob(pattern)))
    return targets


def has_sql_box_or_part_c(html: str) -> bool:
    lowered = html.lower()
    return "sql-input" in lowered or "teil c" in lowered or "aufgabe 4." in lowered


def inject_script(html: str) -> str:
    if SCRIPT_TAG in html:
        return html

    if "</body>" in html:
        return html.replace("</body>", f"{SCRIPT_TAG}\n</body>")

    return html + "\n" + SCRIPT_TAG + "\n"


def main() -> int:
    args = parse_args()
    write = args.write and not args.check

    repo_root = Path(".").resolve()
    targets = collect_targets(repo_root)
    needs_update: list[Path] = []

    for target in targets:
        current = target.read_text(encoding="utf-8")
        if not has_sql_box_or_part_c(current):
            continue

        updated = inject_script(current)
        if updated == current:
            continue

        needs_update.append(target)
        label = "FIX" if write else "NEEDS-FIX"
        print(f"[sql-practice] {label}: {target.relative_to(repo_root)}")

        if write:
            target.write_text(updated, encoding="utf-8")

    if args.check and needs_update:
        print("[sql-practice] FAIL: SQL practice runtime is not injected in all required pages")
        print("[sql-practice] HINT: bash scripts/augment-sql-practice-pages.sh")
        return 1

    print(f"[sql-practice] OK: {len(targets)} Dateien geprueft")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
