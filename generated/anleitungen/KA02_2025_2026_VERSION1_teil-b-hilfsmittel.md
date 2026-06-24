# Hilfsmittel Teil B: EERM, Normalisierung und Anomalien

Diese Anleitung hilft dir, die Lösung schrittweise selbst zu erarbeiten. Sie ersetzt nicht das sachliche Lesen der Aufgabe, sondern zeigt dir die Reihenfolge der Gedanken.

## Ausgehend von diesen Quellen arbeiten

- [Aufgaben VERSION1](../klassenarbeiten/KA02_2025_2026_VERSION1_aufg.md)
- [Lösung VERSION1](../klassenarbeiten/KA02_2025_2026_VERSION1_lsg.md)
- [Grundlagen Modellierung](../informationen/teil-b/01_grundlagen_modellierung_eerm.md)
- [Kardinalitäten](../informationen/teil-b/02_kardinalitaeten_eine_saetze_mengenmaessig.md)
- [Normalisierung bis 3NF](../informationen/teil-b/03_normalisierung_bis_3nf.md)
- [Redundanzen](../informationen/teil-b/04_redundanzen.md)
- [Referentielle Integrität](../informationen/teil-b/05_referentielle_integritaet.md)
- [Stichwortverzeichnis Relationale Datenbanken](../informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.md)
- [Stichwortverzeichnis (suchbare HTML-Ansicht)](../informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.html)
- [Workbench-Workflow](../klassenarbeiten/WORKBENCH-MWB-WORKFLOW.md)

## 1. Sachverhalt in Fachbegriffe zerlegen

Lies den Text einmal nur fachlich. Markiere:

- Dinge, die als Entitätstypen infrage kommen
- Verben, die Beziehungen andeuten
- Eigenschaften, die als Attribute brauchbar sind
- Formulierungen wie mehrfach, gemeinsam, zu Terminen, im Team oder ohne aktive Zuordnung

Für diesen Kontext führen die wichtigsten Kandidaten typischerweise zu:

- Teilnehmende
- Kurse
- Termine
- Lehrkräfte
- Buchungen

## 2. Beziehungen mit Eine-Sätzen absichern

Nutze die Methode aus dem Informationsblatt zu Kardinalitäten:

- Eine Teilnehmende kann mehrere Buchungen haben.
- Eine Buchung gehört zu genau einer teilnehmenden Person.
- Ein Kurs hat mehrere Termine.
- Ein Termin gehört zu genau einem Kurs.
- Eine Lehrkraft kann mehrere Kurse betreuen.
- Ein Kurs kann im Team von mehreren Lehrkräften betreut werden.

Wenn du eine Beziehung in beide Richtungen mit mehreren Beteiligten formulieren kannst, prüfe zuerst eine n:m-Beziehung. Wenn eine Seite eindeutig genau eins ist, bleibt es bei 1:n.

## 3. Entitätstypen und Schlüssel festlegen

Arbeite erst die Fachstruktur aus, dann die Technik:

- Jeder Entitätstyp bekommt einen Primärschlüssel.
- Fachliche Namen bleiben lesbar und kurz.
- Vermeide doppelte Speicherung derselben Information.

Für das Modell bedeutet das:

- Stammdaten wie Name oder Titel gehören in den passenden Entitätstyp.
- Buchungsinformationen gehören in die Buchung.
- Terminbezogene Angaben gehören in den Termin.

Wenn dir bei Attributen etwas fehlt, ergänze nur das Nötige für die Fachlogik und die Auswertung. Nicht jedes denkbare Detail muss modelliert werden.

## 4. Das Modell in MySQL Workbench aufbauen

Baue das EERM in dieser Reihenfolge:

1. Entitätstypen anlegen
2. Primärschlüssel setzen
3. Beziehungen modellieren
4. Kardinalitäten eintragen
5. Nur dann Attribute ergänzen, wenn sie fachlich gebraucht werden

Für die Team-Betreuung gilt: Wenn ein Kurs von mehreren Lehrkräften betreut werden kann, dann muss die Beziehung zwischen Lehrkraft und Kurs fachlich als n:m gedacht werden. Eine Zwischentabelle oder Assoziation ist dann die saubere Lösung.

## 5. Normalisierung bis 3NF prüfen

Gehe mit den drei Prüfungen aus dem Infoblatt vor:

- 1NF: keine Listenwerte und keine zusammengesetzten Zellen
- 2NF: bei zusammengesetzten Schlüsseln müssen Nichtschlüsselattribute vom ganzen Schlüssel abhängen
- 3NF: keine transitiven Abhängigkeiten

Praktische Leitfrage:

- Steht eine Kurs- oder Lehrkraftinformation mehrfach in einer Buchung, ist das ein Warnsignal.
- Hängt ein Attribut nur indirekt über ein anderes Nichtschlüsselattribut ab, ist das kein 3NF-Zustand.

Als Kontrollidee kannst du diese funktionalen Abhängigkeiten prüfen:

- termin_id bestimmt kurs_id
- buchung_id bestimmt teilnehmer_id und termin_id

Wenn du solche Abhängigkeiten sauber trennen kannst, bist du auf dem richtigen Weg.

## 6. Redundanzen und Anomalien benennen

Nimm die drei Standardfragen aus dem Infoblatt:

- Welche Information würde mehrfach auftauchen?
- Was müsste bei einer Änderung an mehreren Stellen angepasst werden?
- Was geht verloren, wenn ein Datensatz gelöscht wird?

Beispielhafte Formulierung für die Lösung:

- Einfügeanomalie: Eine neue Fachinformation lässt sich nicht unabhängig anlegen.
- Änderungsanomalie: Ein Kursname müsste an vielen Stellen gleichzeitig korrigiert werden.
- Löschanomalie: Beim Löschen eines Vorgangs verschwinden fachlich wichtige Restinformationen mit.

## 7. Abschlusskontrolle vor der Abgabe

- Ist jeder Entitätstyp fachlich begründet?
- Sind alle Kardinalitäten mit Eine-Sätzen abgesichert?
- Gibt es keine doppelte Speicherung derselben Stammdaten?
- Sind die Fremdschlüsselbeziehungen fachlich nachvollziehbar?
- Ist die Modellierung unabhängig vom SQL-Teil gedacht?
