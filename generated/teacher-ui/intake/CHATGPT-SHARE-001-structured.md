# CHATGPT-SHARE-001 Strukturierte Intake-Analyse

Erstellt am (UTC): 2026-07-13T11:27:07Z

## Normalisierte Eingabe

Quelle: ChatGPT - Automatisierte UI-Entwicklung. Lehrkraefte sollen paedagogische Ideen, Aenderungswuensche und Funktionsvorschlaege frei per Text oder Sprache erfassen koennen. Das System soll die Eingaben automatisch sprachlich bereinigen, strukturieren, in Einzelanforderungen zerlegen, Beduerfnisse und Prozesse erkennen, geeignete Funktionalitaeten ableiten, UI-Bereiche pro Taetigkeit zuordnen, Module fuer Backend und Frontend planen, Meilensteine bestimmen, Tests festlegen und Wochenberichte mit aktuellem Stand, umgesetzten Modulen und naechsten logischen Schritten erzeugen. Lehrplaene, Kompetenzziele, Differenzierung, Kursveroeffentlichung, Bewertungsraster, Musterloesungen und KI-Feedback muessen als wiederholbare Prozesskette beruecksichtigt werden.

## Erkannte Einzelanforderungen

1. Quelle: ChatGPT - Automatisierte UI-Entwicklung
2. Lehrkraefte sollen paedagogische Ideen, Aenderungswuensche und Funktionsvorschlaege frei per Text oder Sprache erfassen koennen
3. Das System soll die Eingaben automatisch sprachlich bereinigen, strukturieren, in Einzelanforderungen zerlegen, Beduerfnisse und Prozesse erkennen, geeignete Funktionalitaeten ableiten, UI-Bereiche pro Taetigkeit zuordnen, Module fuer Backend und Frontend planen, Meilensteine bestimmen, Tests festlegen und Wochenberichte mit aktuellem Stand, umgesetzten Modulen und naechsten logischen Schritten erzeugen
4. Lehrplaene, Kompetenzziele, Differenzierung, Kursveroeffentlichung, Bewertungsraster, Musterloesungen und KI-Feedback muessen als wiederholbare Prozesskette beruecksichtigt werden

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
