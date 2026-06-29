#!/usr/bin/env python3
"""Synchronize generated HTML documentation with its Markdown sources."""

from __future__ import annotations

import argparse
import html
import os
import re
from pathlib import Path

import markdown


LINK_RE = re.compile(r'(?P<attr>href|src)="(?P<target>[^"]+)"', re.IGNORECASE)
PLAN_PATH = Path("generated/anleitungen/stoffverlaufsplan_rdb_3wochen.html")
STYLESHEET_PATH = Path("generated/assets/generated-docs.css")
SQL_RUNTIME_TAG = '<script type="module" src="/js/sql-practice-runtime.mjs"></script>'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synchronize generated HTML documentation.")
    parser.add_argument("--check", action="store_true", help="Check only, do not write files")
    parser.add_argument("--write", action="store_true", help="Write synchronized HTML files")
    return parser.parse_args()


def collect_markdown_files(repo_root: Path) -> list[Path]:
    return sorted(path for path in repo_root.glob("generated/**/*.md") if path.is_file())


def is_external_target(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith(("http://", "https://", "mailto:", "data:", "javascript:")) or target.startswith("#")


def split_fragment(target: str) -> tuple[str, str]:
    if "#" in target:
        path, fragment = target.split("#", 1)
        return path, fragment
    return target, ""


def extract_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback


def render_markdown(markdown_text: str) -> str:
    return markdown.markdown(markdown_text, extensions=["extra", "tables", "fenced_code", "sane_lists"])


def rewrite_local_links(html_text: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        attr = match.group("attr")
        target = match.group("target")

        if is_external_target(target):
            return match.group(0)

        target_path, fragment = split_fragment(target)
        if not target_path.lower().endswith(".md"):
            return match.group(0)

        rewritten = Path(target_path).with_suffix(".html").as_posix()
        if fragment:
            rewritten = f"{rewritten}#{fragment}"
        return f'{attr}="{rewritten}"'

    return LINK_RE.sub(_replace, html_text)
def rewrite_plan_links(html_text: str) -> str:
    """Rewrite local .md links inside the HTML stoffverlaufsplan to .html.

    The plan itself is HTML, but its local links should stay HTML-only so the
    lesson flow never points back to Markdown sources.
    """

    def _replace(match: re.Match[str]) -> str:
        attr = match.group("attr")
        target = match.group("target")

        if is_external_target(target):
            return match.group(0)

        target_path, fragment = split_fragment(target)
        if not target_path.lower().endswith(".md"):
            return match.group(0)

        rewritten = Path(target_path).with_suffix(".html").as_posix()
        if fragment:
            rewritten = f"{rewritten}#{fragment}"
        return f'{attr}="{rewritten}"'

    return LINK_RE.sub(_replace, html_text)


def wrap_html_document(title: str, source_path: Path, body_html: str, stylesheet_href: str) -> str:
    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title, quote=True)}</title>
  <link rel="stylesheet" href="{html.escape(stylesheet_href, quote=True)}">
</head>
<body>
  <div class="page">
    <header class="hero">
      <h1>{html.escape(title)}</h1>
      <p>Automatisch aus der zugehörigen Markdown-Quelle erzeugte HTML-Fassung.</p>
      <p>Quelle: {html.escape(source_path.as_posix())}</p>
    </header>
    <main class="content">
{body_html}
    </main>
  </div>
</body>
</html>
"""


def should_inject_sql_runtime(md_file: Path, markdown_text: str) -> bool:
    md_path = md_file.as_posix()
    if re.search(r"generated/klassenarbeiten/KA\d+_.*_aufg\.md$", md_path, re.IGNORECASE):
        return True
    if re.search(r"generated/uebungen/UE\d+_.*_sql_abfragen\.md$", md_path, re.IGNORECASE):
        return True

    lowered = markdown_text.lower()
    return "teil c" in lowered and "sql" in lowered and "aufgabe 4." in lowered


def inject_sql_runtime_tag(html_text: str) -> str:
    if SQL_RUNTIME_TAG in html_text:
        return html_text

    if "</body>" in html_text:
        return html_text.replace("</body>", f"{SQL_RUNTIME_TAG}\n</body>")

    return html_text + "\n" + SQL_RUNTIME_TAG + "\n"


def render_file(md_file: Path, write: bool, repo_root: Path) -> tuple[bool, Path]:
    markdown_text = md_file.read_text(encoding="utf-8")
    html_file = md_file.with_suffix(".html")
    title = extract_title(markdown_text, md_file.stem)
    body_html = render_markdown(markdown_text)
    body_html = rewrite_local_links(body_html)
    stylesheet_href = Path(os.path.relpath((repo_root / STYLESHEET_PATH).resolve(), md_file.parent.resolve())).as_posix()
    generated_html = wrap_html_document(title, md_file, body_html, stylesheet_href)
    if should_inject_sql_runtime(md_file, markdown_text):
        generated_html = inject_sql_runtime_tag(generated_html)
    current_html = html_file.read_text(encoding="utf-8") if html_file.exists() else None
    changed = current_html != generated_html
    if write and changed:
        html_file.write_text(generated_html, encoding="utf-8")
    return changed, html_file


def main() -> int:
    args = parse_args()
    write = args.write and not args.check
    repo_root = Path(".").resolve()
    markdown_files = collect_markdown_files(repo_root)
    plan_file = repo_root / PLAN_PATH

    needs_update: list[Path] = []
    for md_file in markdown_files:
        changed, html_file = render_file(md_file, write=write, repo_root=repo_root)
        if changed:
            needs_update.append(html_file)
            prefix = "FIX" if write else "NEEDS-FIX"
            print(f"[html-sync] {prefix}: {md_file.relative_to(repo_root)} -> {html_file.relative_to(repo_root)}")

    if plan_file.exists():
        plan_original = plan_file.read_text(encoding="utf-8")
        plan_rewritten = rewrite_plan_links(plan_original)
        if plan_rewritten != plan_original:
            needs_update.append(plan_file)
            if write:
                plan_file.write_text(plan_rewritten, encoding="utf-8")
            prefix = "FIX" if write else "NEEDS-FIX"
            print(f"[html-sync] {prefix}: {plan_file.relative_to(repo_root)}")

    if args.check and needs_update:
        print("[html-sync] FAIL: generated HTML documentation is not synchronized")
        print("[html-sync] HINT: bash scripts/sync-generated-html.sh")
        return 1

    print(f"[html-sync] OK: {len(markdown_files)} Markdown-Dateien geprüft")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())