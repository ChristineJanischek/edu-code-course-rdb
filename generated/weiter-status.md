# Weiter-Statusbericht

Zeitpunkt (UTC): 2026-07-11T15:04:25Z

## Repo-Stand

- Branch: main
- Letzter Commit: 7bc6380 chore: sichern aktueller arbeitsstand
- Working Tree: dirty
- Ahead/Behind gegen Upstream: ahead=0	0, behind=0	0

## Auto-Erkennung nach Marschplan

- M1 Baseline gesichert: no
- M2 Hint-Modus (API + UI): no
- M3 Wissensanbindung (Suche + Quellen): no
- M4 Audit-Trail: no
- M5 Lehrkraft-Features Fundament: no

## Analyse-Dimensionen

### Best Practice
- SSOT-Dokumentation und Pflicht-Gates weiterhin als Abschlussregel verwenden.
- Aenderungen nur in klar getrennten Schichten (Route/Service/Repository/UI).

### Prozess
- Naechster Milestone wird datenbasiert aus Marker-Status ermittelt.
- Jeder Lauf erzeugt einen neuen Statusbericht als Audit-Artefakt.

### Zuordnung (Core vs Course)
- Core: wiederverwendbare Assistentenlogik, Sicherheitsregeln, Logging, Rollenmodell.
- Course: fachspezifische Inhalte, Aufgabenkarten, didaktische Beispiele.

### Usability
- Funktionen pro Arbeitsprozess gruppieren (nicht pro Technikmodul).
- Neue Funktionen zuerst in bestehende Reiter/Views einordnen, neue Hauptreiter nur bei klarer Eigenstaendigkeit.

## Naechster Milestone

M1 Baseline sichern

## Naechste Schritte

- Lokale Aenderungen committen und pushen.
- Optionalen Snapshot-Tag setzen.
- Danach erneut `bash scripts/weiter.sh` ausfuehren.

## Sinnvolle Testvorschlaege fuer den naechsten Zyklus

- API-Tests: Hint-Endpunkt, Keyword-Search, Fehlerpfade.
- UI-Smoke: Laden, Weiter-Navigation, Lernhilfe, Stichwortsuche.
- Sicherheits-Checks: SQL-Sandbox-Write-Blocker, Input-Validierung, Fehlerausgaben.
- Pflicht-Gates: [security] Starte Sicherheitsvalidierung...
[security] Sicherheitsvalidierung erfolgreich, [arch] Starte Architekturvalidierung...
[java] Kompilierung erfolgreich
[java] Starte Headless-Modell-Smoke-Tests...
[java-model-test] Starte Volleyball-Modell-Smoke-Tests...
------------------------------------------------------------
  PASS  Startaufstellung hat 6 Spieler
  PASS  Erster Spieler ist Armin
  PASS  Ersatzbank hat 6 Spieler
  PASS  Erster Ersatzspieler ist Chris
  PASS  Kader hat 12 Spieler gesamt
  PASS  Nach Tausch ist Index 0 = Batu
  PASS  Nach Tausch ist Index 1 = Armin
  PASS  Nach Einfuegen hat Startaufstellung 7 Spieler
  PASS  Eingefuegter Spieler ist an Position 0
  PASS  Kader enthaelt Kaderspieler-Typ an Position 0
  PASS  Kader enthaelt Ersatzspieler-Typ an Position 6
  PASS  Ungueltiger Tausch wirft keine Exception
  PASS  holeSpielerliste(99) gibt leere Liste zurueck
------------------------------------------------------------
[java-model-test] Ergebnis: 13 bestanden, 0 fehlgeschlagen
[java-model-test] Alle Tests erfolgreich
[java] Modell-Tests erfolgreich
[arch] Architekturvalidierung erfolgreich, [docs] Starte Dokumentationsvalidierung...
[content-db] CHECK: contexts=4, duplicates=0
[content-db] OK
[html-sync] NEEDS-FIX: generated/weiter-status-history/weiter-status-20260711-150425.md -> generated/weiter-status-history/weiter-status-20260711-150425.html
[html-sync] FAIL: generated HTML documentation is not synchronized
[html-sync] HINT: bash scripts/sync-generated-html.sh
[docs] FAIL: HTML-Exporte aus Markdown oder Stoffverlaufsplan sind nicht synchron
[docs] HINT: bash scripts/sync-generated-html.sh.
