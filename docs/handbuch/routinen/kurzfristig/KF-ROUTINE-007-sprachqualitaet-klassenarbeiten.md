# KF-ROUTINE-007: Sprachqualitaet in Klassenarbeiten (UTF-8 und Transferleistung)

## Metadata
- **ID:** KF-ROUTINE-007
- **Kategorie:** kurzfristig
- **Haeufigkeit:** bei jeder Aenderung an Klassenarbeitsvorlagen
- **Zeitaufwand:** 5-10 Minuten
- **Verantwortlicher:** Autor der Aenderung
- **Abhaengigkeiten:** KF-ROUTINE-006-qualitaetsgate-pruefung.md
- **Version:** 1.0
- **Letzte Aktualisierung:** 09.05.2026

## Ziel
Sicherstellen, dass Aufgabenstellungen sprachlich korrekt mit UTF-8-Umlauten vorliegen und die Transferleistung nicht durch loesungsnahe Stichpunkte reduziert wird.

## Vorbedingungen
- Klassenarbeitsdateien wurden geaendert.
- Lokale Aenderungen sind gespeichert.

## Schritte
1. Sprachqualitaetspruefung ausfuehren: `bash scripts/validate-ka-language-quality.sh`
2. Bei Fundstellen Umlaute direkt als UTF-8 schreiben (z. B. "Entitäten" statt "Entitaeten").
3. Zu direkte Loesungshinweise in Sachverhaltsaufgaben umformulieren.
4. Danach Pflicht-Gates erneut ausfuehren: Security, Architektur, Doku.

## Erfolgskriterien
- Keine ASCII-Umschriften in den geprueften Klassenarbeitsdateien.
- Keine loesungsnahen Stichpunkte in Aufgabenstellungen.
- `bash scripts/validate-docs.sh` laeuft erfolgreich.

## Fehlerbehandlung
- Wiederholte Verstosse: Formulierungsrichtlinie im Teamreview schaerfen.
- UTF-8-Probleme im Editor: Datei-Encoding explizit auf UTF-8 setzen.

## Ausgaben/Ergebnisse
- Korrekt codierte und didaktisch saubere Aufgabenstellungen.

## Verknuepfungen
- [KF-ROUTINE-006-qualitaetsgate-pruefung.md](./KF-ROUTINE-006-qualitaetsgate-pruefung.md)

## Changelog
- v1.0 (09.05.2026): Initiale Routine erstellt
