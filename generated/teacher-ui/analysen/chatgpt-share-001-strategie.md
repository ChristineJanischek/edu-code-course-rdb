# Strategieplan: ChatGPT - Automatisierte UI-Entwicklung

## Kernbild

- Idee: Paeadagogische Ideen automatisch in didaktisch tragfaehige digitale Lernmodule uebersetzen.
- Ausgangspunkt: Freiform-Ideen und Sprachinput sind vorhanden, aber bisher nicht als durchgaengige Quellkette im Repo angedockt.
- Ziel: Eine wiederholbare Teacher-UI- und Kurseditor-Pipeline, die Ideen aufnimmt, analysiert, Module plant, testbar macht und transparent fortschreibt.
- Philosophie: Bedarfsgesteuerte Softwareentwicklung: erst den Lehrerprozess verstehen, dann Funktionen pro Taetigkeit kapseln und sichtbar machen.

## Erkannte Bedürfnisse

- Freiform- und Spracheingaben ohne Vorstruktur aufnehmen
- Ideen in Prozesse, Bedürfnisse und Module zerlegen
- Didaktik, Lehrplan und Differenzierung automatisch mitdenken
- Backend- und Frontend-Bausteine pro Lehrerprozess planen
- Meilensteine, Tests und Wochenberichte aus derselben Quelle ableiten
- Lehrkraft als finale Entscheidungstraegerin im Review behalten

## Module

### MOD-SRC-001: Share-Quellenimport

- Prozess: Quelle andocken
- Status: implemented
- Ziel: Externe ChatGPT-Share-Quellen reproduzierbar importieren und als Repo-Artefakt sichern.
- Backend: scripts/import_teacher_ui_share.py
- Backend: generated/teacher-ui/sources/*.md
- Backend: generated/teacher-ui/batches/*-input.txt
- Frontend: Teacher-UI Modulplan im Informationsfenster
- Test: Share-URL ist abrufbar
- Test: Nach dem Import existieren Quellen-, Plan- und Reportdateien

### MOD-ANL-002: Bedarfs- und Prozessanalyse

- Prozess: Ideen analysieren
- Status: implemented
- Ziel: Aus Rohideen Bedürfnisse, Prozesse, UI-Zuordnung und technische Aufgaben ableiten.
- Backend: scripts/teacher-ui-intake.sh
- Backend: scripts/teacher-ui-routing.sh
- Backend: scripts/teacher-ui-todo.sh
- Backend: scripts/teacher-ui-context.sh
- Frontend: Prozessgruppen im Modulplan
- Frontend: Status- und Testangaben pro Modul
- Test: Intake erzeugt strukturierte Anforderungen
- Test: Routing ordnet Prozesse und UI-Hauptbereiche zu
- Test: To-do-Datei enthaelt Testschritte

### MOD-DID-003: Didaktik- und Lehrplan-Mapping

- Prozess: Unterricht planen
- Status: implemented
- Ziel: Kompetenzziele, Differenzierung, Altersstufe und Lehrplanhinweise aus der Quelle auf Kursbausteine mappen.
- Backend: Curriculum-Service mit Tagging und Empfehlungen
- Backend: Mapping-Regeln fuer Kompetenzziele
- Backend: Lehrplanindex aus generated/lehrplaene/index.json
- Frontend: Planungskarte mit Lehrplan- und Kompetenzhinweisen
- Frontend: Kontext-Hinweise im Kurseditor
- Frontend: Curriculum-Empfehlungen im Strategiepanel
- Test: Lehrplanhinweise erscheinen pro Modulkontext
- Test: Empfehlungen sind pro Curriculum-Dokument nachvollziehbar
- Test: Curriculum-Empfehlungen werden im Web-Frontend gerendert

### MOD-GEN-004: Unterrichtsmodul-Generator

- Prozess: Module generieren
- Status: planned
- Ziel: Aus validierten Anforderungen Kursmodule, Aufgaben, Bewertungsraster und Lernhilfen zusammenstellen.
- Backend: Generator fuer Materialpakete und Bewertungsraster
- Backend: Versionsierte Moduldefinitionen
- Frontend: Modul-Composer pro Arbeitsprozess
- Frontend: Vorschau fuer Aufgaben, Hinweise und Veroeffentlichung
- Test: Jedes Modul hat Aufgabe, Hilfe, Bewertung und Publikationsstatus
- Test: Fehlende Daten brechen die Vorschau nicht

### MOD-OPS-005: Milestone- und Testorchestrierung

- Prozess: Qualitaet sichern
- Status: implemented
- Ziel: Naechste Meilensteine, Regressionstests und Qualitaets-Gates automatisch fortschreiben.
- Backend: scripts/weiter.sh
- Backend: scripts/teacher-ui-milestone.sh
- Frontend: Milestone- und Testlisten im Modulplan
- Test: Weiter-Report wird aktualisiert
- Test: Milestone-Datei verweist auf Regressionstestpfad

### MOD-REP-006: Wochenbericht-Automat

- Prozess: Transparenz herstellen
- Status: implemented
- Ziel: Aktuellen Stand, umgesetzte Module und naechste Schritte als wiederholbaren Wochenbericht ausgeben.
- Backend: generated/teacher-ui/reports/*.md
- Backend: webapp/public/data/teacher-ui-module-plan.json
- Frontend: Wochenberichtskarte im Informationsfenster
- Test: Bericht nennt Stand, umgesetzte Module und naechste Schritte
- Test: Bericht bleibt auch ohne externe Quelle konsistent lesbar

## Meilensteine

- MS-01: Quelle ingestieren und strukturieren (done)
- MS-02: Strategieplan im UI sichtbar machen (done)
- MS-03: Didaktisches Mapping und Modulgenerator vertiefen (next)

## Wochenbericht

- Stand: Die externe Strategiequelle ist nun als Artefakt importiert, analysiert und in einen sichtbaren Modulplan fuer die Webapp ueberfuehrt.
- Umgesetzt: Share-Quellenimport
- Umgesetzt: Bedarfs- und Prozessanalyse
- Umgesetzt: Didaktik- und Lehrplan-Mapping
- Umgesetzt: Milestone- und Testorchestrierung
- Umgesetzt: Wochenbericht-Automat
- Naechster Schritt: Modul-Generator fuer Aufgaben, Bewertungsraster und Publikation konkretisieren
- Naechster Schritt: Curriculum-Mapping von Empfehlungen auf konkrete Modulvorlagen verfeinern
- Naechster Schritt: Wochenberichte optional zeitgesteuert aus demselben Datenmodell erzeugen
