# KF-ROUTINE-006: Qualitaets-Gate-Pruefung vor Merge

## Metadata
- **ID:** KF-ROUTINE-006
- **Kategorie:** kurzfristig
- **Häufigkeit:** bei jedem PR
- **Zeitaufwand:** 10-15 Minuten
- **Verantwortlicher:** Autor der Änderung
- **Abhängigkeiten:** review-prozess.md, qualitaets-gates-automatisierung.md
- **Version:** 1.0
- **Letzte Aktualisierung:** 25.03.2026

## Ziel
Vor jedem Merge automatisiert sicherstellen, dass Design-Prinzipien und Dokumentationspflichten eingehalten sind.

## Vorbedingungen
- Alle lokalen Codeaenderungen sind gespeichert.
- Branch ist aktuell.

## Schritte
1. Security-Gate ausführen: `bash scripts/validate-security.sh`
2. Architecture-Gate ausführen: `bash scripts/validate`bash scripts/validate-architecture.sh` ausführen: `bash scripts/validate-docs.sh`
4. Bei Fehlern U`bash scripts/validate-docs.sh`t starten.
5. PR mit Checklist ausfuellen und einreichen.

## Erfolgskriterien
- Alle drei Gates erfolgreich.
- PR-Checklist vollstaendig.
- Keine offenen Architektur-/Security-Hinweise im Review.

## Fehlerbehandlung
- Gate fehlgeschlagen: Merge stoppen, Fehler ursachenbasiert beheben.
- Mehrfaches Scheitern: Review durch zweite Person und Anpassung der Validierungsskripte.

## Ausgaben/Ergebnisse
- Nachweisbar valider PR mit gruenen Pflichtchecks.

## Verknuepfungen
- [review-prozess.md](../../prozesse/review-prozess.md)
- [qualitaets-gates-automatisierung.md](../../prozesse/qualitaets-gates-automatisierung.md)

## Changelog
- v1.0 (25.03.2026): Initiale Routine erstellt
