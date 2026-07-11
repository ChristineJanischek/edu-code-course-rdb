# TUI-001-M6 Strukturierte Intake-Analyse

Erstellt am (UTC): 2026-07-11T20:42:21Z

## Normalisierte Eingabe

Titel: M6 Schulbetrieb-Features in Teilaufgaben Freitext: Wir wollen im nächsten Inkrement drei Schienen sauber trennen. Erstens Avatar und Voice als optionale Lehrkraftfunktionen mit klarer DSGVO-konformer Speicherung, Löschkonzept, Rollenrechten und Opt-in. Zweitens Governance für Prompt-, Wissens- und Modellupdates mit Vier-Augen-Freigabe, Versionierung, Rollback und Audit-Trail. Drittens Pilotbetrieb mit Feedbackzyklus über zwei Klassen, definierten Erfolgsmetriken, wöchentlichem Review und priorisierter Nachsteuerung. Prioritaet: Hoch Zielbereich: Core Betroffener Prozess: Schulbetrieb und Qualitätssteuerung Optionaler UI-Bereich: Lehrkraft-Dashboard, Kurseditor, Admin-Konsole

## Erkannte Einzelanforderungen

1. Titel: M6 Schulbetrieb-Features in Teilaufgaben Freitext: Wir wollen im nächsten Inkrement drei Schienen sauber trennen
2. Erstens Avatar und Voice als optionale Lehrkraftfunktionen mit klarer DSGVO-konformer Speicherung, Löschkonzept, Rollenrechten und Opt-in
3. Zweitens Governance für Prompt-, Wissens- und Modellupdates mit Vier-Augen-Freigabe, Versionierung, Rollback und Audit-Trail
4. Drittens Pilotbetrieb mit Feedbackzyklus über zwei Klassen, definierten Erfolgsmetriken, wöchentlichem Review und priorisierter Nachsteuerung
5. Prioritaet: Hoch Zielbereich: Core Betroffener Prozess: Schulbetrieb und Qualitätssteuerung Optionaler UI-Bereich: Lehrkraft-Dashboard, Kurseditor, Admin-Konsole

## Standard To-do-Liste

- [ ] Idee vollstaendig erfassen
- [ ] Einzelanforderungen finalisieren
- [ ] Zielgruppe und Rollen zuordnen
- [ ] Prozesszuordnung bestaetigen
- [ ] UI-Zuordnung mit Klickpfad pruefen
- [ ] Dopplungen gegen bestehende UI pruefen
- [ ] Prioritaet und Abhaengigkeiten festlegen
- [ ] Akzeptanzkriterien definieren
- [ ] Technische Teilaufgaben anlegen
- [ ] Testfaelle spezifizieren
- [ ] Datenschutz- und Sicherheitscheck einplanen

## Akzeptanzkriterien

1. Spracheingabe wird in weniger als 5 Sekunden in Klartext normalisiert.
2. Jede Eingabe wird in mindestens eine, maximal 15 Einzelanforderungen zerlegt.
3. Jede Einzelanforderung enthaelt Prozess- und Zielbereichszuordnung (Core/Course).
4. Es wird automatisch eine priorisierte To-do-Liste erzeugt.
5. Akzeptanzkriterien und technische Teilaufgaben werden im Backlog gespeichert.
6. Unklare Angaben werden als offene Punkte markiert, nicht verworfen.

## Testvorschlaege

- Parser-Test: Fuellwoerter entfernen ohne Bedeutungsverlust.
- Segmentierungs-Test: Lange Spracheingabe wird korrekt in Anforderungen geteilt.
- Mapping-Test: Prozess und Zielbereich werden fuer jede Anforderung gesetzt.
- Regressionstest: Leere oder sehr kurze Eingaben liefern klare Fehlermeldung.
