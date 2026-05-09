#!/usr/bin/env bash
set -euo pipefail

echo "[ka-language] Starte Sprach- und Transferleistungsvalidierung..."

python3 - <<'PY'
from pathlib import Path
import re
import sys

files = [
    Path("docs/handbuch/templates/KLASSENARBEIT-TEMPLATE-60MIN-34P-BPE6-BPE5.md"),
    Path("generated/klassenarbeiten/KA02_BG12_2025_60min_34P_Muster_EERM_SQL.md"),
]

errors = []

# Haeufige ASCII-Umschriften, die in Aufgabenstellungen als Umlaute erwartet sind.
umlaut_rules = {
    "Entitaeten": "Entitäten",
    "Kardinalitaeten": "Kardinalitäten",
    "Aenderungsanomalie": "Änderungsanomalie",
    "Loeschanomalie": "Löschanomalie",
    "Einfuegeanomalie": "Einfügeanomalie",
    "fuer": "für",
    "ueber": "über",
    "gueltig": "gültig",
    "Schueler": "Schüler",
}

# Formulierungen, die zu viel vorwegnehmen und Transferleistung reduzieren.
transfer_antipatterns = [
    r"^\s*-\s*Entitaeten\s*:",
    r"PK/FK\s+sauber\s+gesetzt",
    r"N:M\s+zwischen\s+.*\s+ueber\s+",
]

for file_path in files:
    if not file_path.exists():
        errors.append(f"Fehlende Datei: {file_path}")
        continue

    raw = file_path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{file_path}: keine gueltige UTF-8-Datei ({exc})")
        continue

    lines = text.splitlines()

    for i, line in enumerate(lines, start=1):
        for bad, good in umlaut_rules.items():
            if re.search(rf"\b{re.escape(bad)}\b", line):
                errors.append(
                    f"{file_path}:{i}: ASCII-Umschrift '{bad}' gefunden, bitte '{good}' verwenden"
                )

        for pat in transfer_antipatterns:
            if re.search(pat, line):
                errors.append(
                    f"{file_path}:{i}: Formulierung nimmt Loesung zu stark vorweg, bitte als Sachverhalt formulieren"
                )

if errors:
    print("[ka-language] FAIL")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)

print("[ka-language] Sprach- und Transferleistungsvalidierung erfolgreich")
PY
