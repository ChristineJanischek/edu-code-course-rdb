# Lehrplanbasierte Inhaltserweiterung für relationale Datenbanken

## Zweck

Dieses Dokument beschreibt, wie neue Lehrpläne und curriculare Vorgaben für das Fachthema relationale Datenbanken in diesem Repository verarbeitet, analysiert und in neue Lernpfade, Aufgaben, Lösungen und Webapp-Inhalte überführt werden.

Der Geltungsbereich ist bewusst auf relationale Datenbanken begrenzt:

- EERM und fachliche Modellierung
- 1. bis 3. Normalform
- SQL-DDL und SQL-DML
- SELECT, JOIN, GROUP BY, HAVING, Unterabfragen
- fachliche Begründungen und Reflexion

## Verbindliche Ablageorte

- Lehrpläne und Bildungspläne: `uploads/lehrplaene/`
- Prüfungsaufgaben, Erwartungshorizonte, Referenzmaterial: `uploads`uploads/pruefungsaufgaben-und-erwartungshorizonte-fuer-ki-training/`vmaterial für Unterricht und Klassenarbeiten: `uploads/klassenarbeiten-und-unterrichtsmaterialien/`

Neue Lehr`uploads/klassenarbeiten-und-unterrichtsmaterialien/`is abgelegt werden.

## Zielbild

Neue curriculare Quellen sollen künftig systematisch zu didaktisch sinnvollen Inhalten führen:

- neue Lernpfade in der Webapp
- neue praxisnahe Sachverhalte
- neue Übungsaufgaben mit Hilfen und Selbstkontrolle
- neue Musterlösungen mit fachlicher Begründung
- neue SQL- und EERM-Testfälle für die technische Lernumgebung

## Empfohlenes Verfahren

## 1. Kein Fine-Tuning als Standard

Für dieses Repository ist ein klassisches Fine-Tuning eines Sprachmodells nicht das beste Primärverfahren.

Gründe:

- Lehrpläne ändern sich punktuell und müssen schnell nachpflegbar sein.
- Nachvollziehbarkeit und Quellenbezug sind wichtiger als ein opakes Modellverhalten.
- Die Domäne ist schmal und profitiert stark von guter Retrieval-Qualität plus klaren Regeln.

## 2. Empfohlenes Modell

Empfohlen wird ein retrieval-gestütztes Verfahren mit mehrsprachigen Embeddings.

Geeignete Wahl:

- Embedding-Modell: `BAAI/bge-m3`

Begründung:

- stark für mehrsprachige Inhalte, auch deutschsprachige Lehrpläne
- robust `BAAI/bge-m3`he Suche über Kompetenzformulierungen, Operatoren und Inhaltsfelder
- gut geeignet für Chunk-Retrieval aus PDFs, Handbuchtexten und vorhandenen Aufgabenbeständen

## 3. Empfohlenes Verfahren

Empfohlen wird ein hybrides Verfahren aus:

- regelbasierter Vorverarbeitung
- Curriculum-Chunking
- Embedding-Retrieval
- didaktischer Template-Ableitung
- fachlicher Validierung gegen SQL-/EERM-Kriterien

Kurzform:

1. Lehrplan in sinnvolle Abschnitte zerlegen
2. Abschnitte mit Embeddings indexieren
3. bestehende Inhalte und Aufgaben semantisch dagegen matchen
4. Lücken und Überdeckungen identifizieren
5. neue Inhalte über didaktische Templates generieren
6. fachlich und technisch validieren

Das ist ein RAG-Ansatz mit curricularer Steuerung, nicht ein freies Generieren ohne Leitplanken.

## Verarbeitungsworkflow

## Schritt 1: Neue Quelle ablegen

Neue curriculare PDFs werden nach `uploads/lehrplaene/` gelegt.

Der erste Import erfolgt mit:

```bash
python3 scripts/import_curriculum_pdf.py
```

Dabei entstehen strukturier`uploads/lehrplaene/`er `generated/lehrplaene/`.

Namensregel:

- bestehende sprechende Dateinamen beibehalten
- Jahrgang oder Fassung n`generated/lehrplaene/`derlich
- keine Umbenennung in generische Dateinamen

## Schritt 2: Quelle fachlich zerlegen

Aus dem Dokument werden Abschnitte extrahiert, zum Beispiel:

- Kompetenzen
- Inhaltsfelder
- Operatoren
- Anforderungsniveaus
- Prüfungsrelevante Formulierungen

Jeder Abschnitt wird als eigener Chunk behandelt.

## Schritt 3: Curriculare Tags ableiten

Jeder Chunk erhält strukturierte Tags, zum Beispiel:

- `eerm`
- `normalisierung`
- `3nf`
- `sql-select`
- `sql-from`
- `sql-join`
- `sql-where`
- `sql-group-by`
- `sql-having`
- `sql-order-by`
- `begruendung`
- `pruefungsvorbereitung`

Achte darauf, dass die Tags konsistent mit der Stichwortsuche und den LLM-Hinweiskarten gepflegt werden.

## Schritt 5: Lückenanalyse

Typische Fragen:

- Welche Kompetenzen sind curricular gefordert, aber in der Webapp noch nicht sichtbar?
- Welche SQL-Muster fehlen noch?
- Gibt es für 3NF und EERM genug praktisch orientierte Sachverhalte?
- Gibt es Selbstkontrolle und Hilfsmittel für alle Kompetenzstufen?

## Schritt 6: Didaktische Ableitung

Neue Inhalte müssen didaktisch sinnvoll sein. Deshalb gilt:

- vom Verstehen zum Modellieren
- vom Modellieren zur Normalisierung
- von der Struktur zur Abfrage
- von einfachen zu komplexeren SQL-Sichten
- immer mit fachlicher Begründung

Jeder neue Inhalt soll enthalten:

- einen realitätsnahen Sachverhalt
- klare Lernziele
- benötigte Vorwissenshinweise
- einen Übungsauftrag
- Selbstkontrolle
- Tipps oder Lösungshinweise
- eine fachlich belastbare Musterlösung

## Qualitätskriterien für neue Sachverhalte

Neue Sachverhalte sollen praktisch, interessant und fachlich sauber sein.

Geeignete Kontexte sind zum Beispiel:

- Lernlabor
- Coworking-Campus
- Foodtruck-Netz
- Bibliothek
- Veranstaltungsmanagement
- Schulische Materialausgabe
- Sportturnier-Verwaltung

Nicht geeignet sind Kontexte, die nur künstlich Tabellen produzieren, ohne echte fachliche Beziehungen oder sinnvolle Normalisierungsargumente.

## Regeln für die Webapp-Erweiterung

Neue Inhalte in der Webapp sollen folgende Bausteine unterstützen:

- Lernpfad mit nachvollziehbarer Reihenfolge
- Infoboxen für Begriffe, Regeln und Fehlerquellen
- Code-Inboxen für SQL und fachliche Begründungen
- sofortige Selbstkontrolle
- konstruktives Feedback
- Hinweise auf Hilfsmittel und Zwischenschritte

Das Feedback muss:

- lösungsorientiert sein
- keine internen Fehlerdetails offenlegen
- fehlende Bausteine konkret benennen
- zum nächsten sinnvollen Schritt führen

## OOP- und Architekturregeln

Bei zukünftigen Implementierungen gilt:

- fachliche Regeln in eigenständige Klassen oder Services kapseln
- curriculare Analyse von UI-Logik trennen
- keine Copy-Paste-Logik für mehrere Aufgabenformate
- gemeinsame Evaluationslogik zentral halten
- Eingaben immer validieren und Ausgaben escapen

## Definition of Done

Eine curriculare Erweiterung ist erst fertig, wenn:

- der neue Lehrplan unter `uploads/lehrplaene/` liegt
- neue oder angepasste Webapp-Inhalte sichtbar sind
- neue Aufgaben und Lösungen fa`uploads/lehrplaene/`iegen
- Handbuch und Betriebsdoku aktualisiert sind
- die Pflicht-Validierungen erfolgreich laufen:

```bash
bash scripts/validate-security.```bash
bash scripts/validate-security.sh
bash scripts/validate-architecture.sh
bash scripts/validate-docs.sh
```](../README.md)
- [INDEX.md](../INDEX.md)
- [ARCHITEKTUR.md](../AR``ITEKTUR.md)
- [PFLICHTENHEFT.md](../PFLICHTENHEFT.md)
- [rdb-live-test-und-webserver-setup.md](../anleitungen/rdb-live-test-und-webserver-setup.md)
