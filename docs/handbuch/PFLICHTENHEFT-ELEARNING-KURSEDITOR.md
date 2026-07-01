# Pflichtenheft: Intelligentes webbasiertes eLearning-Kurseditor-System (Informatik)

Version: 1.0
Status: Konzept und Architekturentwurf
Datum: 01.07.2026

---

## 1. Projektvision

Ziel ist ein webbasiertes, intelligentes Kurseditor-System fuer den Informatikunterricht mit Schwerpunkt auf praxisorientiertem Lernen (Code-In-Boxen, Modellierungsaufgaben, qualitaetsgesicherte Aufgabenentwicklung, intelligente Lernpfade).

Das System ist kein klassisches LMS, sondern ein didaktischer Kurseditor mit KI-Unterstuetzung fuer Lernende und Lehrkraefte.

Langfristig soll die Loesung auf weitere Faecher uebertragbar sein (Deutsch, Mathematik, Sprachen, Naturwissenschaften).

---

## 2. Empfehlung Authoring-System (Best Practice, 3 Optionen)

### Empfehlung

Fuer diesen Use-Case wird ein hybrider Ansatz empfohlen:

- H5P als didaktischer Interaktions-Baukasten
- Adapt Learning als strukturierter Kurs-Player
- Eigener domaenenspezifischer Kurseditor in diesem Repository als Fach- und Governance-Schicht

### Vergleich

| System | Vorteile | Nachteile | Eignung im Projekt |
|---|---|---|---|
| H5P (self-hosted) | Viele interaktive Aufgabentypen, schnell einsetzbar, breite Community | Begrenzte fachspezifische Modellierung ohne Zusatzlogik | Sehr gut fuer Uebungs-Interaktionen und formative Checks |
| Adapt Learning | Responsives Kursframework, saubere Content-Struktur, gut fuer Lernpfade | Hoeherer Initialaufwand, Authoring weniger intuitiv als H5P | Gut fuer lineare und verzweigte Lernpfade |
| eXeLearning | Offline-faehig, leichtgewichtig, einfacher Einstieg | Eingeschraenkte moderne Interaktivitaet, weniger flexibel bei Live-Assistenten | Gut fuer schnelle Materialpakete und Export |

Entscheidungsregel:
- Kurzfristig: H5P + bestehende Webapp-Komponenten.
- Mittelfristig: Adapt-Lernpfade fuer groessere Kurssequenzen.
- Dauerhaft: Eigener Editor als SSOT fuer Inhalte, Metadaten, Bewertung und KI-Assistenz.

---

## 3. Projektziele

### Paedagogische Ziele

- Handlungsorientierter Informatikunterricht
- Selbstgesteuertes Lernen mit Hilfestellungen statt Loesungsvorgaben
- Strukturierte Lernpfade und Reflexionsschritte
- Integration moderner Themen (KI und Machine Learning)

### Technische Ziele

- Erweiterbarkeit, Wartbarkeit, Wiederverwendbarkeit
- Security by default, Datenschutz im Schulkontext
- Hohe Usability fuer Lehrkraft und Lernende
- OOP- und MVC-konforme Architektur
- Vollstaendige und redundanzarme Dokumentation

---

## 4. Zielgruppen

Primaer:
- Informatiklehrkraefte
- Lernende Sekundarstufe II
- Berufskollegs und Gymnasien

Sekundaer:
- Fachschaften Informatik
- Schulen mit GitHub Classroom
- Entwicklerteams fuer Bildungssoftware

---

## 5. Fachlicher Scope (Inkrement 1)

Fokusdomaene in diesem Inkrement:
- Relationale Datenbanken (RDB)
- EERM, Normalisierung, SQL (DDL/DML, SELECT/JOIN/GROUP BY/HAVING)

Quellenanbindung:
- Primär externe Referenz: https://www.w3schools.com/sql/
- Interne SSOT-Quellen: data/content-db, docs/handbuch, generated/

---

## 6. Kernanforderungen

### Funktionale Anforderungen

- KI-Assistent beantwortet Fragen von Schuelern und Lehrkraeften im Lernkontext.
- Antworten sind didaktisch fuehrend, ohne komplette Musterloesung vorwegzunehmen.
- Fragen und Hinweise werden systematisch erfasst und strukturiert gespeichert.
- Wissensdatenbank wird aus internen Quellen und kontrollierten externen Quellen gepflegt.
- Lehrkraftfunktionen: Aufgabenstellung, Loesung, didaktische Hilfen, Bewertung, Projektbegleitung, Dokumentenverwaltung (Upload/Download).
- Avatar-Konfiguration fuer den Assistenten.
- Chatfunktionen und Uploadfunktionen.
- Sprachkommunikation: Transkription und didaktische Auswertung.

### Nicht-funktionale Anforderungen

- Datenschutz fuer Schulen (Datenminimierung, Rollenrechte, Protokollierung, Loeschkonzepte).
- Nachvollziehbarkeit aller KI-Antworten (Quellenhinweis, Versionierung, Audit-Trail).
- Ausfallsicherheit und reproduzierbare Deployments.
- Sicherheitstests und Eingabevalidierung auf allen API-Pfaden.

---

## 7. Sicherheits- und Datenschutzanforderungen (Schulwesen)

- Rollenmodell: Lernende, Lehrkraft, Admin, Auditor.
- Standardmaessig minimale Datenspeicherung (Privacy by default).
- Keine Speicherung sensibler Inhalte ohne explizite Notwendigkeit.
- Verschluesselung in Transit und at Rest.
- Trennung von Inhaltsdaten, Bewertungsdaten und Kommunikationsdaten.
- Keine internen Stacktraces oder Sicherheitsdetails in Client-Antworten.
- Regelmaessige Sicherheitsvalidierung ueber vorhandene Repo-Gates.

---

## 8. Architekturvorgaben (OOP/MVC)

Frontend (MVC):
- Model: Zustand, Eingabevalidierung, Payload-Bildung.
- View: Rendering und sichere Nutzerrueckmeldungen.
- Controller: Eventsteuerung und API-Orchestrierung.

Backend (Service-Architektur):
- Route/Controller: HTTP-Validierung und Response-Konsistenz.
- Service: Didaktiklogik, Hint-Generierung, Tutor-Policy.
- Repository: Interaktionsspeicherung und Wissensquellen-Zugriff.

---

## 9. Implementierungsinkrement 1 (im Repo bereits vorbereitet)

- API-Endpunkt fuer Lernhinweise: POST /api/v1/assistant/hint
- Service-Schichten in services/python-api/learning_api:
  - assistant_models.py
  - assistant_repository.py
  - assistant_service.py
  - assistant_routes.py
- Frontend-MVC-Startmodule in webapp/public/js:
  - models/assistant.model.mjs
  - views/assistant.view.mjs
  - controllers/assistant.controller.mjs

Hinweis: Das Inkrement liefert eine sichere didaktische Hint-Basis. RAG, Voice und Avatar-Engine werden in den naechsten Phasen iterativ erweitert.

---

## 10. Wiederverwendung fuer andere Fachthemen

Die Anforderungsschablone ist fachneutral anwendbar, wenn folgende Parameter ausgetauscht werden:

- Fachdomaene und Kompetenzmodell
- Externe Referenzquellen
- Bewertungsrubriken
- Fachspezifische Sicherheits- und Compliance-Anforderungen

Template-Referenz:
- docs/handbuch/templates/ELEARNING-PFLICHTENHEFT-TEMPLATE.md

---

## 11. Abnahmekriterien fuer Inkrement 1

- Hint-Endpunkt erreichbar und validiert Eingaben robust.
- Assistent antwortet im Hint-Modus (keine Vollloesungen).
- Interaktionen werden append-only protokolliert.
- Frontend-MVC-Integration ist vorbereitet und fehlertolerant.
- Pflicht-Gates Security, Architecture, Docs laufen erfolgreich.

---

## 12. Changelog

- v1.0 (01.07.2026): Erstanlage fuer eLearning-Kurseditor mit RDB-LLM-Startarchitektur und Wiederverwendungsrahmen.
