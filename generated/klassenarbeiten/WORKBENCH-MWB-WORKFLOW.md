# Workflow: MWB-Dateien direkt aus SQL erzeugen

Diese Datei wurde automatisch erzeugt mit:

`bash scripts/prepare-workbench-mwb.sh`

Die Generierung laeuft ohne MySQL Workbench. Sie liest die SQL-Strukturdumps, baut daraus native MWB-Archive und verwendet fuer die Containerstruktur eine Referenzvorlage aus dem Repository.

## 1) Erzeugte Modelle

| System | Schema | Quelle | Ziel-.mwb |
|---|---|---|---|
| kursplattform | kursplattform | generated/klassenarbeiten/KA02_BG12_2025_2026_VERSION1_lsg.md | generated/klassenarbeiten/kursplattform_2025.mwb |

## 2) Validierung

Die erzeugten Archive enthalten intern `document.mwb.xml`, `lock` und `@db/data.db`.

Beispielpruefung:

`bash scripts/validate-mwb-native.sh`
