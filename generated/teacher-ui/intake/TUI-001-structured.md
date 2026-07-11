# TUI-001 Strukturierte Intake-Analyse

Erstellt am (UTC): 2026-07-11T15:26:38Z

## Normalisierte Eingabe

Lehrkraefte sollen Ideen per Sprache erfassen koennen. Die Eingabe wird transkribiert, sprachlich bereinigt und in einzelne Anforderungen zerlegt. Das System soll Zielgruppe, Prozess und passende UI-Zuordnung vorschlagen. Danach soll automatisch eine priorisierte To-do-Liste mit Akzeptanzkriterien und technischen Aufgaben erzeugt werden.

## Erkannte Einzelanforderungen

1. Lehrkraefte sollen Ideen per Sprache erfassen koennen
2. Die Eingabe wird transkribiert, sprachlich bereinigt und in einzelne Anforderungen zerlegt
3. Das System soll Zielgruppe, Prozess und passende UI-Zuordnung vorschlagen
4. Danach soll automatisch eine priorisierte To-do-Liste mit Akzeptanzkriterien und technischen Aufgaben erzeugt werden

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
