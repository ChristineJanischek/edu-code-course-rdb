# Template-Sync für Schülerinnen und Schüler (vor jedem Start)

Nutze diese Kurzroutine immer **vor Arbeitsbeginn**, damit du mit der aktuellen Version arbeitest.

## Müssen Schüler aktiv etwas tun?

Ja, in den meisten Fällen kurz prüfen und aktualisieren.

- Wenn du direkt im Klassenrepository arbeitest: `git pull` reicht meistens.
- Wenn du in einem eigenen Fork arbeitest: zuerst Fork synchronisieren, dann lokal aktualisieren.
- Wenn Lehrkraft-Updates automatisch eingespielt wurden, musst du nur noch lokal nachziehen.

## 60-Sekunden-Routine vor jeder Stunde

1. Terminal im Projekt öffnen.
2. Auf `main` wechseln:
   ```bash
   git checkout main
   ```
3. Änderungen holen:
   ```bash
   git pull origin main
   ```
4. Prüfen, ob alles aktuell ist:
   ```bash
   git status -sb
   ```
5. Ergebnis lesen:
   - `## main...origin/main` ohne `behind` => aktuell.
   - `behind X` => nochmal `git pull origin main` ausführen.

## Falls du in einem eigenen Fork arbeitest

1. Auf GitHub deinen Fork öffnen.
2. Oben auf **Sync fork** klicken und bestätigen.
3. Danach lokal im Codespace/Terminal:
   ```bash
   git checkout main
   git pull origin main
   ```

## Wenn `git pull` wegen eigener Änderungen fehlschlägt

Nutze diesen sicheren Ablauf:

```bash
git add -A
git commit -m "WIP: mein Zwischenstand"
git pull --rebase origin main
```

Danach weiterarbeiten.

## Mindestregel

- **Immer vor dem Start syncen.**
- **Nicht** mit altem Stand in Aufgaben/Übungen starten.
- Bei Konflikten früh Lehrkraft fragen.
