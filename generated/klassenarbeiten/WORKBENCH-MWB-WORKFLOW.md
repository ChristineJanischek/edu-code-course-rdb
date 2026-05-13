# Workflow: Echte MySQL Workbench .mwb aus SQL erzeugen

Diese Datei wurde automatisch erzeugt mit:

`bash scripts/prepare-workbench-mwb.sh`

FK-/Index-Muster-Normalisierung: aktiv

## 1) Vorbereitete Datenbankschemata

| System | Jahr | Schema fuer Reverse Engineering | Charset | Collation | Tabellen | Struktur-SQL | Daten-SQL | Ziel-.mwb |
|---|---:|---|---|---|---:|---|---|---|
| coworkingcampus | 2025 | wb_coworkingcampus_2025 | utf8 | utf8_general_ci | 6 | generated/klassenarbeiten/coworkingcampus_struktur_2025.sql | generated/klassenarbeiten/coworkingcampus_daten_2025.sql | generated/klassenarbeiten/coworkingcampus_2025.mwb |
| foodtrucknetz | 2025 | wb_foodtrucknetz_2025 | utf8 | utf8_general_ci | 6 | generated/klassenarbeiten/foodtrucknetz_struktur_2025.sql | generated/klassenarbeiten/foodtrucknetz_daten_2025.sql | generated/klassenarbeiten/foodtrucknetz_2025.mwb |
| stadtfahrradverleih | 2025 | wb_stadtfahrradverleih_2025 | utf8 | utf8_general_ci | 6 | generated/klassenarbeiten/stadtfahrradverleih_struktur_2025.sql | generated/klassenarbeiten/stadtfahrradverleih_daten_2025.sql | generated/klassenarbeiten/stadtfahrradverleih_2025.mwb |

## 2) Schritte in MySQL Workbench (pro System)

1. Workbench starten.
2. Verbindung anlegen/waehlen mit diesen Parametern:
   - Hostname: 127.0.0.1
   - Port: 3306
   - Username: root
3. Menue: `Database -> Reverse Engineer...`
4. Das passende Schema aus der Tabelle oben auswaehlen.
5. Import abschliessen, dann im Modell auf EER-Diagramm wechseln.
6. Notation setzen: `Model -> Relationship Notation -> Connect to Columns` (wenn verfuegbar).
7. Speichern: `File -> Save Model As...` und die Datei auf den jeweiligen Ziel-.mwb-Pfad speichern.

## 3) Validierung einer echten .mwb

Eine echte Workbench-Datei enthaelt intern die Datei `document.mwb.xml`.

Beispielpruefung:

`unzip -l <datei>.mwb | grep document.mwb.xml`

Wenn kein Treffer kommt, ist die Datei kein natives Workbench-Modell.
