# Classroom-Anleitung: weiter-Routine fuer Schueler

Version: 1.0
Status: Aktiv
Gueltig ab: 11.07.2026

---

## Zielgruppe

Schuelerinnen und Schueler, die im Classroom KI-gestuetzt den Entwicklungsstand im Repo nachvollziehen und den naechsten Lern- und Umsetzungsschritt selbststaendig bearbeiten.

---

## Ziel der Routine

Mit dem Stichwort weiter wird der aktuelle Stand ermittelt, ein sinnvoller naechster Schritt vorgeschlagen und als nachvollziehbarer Lernprozess abgearbeitet.

---

## Didaktischer Ablauf in Schritten

| Schritt | Ausgangspunkt | Ziel | Zweck |
|---|---|---|---|
| 1. Orientierung | Der aktuelle Arbeitsstand ist unklar. | Den Stand sichtbar machen. | Lernende verstehen, wo sie im Prozess stehen. |
| 2. Statuslauf | Das Repo ist geoeffnet. | `bash scripts/weiter.sh` ausfuehren und Status lesen. | Objektive Standortbestimmung statt Bauchgefuehl. |
| 3. Milestone verstehen | Ein naechster Milestone wird angezeigt. | Milestone in eigene Worte uebersetzen. | Fachsprachliche und prozessuale Sicherheit aufbauen. |
| 4. KI-Vorschlag nutzen | Es gibt naechste Schritte und Testvorschlaege. | Einen Teilschritt auswaehlen und planen. | Selbststeuerung und Priorisieren trainieren. |
| 5. Umsetzen | Geplanter Teilschritt liegt vor. | Skript/Routine ausfuehren und Artefakt erzeugen. | Handlungsorientiertes Lernen mit sichtbarem Ergebnis. |
| 6. Reflexion | Artefakt wurde erzeugt. | Ergebnis gegen Ziel und Zweck pruefen. | Qualitaetsbewusstsein und Fehlerkultur foerdern. |
| 7. Qualitaetscheck | Aenderungen sind lokal vorhanden. | Pflichtchecks starten. | Sicherheits- und Architekturstandards einhalten. |
| 8. Abschluss | Checks sind gruen. | Commit und Push dokumentieren. | Verbindliche Arbeitsweise wie im Teamkontext ueben. |

---

## Konkrete Befehlsfolge fuer Schueler

1. `bash scripts/weiter.sh`
2. Einen vorgeschlagenen Teilschritt auswaehlen (z. B. Intake, Routing, To-do, Kontext, Milestone)
3. Teilschritt ausfuehren:
   - `bash scripts/teacher-ui-intake.sh --id TUI-001`
   - `bash scripts/teacher-ui-routing.sh --id TUI-002`
   - `bash scripts/teacher-ui-todo.sh --id TUI-003`
   - `bash scripts/teacher-ui-context.sh --id TUI-004`
   - `bash scripts/teacher-ui-milestone.sh --id TUI-005`
4. `bash scripts/sync-generated-html.sh --write`
5. `bash scripts/validate-security.sh`
6. `bash scripts/validate-architecture.sh`
7. `bash scripts/validate-docs.sh`

---

## Lehrplanrelevante Kompetenzen

- Prozesskompetenz: Arbeitsablaeufe planen, ausfuehren, reflektieren
- Fachkompetenz: Datenbank- und KI-bezogene Teilschritte begruendet anwenden
- Urteilskompetenz: Vorschlaege bewerten und priorisieren
- Methodenkompetenz: Qualitaetschecks, Dokumentation und Versionierung nutzen

---

## Erfolgskriterien fuer Schueler

1. Der naechste Schritt wird aus dem Report korrekt abgeleitet.
2. Mindestens ein passendes Artefakt wird erzeugt.
3. Die drei Pflichtchecks laufen erfolgreich.
4. Der Schritt wird kurz reflektiert: Was war Ausgangspunkt, Ziel und Zweck?

---

## Reflexionsfragen fuer den Unterricht

1. Welchen Ausgangspunkt hat der Report gezeigt?
2. Warum war der gewaehlte Schritt didaktisch sinnvoll?
3. Welche KI-Vorschlaege waren hilfreich, welche nicht?
4. Was wuerdet ihr am naechsten Durchlauf verbessern?

---

## Changelog

- v1.0 (11.07.2026): Erstanlage der Classroom-Anleitung mit didaktischer Schrittstruktur nach Ausgangspunkt, Ziel und Zweck.
