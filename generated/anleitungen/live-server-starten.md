# Live-Server starten

Diese Anleitung zeigt Schritt für Schritt, wie das Lernportal in diesem Repository lokal oder im Codespace gestartet wird.

## Ziel

Am Ende läuft die Weboberfläche im Browser über Port 8080.

Wichtig:

- Port 8080 ist die Weboberfläche.
- Port 8000 ist die Python-API.
- Port 3306 ist MySQL und kein Browser-Ziel.

## Schritt für Schritt

1. Terminal im Repository öffnen.
2. In das Projektverzeichnis wechseln:

```bash
cd /workspaces/edu-code-course-rdb
```

3. Falls nötig, die lokale Umgebung vorbereiten:

```bash
cp .env.example .env
```

4. In der Datei `.env` sichere Werte für `MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD` und `SUBMISSION_API_KEY` setzen.
5. Alle Dienste starten:

```bash
bash scripts/start-services.sh
```

6. Warten, bis im Terminal die Meldung erscheint, dass die Dienste gestartet wurden.
7. Die Weboberfläche öffnen:

```text
http://localhost:8080
```

8. Im GitHub Codespace stattdessen den weitergeleiteten Port 8080 öffnen.

Beispiel:

```text
https://CODESPACE-NAME-8080.app.github.dev
```
```text
Beispiel: https://silver-spork-v6w4x495v6wc6xj4-8080.app.github.dev
```

## Funktion prüfen

Optional kann anschließend geprüft werden, ob alle Dienste korrekt antworten:

```bash
bash scripts/test-services.sh
```

## Fehlerbehebung

### Im Browser erscheint eine Fehlermeldung

- Prüfen, ob wirklich Port 8080 geöffnet wurde.
- Nicht Port 3306 im Browser verwenden.
- Falls der Start abbricht, die Werte in `.env` prüfen.

### Die API antwortet, aber die Webseite nicht

- Prüfen, ob der Container `php-web` läuft.
- Prüfen, ob Port 8080 im Codespace freigegeben ist.

### Die Dienste sollen neu gestartet werden

```bash
bash scripts/stop-services.sh
bash scripts/start-services.sh
```