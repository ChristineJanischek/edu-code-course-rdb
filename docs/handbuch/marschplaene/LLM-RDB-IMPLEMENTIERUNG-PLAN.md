# Marschplan: LLM-Implementierung fuer RDB-Lernassistenz

Version: 1.0
Datum: 01.07.2026
Status: Aktiv

---

## Ziel

Schrittweise Implementierung eines sicheren, didaktisch fuehrenden KI-Assistenten fuer relationale Datenbanken mit Wissensanbindung und systematischer Lernprozessunterstuetzung.

---

## Phase 0: Baseline sichern (Tag 0)

- Repo-Stand versionieren (Tag): snapshot-2026-07-01-pre-llm-rdb
- Pflicht-Gates gruene Basis herstellen

Ergebnis:
- Reproduzierbarer Ausgangspunkt vorhanden

---

## Phase 1: Architekturgrundlage (Woche 1)

- Backend-Schichten fuer Assistenten anlegen (Route, Service, Repository, Models)
- Frontend-MVC-Basis fuer Hinweisdialog anlegen
- Hint-Modus erzwingen (keine Vollloesung)

Definition of Done:
- POST /api/v1/assistant/hint liefert robuste didaktische Hinweise
- Frontend kann Hinweisanfrage ausfuehren

Status-Checkpoint (01.07.2026):
- API-Endpunkt fuer den Hint-Modus ist aktiv und ueber Python-API sowie PHP-Proxy validiert.
- Sichtbares Assistant-Panel mit Formular, Statusanzeige und Hinweis-Ausgabe ist in der Webapp integriert.
- UI-Workspace ist auf zwei Hauptreiter erweitert: Reiter 1 fuer Information/Aufgaben/Stichwortsuche und Reiter 2 fuer Editor/Assistenz.
- Praxisbereich enthaelt zusaetzlichen Datei-Reiter sowie Weiter- und Check-Funktion fuer Selbstkontrolle.

---

## Phase 2: Wissensanbindung RDB (Woche 2-3)

- W3Schools-SQL-Inhalte regelkonform ingestieren (Crawling nur nach Nutzungsbedingungen)
- Chunking, Metadaten, Quellenpriorisierung
- Ablage in normalisierter Wissensstruktur

Definition of Done:
- RDB-Wissensindex versioniert und aktualisierbar
- Quellenprovenienz pro Antwort dokumentiert

---

## Phase 3: Didaktik-Engine (Woche 4-5)

- Rubriken fuer Hilfegrade (Anstoss, Leitfrage, Teilschritt)
- Fehlerklassifikation haeufiger SQL-Fehler
- Personalisierte Folgefragen pro Kompetenzstufe

Definition of Done:
- Assistent passt Hinweise an Fehlerbild und Lernstand an
- Lehrkraftmodus und Schuelermodus sauber getrennt

---

## Phase 4: Schulbetrieb-Features (Woche 6-8)

- Avatar-Konfiguration
- Sprachtranskription mit DSGVO-konformer Speicherung
- Upload- und Dokumentenbezug fuer Unterrichtsmaterial

Definition of Done:
- Sprachdialog und Chat laufen in gesichertem Betriebsmodus
- Rollenrechte und Audit-Trail aktiv

---

## Phase 5: Qualität, Sicherheit, Rollout (Woche 9+)

- Lasttests und Sicherheitstests
- Lehrkraft-Feedbackzyklen
- Governance fuer Prompt-, Wissens- und Modellupdates

Definition of Done:
- Stabiler Pilotbetrieb
- Dokumentierte Betriebsprozesse

---

## Schritt-fuer-Schritt Leitfaden (ausfuehrbar)

1. Baseline-Tag setzen und pushen.
2. API-Grundendpunkt fuer Hint-Modus bereitstellen.
3. Frontend-Dialog fuer Hinweisabfrage integrieren.
4. Logging/Audit fuer Interaktionen aktivieren.
5. Wissens-Ingestion fuer RDB starten.
6. Didaktische Regelwerke je Kompetenzstufe definieren.
7. Lehrkraft-Tools fuer Aufgaben- und Bewertungsunterstuetzung erweitern.
8. Datenschutz-Review und Freigabeprozess durchlaufen.
9. Pilotklasse aufsetzen und Feedback aufnehmen.
10. Verbesserungen versioniert in den naechsten Zyklus uebernehmen.

---

## Risiken und Gegenmassnahmen

- Risiko: Halluzinationen
  - Gegenmassnahme: Quellenpflicht, konservative Antwortpolitik, Hint-Modus
- Risiko: Datenschutzverletzung
  - Gegenmassnahme: Datensparsamkeit, Rollenrechte, Loeschkonzept
- Risiko: Ueberautomatisierung
  - Gegenmassnahme: Lehrkraft bleibt Freigabeinstanz

---

## Changelog

- v1.0 (01.07.2026): Erstanlage Marschplan fuer RDB-LLM-Implementierung.
- v1.1 (01.07.2026): Phase-1-Checkpoint mit erfolgreicher API-Validierung und sichtbarer Frontend-Integration des Assistant-Panels ergaenzt.
- v1.2 (01.07.2026): UX-Ausbau auf 2-Reiter-Workspace inkl. Datei-Reiter und Selbstkontroll-Assistenz dokumentiert.
