# Routine: Template-Repositories aktuell halten

Diese Routine richtet sich an Lehrkräfte oder Teams, die aus diesem Repository ein eigenes Template-Repository erzeugt haben.

## Ziel

Neue Verbesserungen aus dem Original-Repository regelmäßig als Pull verfügbar machen.

## Automatischer Weg (empfohlen): Sync-PR per GitHub Actions

Im Repository ist ein Workflow vorhanden:

- `.github/workflows/template-sync-pr.yml`

Was dieser Workflow macht:

1. Läuft automatisch jeden Montagmorgen (UTC) und zusätzlich manuell per "Run workflow".
2. Holt Änderungen aus `upstream/main`.
3. Erstellt bei neuen Änderungen automatisch einen Pull Request nach `main`.

### Konfiguration für Template-Nutzer

Setze in deinem abgeleiteten Repository eine Variable unter
`Settings -> Secrets and variables -> Actions -> Variables`:

- `TEMPLATE_UPSTREAM_REPO=ChristineJanischek/edu-code-course-rdb`

Falls die Variable fehlt, nutzt der Workflow diesen Wert als Standard.

### Vorteil

- Updates kommen als prüfbarer PR statt als stiller Direkt-Merge.
- Lehrkräfte können Änderungen didaktisch freigeben, bevor sie live sind.

## Einmalig einrichten

1. In deinem abgeleiteten Repository das Original als zusätzliche Remote-Quelle eintragen:

```bash
git remote add upstream https://github.com/ChristineJanischek/edu-code-course-rdb.git
```

2. Prüfen, ob die Remote vorhanden ist:

```bash
git remote -v
```

## Regelmäßige Sync-Routine

```bash
git fetch upstream
git checkout main
git merge --no-ff upstream/main
git push origin main
```

## Empfehlung für den Unterrichtsbetrieb

- Führe die Sync-Routine mindestens 1x pro Woche aus.
- Führe sie zusätzlich vor Beginn einer neuen Klassenarbeits- oder Übungsphase aus.
- Nach dem Merge kurz prüfen:
  - `generated/informationen/begrifflichkeiten/`
  - `generated/informationen/teil-b/`
  - `generated/informationen/teil-c/`

Hinweis: Wenn der automatische Workflow aktiv ist, dient die manuelle Routine vor allem als Fallback bei Merge-Konflikten.

## Optional: Team-Standard festlegen

Wenn mehrere Personen am Schul-Repository arbeiten, die Routine als festen Termin in den Teamkalender aufnehmen (z. B. Montag 07:30 Uhr).
