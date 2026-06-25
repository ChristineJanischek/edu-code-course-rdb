# Routine: Template-Repositories aktuell halten

Diese Routine richtet sich an Lehrkräfte oder Teams, die aus diesem Repository ein eigenes Template-Repository erzeugt haben.

Für Lernende mit eigenem Arbeitsrepo gibt es eine Kurzroutine unter:
[generated/anleitungen/template-sync-fuer-schueler.md](../../anleitungen/template-sync-fuer-schueler.md)

## Ziel

Neue Verbesserungen aus dem Original-Repository regelmäßig als Pull verfügbar machen.

Wichtig: Template-Repositories sollen nicht nur einzelne Dateien oder Teilbereiche übernehmen, sondern den vollständigen Stand von `upstream/main` als Ganzes mergen.

## Automatischer Weg (empfohlen): Sync-PR per GitHub Actions

Im Repository ist ein Workflow vorhanden:

- `.github/workflows/template-sync-pr.yml`

Was dieser Workflow macht:

1. Läuft automatisch jeden Montagmorgen (UTC) und zusätzlich manuell per "Run workflow".
2. Holt Änderungen aus `upstream/main`.
3. Führt einen Voll-Repo-Merge von `upstream/main` in das eigene `main` durch.
4. Pusht das Ergebnis direkt nach `main` oder erstellt bei Branch-Schutzregeln einen Sync-Pull-Request.

### Konfiguration für Template-Nutzer

Setze in deinem abgeleiteten Repository eine Variable unter
`Settings -> Secrets and variables -> Actions -> Variables`:

- `TEMPLATE_UPSTREAM_REPO=ChristineJanischek/edu-code-course-rdb`

Falls die Variable fehlt, nutzt der Workflow diesen Wert als Standard.

### Vorteil

- Updates kommen als prüfbarer PR statt als stiller Direkt-Merge.
- Lehrkräfte können Änderungen didaktisch freigeben, bevor sie live sind.
- Der komplette Repository-Stand bleibt konsistent, auch wenn sich Struktur, Skripte, Doku und Webapp gleichzeitig geändert haben.

## Admin-Checkliste für Template-Repositories

1. Sicherstellen, dass das Template-Repository den Workflow `.github/workflows/template-sync-pr.yml` enthält.
2. Unter `Settings -> Secrets and variables -> Actions -> Variables` die Variable `TEMPLATE_UPSTREAM_REPO=ChristineJanischek/edu-code-course-rdb` setzen.
3. Prüfen, dass der Default-Branch `main` heißt.
4. Falls Branch-Schutz aktiv ist: GitHub Actions Push auf `main` erlauben oder PR-basierte Übernahme zulassen.
5. Keine selektiven Cherry-Picks für Template-Updates verwenden, wenn der Upstream strukturell umgebaut wurde.
6. Nach dem ersten Sync prüfen, ob `generated/`, `scripts/`, `services/`, `webapp/` und `docs/` vollständig übernommen wurden.
7. Bei Konflikten immer `upstream/main` vollständig mergen, nicht einzelne Dateien manuell nachziehen.

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

Diese Routine ist bewusst als Voll-Repo-Merge formuliert. Sie ist die richtige Wahl, wenn sich das Ursprungsrepository in vielen Bereichen gleichzeitig weiterentwickelt hat.

## Empfehlung für den Unterrichtsbetrieb

- Führe die Sync-Routine mindestens 1x pro Woche aus.
- Führe sie zusätzlich vor Beginn einer neuen Klassenarbeits- oder Übungsphase aus.
- Nach dem Merge kurz prüfen:
  - `generated/informationen/begrifflichkeiten/`
  - `generated/informationen/teil-b/`
  - `generated/informationen/teil-c/`

Hinweis: Wenn der automatische Workflow aktiv ist, dient die manuelle Routine vor allem als Fallback bei Merge-Konflikten.

## Mindestregel für Template-Nutzer

- Upstream-Änderungen immer von `upstream/main` übernehmen.
- Das Repository nie nur teilweise synchronisieren.
- Bei größeren Änderungen zuerst den automatischen Sync-Workflow oder einen normalen Merge verwenden und erst danach lokale Anpassungen erneut einbringen.

## Optional: Team-Standard festlegen

Wenn mehrere Personen am Schul-Repository arbeiten, die Routine als festen Termin in den Teamkalender aufnehmen (z. B. Montag 07:30 Uhr).
