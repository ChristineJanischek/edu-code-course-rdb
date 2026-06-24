# Prozess: Qualitaets-Gates & Automatisierung

**Version:** 1.0
**Status:** Aktiv
**Gueltig ab:** 25.03.2026

---

## Ziel

Sicherstellen, dass jede Code- oder Doku-Erweiterung automatisiert auf OOP, Erweiterbarkeit, Wartbarkeit, Sicherheit, Wiederverwendbarkeit, Redundanzfreiheit und Dokumentationskonsistenz geprueft wird.

## Pflicht-Gates

1. Security-Gate: `bash scripts/validate-security.sh`
2. Architecture-Gate: `bash scripts/validate`bash scripts/validate-architecture.sh`: `bash scripts/validate-docs.sh`

Hinweis Klassen`bash scripts/validate-docs.sh`b des Documentation-Gates wird zusaetzlich `bash scripts/validate-ka-separate-context.sh` ausgeführt.
- Dadu`bash scripts/validate-ka-separate-context.sh` und Teil C (SQL) didaktisch getrennte Kontexte verwenden.

Hinweis zentrale Einstiegspunkte:
- Innerhalb des Documentation-Gates wird zusaetzlich `bash scripts/validate-central-entrypoints.sh` ausgeführt.
- Dadurch wird erzwungen, dass nur folg`bash scripts/validate-central-entrypoints.sh`arkiert sind:
	- `README.md`
	- `generated/README.md`
	- `docs/handbuch/README.md`

Alle drei Gates sind lokal und in CI verpflichtend.

## Workflow
`README.md`ng`generated/README.md`rchfuehren
2`docs/handbuch/README.md`wn synchronisieren: `bash scripts/sync-generated-html.sh`
3. Dokumentation automatisch optimieren: `bash scripts/optimize-docs.sh`
3. Lokale Gates ausführen
4. PR mit Te`bash scripts/sync-generated-html.sh`s müssen gruen sein
6. Review + Merge

## Dokumentations-Autopilo`bash scripts/optimize-docs.sh`mize-docs.sh`
- Funktionen:
	- synchronisiert planverlinkte Markdown-Dateien mit ihren HTML-Gegenstuecken
	- normalisiert Markdown-Dateien (Whitespace, Leerzeilen, konsistent`bash scripts/optimize-docs.sh`ft doppelte Ueberschriften als Redundanzsignal
	- validiert die Wohlgeformtheit direkt im Anschluss
- Das Documentation-Gate (`bash scripts/validate-docs.sh`) erzwingt diese Strukturpruefung automatisch.

## Abbruchkriterien

Ein Merge ist zu stoppen, wenn mindestens eines der folgenden Kriterien zutrifft:

- Sicherheitsverstoß (Secr`bash scripts/validate-docs.sh`ak)
- Architekturverstoß (Schichtbruch, Encapsulation-Verletzung)
- Doku-Luecke (Code geändert, Handbuch nicht aktualisiert)

## Messkriterien

- CI-Erfolgsrate der Pflicht-Gates
- Anzahl geblockter Merges durch Gate-Fehler
- Anteil Änderungen mit aktualisierter Doku

## Changelog

- v1.0 (25.03.2026): Initiale Prozessdefinition für automatische Qualitaets-Gates
