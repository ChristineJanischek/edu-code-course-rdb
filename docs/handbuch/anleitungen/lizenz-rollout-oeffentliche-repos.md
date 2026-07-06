# Anleitung: Lizenz-Rollout fuer alle oeffentlichen Repositories

## Ziel

Diese Anleitung beschreibt, wie die benutzerdefinierte Lizenzpolitik automatisiert auf alle oeffentlichen Repositories eines GitHub-Owners ausgerollt wird.

Die Lizenzpolitik lautet:

- Namensnennung verpflichtend: Christine Janischek - https://emotionalspirit.de
- Ausschliesslich nicht-kommerzielle Nutzung
- Nutzung nur im staatlichen Schulwesen
- Alle anderen Nutzungen nur nach ausdruecklicher vorheriger schriftlicher Genehmigung

## Skript

Das Rollout-Skript liegt hier:

- `scripts/rollout-custom-license-all-public-repos.sh`

## Voraussetzungen

1. GitHub CLI ist installiert und authentifiziert (`gh auth status`).
2. Push-/PR-Rechte auf die Ziel-Repositories sind vorhanden.

## Empfohlener Ablauf

1. Zuerst Dry-Run ausfuehren:

```bash
bash scripts/rollout-custom-license-all-public-repos.sh \
  --owner ChristineJanischek \
  --dry-run
```

2. Danach Rollout mit Push und PR-Erstellung starten:

```bash
bash scripts/rollout-custom-license-all-public-repos.sh \
  --owner ChristineJanischek \
  --apply \
  --push \
  --create-pr
```

## Wichtige Optionen

- `--include "repo1,repo2"`: nur ausgewaehlte Repositories verarbeiten
- `--exclude "repo3,repo4"`: Repositories ausnehmen
- `--branch-name <name>`: eigenen Branch-Namen setzen
- `--base-branch <branch>`: abweichenden Basis-Branch erzwingen

## Was im Ziel-Repository geaendert wird

1. `LICENSE` wird auf den benutzerdefinierten Lizenztext gesetzt.
2. `NOTICE` wird mit Attributionshinweis erstellt.
3. `README.md` erhaelt einen Lizenzabschnitt (idempotent ueber Marker).

## Sicherheit und Betrieb

- Das Skript arbeitet standardmaessig im Dry-Run-Modus.
- Ohne `--apply` werden keine Repositories veraendert.
- PR-Erstellung ist nur mit `--push` moeglich.
