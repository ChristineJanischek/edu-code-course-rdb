# Anleitung: Neues GitHub-Repository mit automatischer Custom-Lizenz

## Ziel

Diese Anleitung beschreibt, wie ein neues Repository direkt mit der aktuell verwendeten Custom-Lizenz erstellt wird.

Damit wird beim Erstellen automatisch sichergestellt, dass folgende Artefakte vorhanden sind:

1. `LICENSE` mit der benutzerdefinierten Lizenz
2. `NOTICE` mit Attributionshinweis
3. `README.md` mit idempotentem Lizenz-Block (Marker-basiert)

## Skript

Das Skript liegt hier:

- `scripts/create-repo-with-custom-license.sh`

Kompakter Entry-Point (Alias-Skript):

- `scripts/new-repo-license.sh`
- `scripts/newrepo-license`

Es verwendet intern die gemeinsame Lizenz-Bibliothek:

- `scripts/lib/custom-license-policy.sh`

Optionales Installationsskript für Shell-Erinnerung nach `gh repo create`:

- `scripts/install-newrepo-license-reminder.sh`

## Voraussetzungen

1. GitHub CLI ist installiert und authentifiziert (`gh auth status`).
2. Berechtigung zum Erstellen von Repositories beim angegebenen Owner ist vorhanden.
3. `git` ist installiert.

## Empfohlener Ablauf

0. Einmalig Kommando + Erinnerung installieren:

```bash
bash scripts/install-newrepo-license-reminder.sh --apply
source ~/.bashrc
```

Danach ist der Befehl `newrepo-license` direkt verfügbar und bei erfolgreichem `gh repo create` erscheint automatisch ein Hinweis zum sofortigen Ausführen.

1. Dry-Run ausführen (kurzer Befehl):

```bash
bash scripts/new-repo-license.sh \
  --owner ChristineJanischek \
  --name mein-neues-repo \
  --description "Neues Projekt mit Custom-Lizenz" \
  --visibility public \
  --dry-run
```

2. Repository erstellen und Lizenz automatisch anwenden:

```bash
bash scripts/new-repo-license.sh \
  --owner ChristineJanischek \
  --name mein-neues-repo \
  --description "Neues Projekt mit Custom-Lizenz" \
  --visibility public \
  --apply
```

3. Optional: Vollständiges Skript direkt nutzen (gleiches Ergebnis):

```bash
bash scripts/create-repo-with-custom-license.sh \
  --owner ChristineJanischek \
  --name mein-neues-repo \
  --description "Neues Projekt mit Custom-Lizenz" \
  --visibility public \
  --apply
```

## Wichtige Optionen

- `--owner <owner>`: GitHub User/Org (Pflicht)
- `--name <repo-name>`: Repository-Name (Pflicht)
- `--description <text>`: optionale Beschreibung
- `--visibility <public|private>`: Sichtbarkeit (Standard: `public`)
- `--target-dir <path>`: Zielordner für den Clone
- `--default-branch <name>`: bevorzugter Branchname für den ersten Push (Standard: `main`)
- `--apply`: führt Erstellung und Push real aus
- `--dry-run`: zeigt nur den Ablauf (Standardmodus)

## Sicherheits- und Betriebsverhalten

- Standard ist Dry-Run, es werden ohne `--apply` keine Änderungen durchgeführt.
- Das Skript bricht ab, wenn der Zielordner bereits ein Git-Repository enthält.
- Die Lizenzanwendung ist idempotent für den README-Lizenzblock (Marker-basiert).
- Die Shell-Erinnerung wird nur nach erfolgreichem `gh repo create` ausgegeben.
- Die Installation der Erinnerung ist idempotent und ersetzt einen vorhandenen Block sauber.

## Hinweis zu bestehenden Repositories

Für bereits existierende Repositories ist weiterhin dieses Skript zuständig:

- `scripts/rollout-custom-license-all-public-repos.sh`
