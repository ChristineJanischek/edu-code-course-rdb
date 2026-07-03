"""Zentrales Wissensmodul fuer Datenbankbegriffe im RDB-Kurs.

Single Source of Truth fuer:
  SYNONYMS      - Semantische Erweiterungen fuer die Stichwortsuche
  INSIGHT_CARDS - Wissensgraphen mit Syntax, SQL-Beispielen und
                  externen Quellen (related_sources)

Konventionen:
  - Schluessel in SYNONYMS: normalisierter Begriff (lowercase, getrimmt)
  - aliases in INSIGHT_CARDS: Menge von Begriffen, die die Karte ausloesen
  - related_sources: Liste von {"label": str, "url": str}
    url leer lassen, wenn kein externer Link verfuegbar ist
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Synonyme: Expandieren Suchbegriffe semantisch
# ---------------------------------------------------------------------------

SYNONYMS: dict[str, set[str]] = {
    "join": {"verbund", "verknuepfung", "verknüpfung", "tabellenverbund",
             "inner join", "left join", "outer join"},
    "left join": {"left outer join", "linker join", "optionaler verbund",
                   "null-werte", "outer join"},
    "from": {"quelltabelle", "basistabelle", "datenquelle", "aus tabelle"},
    "select from": {"abfragegrundgeruest", "grundgeruest", "projektion"},
    "normalisierung": {"1nf", "2nf", "3nf", "boyce-codd", "bcnf",
                       "anomalie", "normalform"},
    "3nf": {"normalisierung", "transitiv", "anomalie", "redundanz"},
    "kardinalitaet": {"kardinalität", "1:n", "n:m", "beziehung", "1:1"},
    "kardinalität": {"kardinalitaet", "1:n", "n:m", "beziehung"},
    "aggregation": {"group by", "having", "sum", "count", "avg", "min",
                    "max", "gruppierung"},
    "group by": {"aggregation", "gruppierung", "gruppenbildung", "count", "sum"},
    "group": {"aggregation", "having", "sum", "count"},
    "having": {"aggregation", "group by", "gruppenfilter"},
    "order": {"sortierung", "order by", "asc", "desc",
              "aufsteigend", "absteigend"},
    "order by": {"sortierung", "asc", "desc", "reihenfolge"},
    "distinct": {"eindeutig", "duplikat", "redundanz", "einzigartig"},
    "select": {"projektion", "spaltenauswahl", "abfrage"},
    "where": {"selektion", "filter", "bedingung", "vergleich", "like"},
    "insert": {"einfuegen", "hinzufuegen", "dml"},
    "update": {"aendern", "aktualisieren", "dml"},
    "delete": {"loeschen", "entfernen", "dml"},
    "subquery": {"unterabfrage", "subselect", "nested",
                 "verschachtelt", "in", "exists"},
    "fremdschluessel": {"fremdschlüssel", "foreign key", "fk",
                        "beziehung", "referenz"},
    "fremdschlüssel": {"fremdschluessel", "foreign key", "fk", "beziehung"},
    "primarschluessel": {"primärschlüssel", "primary key", "pk", "schluessel"},
    "primärschlüssel": {"primarschluessel", "primary key", "pk", "schlüssel"},
    "eerm": {"er-modell", "entitaetstyp", "entitaet",
             "attribut", "beziehungstyp"},
    "view": {"sicht", "virtuelle tabelle", "create view"},
    "index": {"btree", "performance", "optimierung"},
}

# ---------------------------------------------------------------------------
# Insight-Cards
# ---------------------------------------------------------------------------

INSIGHT_CARDS: tuple[dict, ...] = (
    {
        "key": "select-from",
        "category": "SQL-Klausel",
        "aliases": {"select", "from", "projektion", "quelltabelle",
                    "spaltenauswahl", "basistabelle", "select from"},
        "summary": (
            "SELECT bestimmt die Ausgabespalten, FROM die Datenquelle. "
            "Zusammen bilden beide Klauseln das Grundgeruest nahezu jeder "
            "SQL-Abfrage."
        ),
        "syntax": "SELECT spalte1, spalte2\nFROM tabelle;",
        "example_sql": (
            "SELECT truckname, kategorie\n"
            "FROM foodtrucks;"
        ),
        "example_view": (
            "CREATE VIEW v_foodtrucks_basis AS\n"
            "SELECT truckname, kategorie\n"
            "FROM foodtrucks;"
        ),
        "related_sources": [
            {
                "label": "W3Schools: SQL SELECT",
                "url": "https://www.w3schools.com/sql/sql_select.asp",
            },
            {
                "label": "W3Schools: SQL FROM",
                "url": "https://www.w3schools.com/sql/sql_ref_from.asp",
            },
            {
                "label": "Lokales Material: Projektion in SQL",
                "url": "/generated/informationen/teil-c/02_projektion_in_sql.html",
            },
        ],
    },
    {
        "key": "group-by",
        "category": "SQL-Klausel",
        "aliases": {"group by", "group", "aggregation", "gruppierung",
                    "having", "count", "sum", "avg"},
        "summary": (
            "GROUP BY verdichtet Datensaetze nach gemeinsamen Attributen "
            "und wird haeufig mit Aggregatfunktionen kombiniert."
        ),
        "syntax": (
            "SELECT spalte, AGGREGAT(feld) AS wert\n"
            "FROM tabelle\n"
            "GROUP BY spalte;"
        ),
        "example_sql": (
            "SELECT kunde_id, COUNT(*) AS buchungen_gesamt\n"
            "FROM buchung\n"
            "GROUP BY kunde_id\n"
            "HAVING COUNT(*) >= 2;"
        ),
        "example_view": (
            "CREATE VIEW v_buchungen_pro_kunde AS\n"
            "SELECT kunde_id, COUNT(*) AS buchungen_gesamt\n"
            "FROM buchung\n"
            "GROUP BY kunde_id;"
        ),
        "related_sources": [
            {
                "label": "W3Schools: SQL GROUP BY",
                "url": "https://www.w3schools.com/sql/sql_groupby.asp",
            },
            {
                "label": "MySQL Doku: GROUP BY",
                "url": "https://dev.mysql.com/doc/refman/8.0/en/group-by-handling.html",
            },
            {
                "label": "Lokales Material: Gruppierung in SQL",
                "url": "/generated/informationen/teil-c/06_gruppierung_in_sql.html",
            },
        ],
    },
    {
        "key": "having",
        "category": "SQL-Klausel",
        "aliases": {"having", "aggregation", "gruppenfilter", "sum", "count"},
        "summary": (
            "HAVING filtert Gruppen nach der Aggregation und ergaenzt "
            "GROUP BY, wenn Bedingungen auf Summen oder Anzahlen benoetigt "
            "werden."
        ),
        "syntax": (
            "SELECT spalte, COUNT(*) AS anzahl\n"
            "FROM tabelle\n"
            "GROUP BY spalte\n"
            "HAVING COUNT(*) > 1;"
        ),
        "example_sql": (
            "SELECT raum_id, COUNT(*) AS buchungen_gesamt\n"
            "FROM buchung\n"
            "GROUP BY raum_id\n"
            "HAVING COUNT(*) >= 3;"
        ),
        "example_view": (
            "CREATE VIEW v_stark_genutzte_raeume AS\n"
            "SELECT raum_id, COUNT(*) AS buchungen_gesamt\n"
            "FROM buchung\n"
            "GROUP BY raum_id\n"
            "HAVING COUNT(*) >= 3;"
        ),
        "related_sources": [
            {
                "label": "W3Schools: SQL HAVING",
                "url": "https://www.w3schools.com/sql/sql_having.asp",
            },
            {
                "label": "Lokales Material: Gruppierung in SQL",
                "url": "/generated/informationen/teil-c/06_gruppierung_in_sql.html",
            },
        ],
    },
    {
        "key": "left-join",
        "category": "SQL-Klausel",
        "aliases": {"left join", "left outer join", "linker join",
                    "outer join", "null-werte", "optionaler verbund"},
        "summary": (
            "LEFT JOIN liefert alle Zeilen der linken Tabelle und ergaenzt "
            "passende Daten der rechten Tabelle. Nicht passende rechte Werte "
            "erscheinen als NULL."
        ),
        "syntax": (
            "SELECT a.spalte, b.spalte\n"
            "FROM tabelle_a AS a\n"
            "LEFT JOIN tabelle_b AS b ON b.fk = a.id;"
        ),
        "example_sql": (
            "SELECT k.id, k.name, COUNT(b.id) AS buchungen_gesamt\n"
            "FROM kunde AS k\n"
            "LEFT JOIN buchung AS b ON b.kunde_id = k.id\n"
            "GROUP BY k.id, k.name\n"
            "ORDER BY k.name ASC;"
        ),
        "example_view": (
            "CREATE VIEW v_kunden_inkl_ohne_buchung AS\n"
            "SELECT k.id, k.name, COUNT(b.id) AS buchungen_gesamt\n"
            "FROM kunde AS k\n"
            "LEFT JOIN buchung AS b ON b.kunde_id = k.id\n"
            "GROUP BY k.id, k.name;"
        ),
        "related_sources": [
            {
                "label": "W3Schools: SQL LEFT JOIN",
                "url": "https://www.w3schools.com/sql/sql_join_left.asp",
            },
            {
                "label": "Lokales Material: SQL-Abfragen über mehrere Tabellen",
                "url": "/generated/informationen/teil-c/01_sql_abfragen_ueber_mehrere_tabellen.html",
            },
        ],
    },
    {
        "key": "join",
        "category": "SQL-Klausel",
        "aliases": {"join", "inner join", "left join", "verbund",
                    "verknuepfung", "verknüpfung", "tabellenverbund"},
        "summary": (
            "JOIN verbindet Datensaetze aus mehreren Tabellen ueber "
            "zusammenpassende Schluesselwerte."
        ),
        "syntax": (
            "SELECT a.spalte, b.spalte\n"
            "FROM tabelle_a AS a\n"
            "INNER JOIN tabelle_b AS b ON b.fk = a.id;"
        ),
        "example_sql": (
            "SELECT k.name, COUNT(b.id) AS buchungen_gesamt\n"
            "FROM kunde AS k\n"
            "LEFT JOIN buchung AS b ON b.kunde_id = k.id\n"
            "GROUP BY k.id, k.name;"
        ),
        "example_view": (
            "CREATE VIEW v_kunden_mit_buchungen AS\n"
            "SELECT k.id, k.name, COUNT(b.id) AS buchungen_gesamt\n"
            "FROM kunde AS k\n"
            "LEFT JOIN buchung AS b ON b.kunde_id = k.id\n"
            "GROUP BY k.id, k.name;"
        ),
        "related_sources": [
            {
                "label": "W3Schools: SQL JOIN",
                "url": "https://www.w3schools.com/sql/sql_join.asp",
            },
            {
                "label": "W3Schools: SQL LEFT JOIN",
                "url": "https://www.w3schools.com/sql/sql_join_left.asp",
            },
            {
                "label": "Lokales Material: SQL-Abfragen über mehrere Tabellen",
                "url": "/generated/informationen/teil-c/01_sql_abfragen_ueber_mehrere_tabellen.html",
            },
        ],
    },
    {
        "key": "where",
        "category": "SQL-Klausel",
        "aliases": {"where", "filter", "bedingung", "vergleich",
                    "like", "selektion"},
        "summary": (
            "WHERE schraenkt Zeilen vor einer Gruppierung oder Sortierung "
            "anhand von Bedingungen ein."
        ),
        "syntax": "SELECT spalten\nFROM tabelle\nWHERE bedingung;",
        "example_sql": (
            "SELECT titel, startdatum\n"
            "FROM kurs\n"
            "WHERE startdatum >= '2026-09-01' AND status = 'aktiv';"
        ),
        "example_view": (
            "CREATE VIEW v_aktive_kurse AS\n"
            "SELECT titel, startdatum\n"
            "FROM kurs\n"
            "WHERE startdatum >= '2026-09-01' AND status = 'aktiv';"
        ),
        "related_sources": [
            {
                "label": "W3Schools: SQL WHERE",
                "url": "https://www.w3schools.com/sql/sql_where.asp",
            },
            {
                "label": "Lokales Material: Selektion in SQL",
                "url": "/generated/informationen/teil-c/03_selektion_in_sql.html",
            },
        ],
    },
    {
        "key": "order-by",
        "category": "SQL-Klausel",
        "aliases": {"order by", "order", "sortierung", "asc", "desc",
                    "aufsteigend", "absteigend"},
        "summary": (
            "ORDER BY sortiert das Ergebnis aufsteigend (ASC) oder "
            "absteigend (DESC) nach einer oder mehreren Spalten."
        ),
        "syntax": "SELECT spalten\nFROM tabelle\nORDER BY spalte ASC|DESC;",
        "example_sql": (
            "SELECT name, geburtstag\n"
            "FROM schueler\n"
            "ORDER BY geburtstag DESC;"
        ),
        "example_view": "",
        "related_sources": [
            {
                "label": "W3Schools: SQL ORDER BY",
                "url": "https://www.w3schools.com/sql/sql_orderby.asp",
            },
            {
                "label": "Lokales Material: Selektion in SQL",
                "url": "/generated/informationen/teil-c/03_selektion_in_sql.html",
            },
        ],
    },
    {
        "key": "distinct",
        "category": "SQL-Klausel",
        "aliases": {"distinct", "eindeutig", "duplikat", "redundanz"},
        "summary": (
            "SELECT DISTINCT entfernt doppelte Zeilen aus dem "
            "Abfrageergebnis."
        ),
        "syntax": "SELECT DISTINCT spalte\nFROM tabelle;",
        "example_sql": "SELECT DISTINCT fach\nFROM lehrkraft_fach;",
        "example_view": "",
        "related_sources": [
            {
                "label": "W3Schools: SQL DISTINCT",
                "url": "https://www.w3schools.com/sql/sql_distinct.asp",
            },
            {
                "label": "Lokales Material: Redundanzen in Abfrageergebnissen",
                "url": "/generated/informationen/teil-c/07_redundanzen_in_abfrageergebnissen.html",
            },
        ],
    },
    {
        "key": "select",
        "category": "SQL-Grundlagen",
        "aliases": {"select", "projektion", "spaltenauswahl", "abfrage", "from"},
        "summary": (
            "SELECT bestimmt, welche Spalten im Ergebnis erscheinen "
            "(Projektion). Kombiniert mit FROM legt es die Quelltabelle fest."
        ),
        "syntax": "SELECT spalte1, spalte2\nFROM tabelle;",
        "example_sql": (
            "SELECT name, email\n"
            "FROM schueler\n"
            "WHERE klasse = '10A';"
        ),
        "example_view": (
            "CREATE VIEW v_schueler_10a AS\n"
            "SELECT name, email\n"
            "FROM schueler\n"
            "WHERE klasse = '10A';"
        ),
        "related_sources": [
            {
                "label": "W3Schools: SQL SELECT",
                "url": "https://www.w3schools.com/sql/sql_select.asp",
            },
            {
                "label": "Lokales Material: Projektion in SQL",
                "url": "/generated/informationen/teil-c/02_projektion_in_sql.html",
            },
        ],
    },
    {
        "key": "subquery",
        "category": "SQL-Fortgeschritten",
        "aliases": {"subquery", "unterabfrage", "subselect", "nested",
                    "in", "exists", "verschachtelt"},
        "summary": (
            "Eine Unterabfrage ist eine SELECT-Anweisung innerhalb einer "
            "anderen Abfrage (in WHERE, FROM oder SELECT eingebettet)."
        ),
        "syntax": (
            "SELECT spalte\n"
            "FROM tabelle\n"
            "WHERE spalte IN (SELECT spalte FROM andere_tabelle);"
        ),
        "example_sql": (
            "SELECT name\n"
            "FROM schueler\n"
            "WHERE id IN (\n"
            "  SELECT schueler_id\n"
            "  FROM teilnahme\n"
            "  WHERE kurs_id = 3\n"
            ");"
        ),
        "example_view": "",
        "related_sources": [
            {
                "label": "W3Schools: SQL Subquery",
                "url": "https://www.w3schools.com/sql/sql_subqueries.asp",
            },
        ],
    },
    {
        "key": "insert",
        "category": "SQL-DML",
        "aliases": {"insert", "einfuegen", "hinzufuegen", "dml",
                    "insert into"},
        "summary": "INSERT INTO fuegt neue Datensaetze in eine Tabelle ein.",
        "syntax": (
            "INSERT INTO tabelle (spalte1, spalte2)\n"
            "VALUES (wert1, wert2);"
        ),
        "example_sql": (
            "INSERT INTO schueler (name, email, klasse)\n"
            "VALUES ('Anna Muster', 'a.muster@schule.de', '10A');"
        ),
        "example_view": "",
        "related_sources": [
            {
                "label": "W3Schools: SQL INSERT",
                "url": "https://www.w3schools.com/sql/sql_insert.asp",
            },
            {
                "label": "Lokales Material: Daten einfügen",
                "url": "/generated/informationen/teil-c/08_daten_einfuegen.html",
            },
        ],
    },
    {
        "key": "update",
        "category": "SQL-DML",
        "aliases": {"update", "aendern", "aktualisieren", "dml"},
        "summary": (
            "UPDATE aendert bestehende Datensaetze. "
            "Ohne WHERE werden alle Zeilen veraendert."
        ),
        "syntax": (
            "UPDATE tabelle\n"
            "SET spalte = neuer_wert\n"
            "WHERE bedingung;"
        ),
        "example_sql": (
            "UPDATE schueler\n"
            "SET email = 'neu@schule.de'\n"
            "WHERE id = 42;"
        ),
        "example_view": "",
        "related_sources": [
            {
                "label": "W3Schools: SQL UPDATE",
                "url": "https://www.w3schools.com/sql/sql_update.asp",
            },
            {
                "label": "Lokales Material: Daten ändern",
                "url": "/generated/informationen/teil-c/09_daten_aendern.html",
            },
        ],
    },
    {
        "key": "delete",
        "category": "SQL-DML",
        "aliases": {"delete", "loeschen", "entfernen", "dml"},
        "summary": (
            "DELETE FROM loescht Datensaetze. "
            "Ohne WHERE werden alle Zeilen geloescht."
        ),
        "syntax": "DELETE FROM tabelle\nWHERE bedingung;",
        "example_sql": (
            "DELETE FROM buchung\n"
            "WHERE enddatum < '2026-01-01';"
        ),
        "example_view": "",
        "related_sources": [
            {
                "label": "W3Schools: SQL DELETE",
                "url": "https://www.w3schools.com/sql/sql_delete.asp",
            },
            {
                "label": "Lokales Material: Daten löschen",
                "url": "/generated/informationen/teil-c/10_daten_loeschen.html",
            },
        ],
    },
    {
        "key": "3nf",
        "category": "Normalisierung",
        "aliases": {"3nf", "normalisierung", "transitiv", "anomalie",
                    "2nf", "1nf", "normalform"},
        "summary": (
            "Die 3. Normalform trennt Attribute, die nur ueber ein "
            "Nichtschluesselattribut abhaengen, in eigene Tabellen aus."
        ),
        "syntax": (
            "Regel: Kein Nichtschluesselattribut darf transitiv "
            "vom Primaerschluessel abhaengen."
        ),
        "example_sql": (
            "-- Vor der Zerlegung\n"
            "student(student_id, kurs_id, kursname, dozent_name)\n\n"
            "-- Nach 3NF\n"
            "student(student_id, kurs_id)\n"
            "kurs(kurs_id, kursname, dozent_id)\n"
            "dozent(dozent_id, dozent_name)"
        ),
        "example_view": (
            "CREATE VIEW v_student_kurs_dozent AS\n"
            "SELECT s.student_id, k.kursname, d.dozent_name\n"
            "FROM student AS s\n"
            "INNER JOIN kurs AS k ON k.kurs_id = s.kurs_id\n"
            "INNER JOIN dozent AS d ON d.dozent_id = k.dozent_id;"
        ),
        "related_sources": [
            {
                "label": "Lokales Material: Normalisierung bis 3NF",
                "url": "/generated/informationen/teil-b/03_normalisierung_bis_3nf.html",
            },
        ],
    },
    {
        "key": "kardinalitaet",
        "category": "Modellierung",
        "aliases": {"kardinalitaet", "kardinalität", "1:n", "n:m",
                    "beziehung", "1:1"},
        "summary": (
            "Kardinalitaeten beschreiben, wie viele Datensaetze einer "
            "Entitaet mit Datensaetzen einer anderen Entitaet verbunden "
            "sein duerfen."
        ),
        "syntax": (
            "Beispiele: 1:1, 1:n, n:m.\n"
            "Eine n:m-Beziehung wird ueber eine Zwischentabelle aufgeloest."
        ),
        "example_sql": (
            "CREATE TABLE teilnahme (\n"
            "  schueler_id INT NOT NULL,\n"
            "  kurs_id INT NOT NULL,\n"
            "  PRIMARY KEY (schueler_id, kurs_id),\n"
            "  FOREIGN KEY (schueler_id) REFERENCES schueler(id),\n"
            "  FOREIGN KEY (kurs_id) REFERENCES kurs(id)\n"
            ");"
        ),
        "example_view": (
            "CREATE VIEW v_teilnahmen AS\n"
            "SELECT s.name AS schueler, k.titel AS kurs\n"
            "FROM teilnahme AS t\n"
            "INNER JOIN schueler AS s ON s.id = t.schueler_id\n"
            "INNER JOIN kurs AS k ON k.id = t.kurs_id;"
        ),
        "related_sources": [
            {
                "label": "Lokales Material: Kardinalitäten",
                "url": "/generated/informationen/teil-b/02_kardinalitaeten_eine_saetze_mengenmaessig.html",
            },
        ],
    },
    {
        "key": "eerm",
        "category": "Modellierung",
        "aliases": {"eerm", "er-modell", "entitaetstyp", "entitaet",
                    "attribut", "beziehungstyp", "modellierung"},
        "summary": (
            "Das Erweiterte Entity-Relationship-Modell (EERM) beschreibt "
            "Entitaetstypen, Attribute und Beziehungstypen als Grundlage "
            "relationaler Datenbankschemata."
        ),
        "syntax": (
            "Entitaetstyp: Rechteck\n"
            "Attribut: Ellipse\n"
            "Beziehungstyp: Raute"
        ),
        "example_sql": (
            "CREATE TABLE produkt (\n"
            "  id INT PRIMARY KEY AUTO_INCREMENT,\n"
            "  name VARCHAR(100) NOT NULL\n"
            ");\n"
            "CREATE TABLE kategorie (\n"
            "  id INT PRIMARY KEY AUTO_INCREMENT,\n"
            "  bezeichnung VARCHAR(60) NOT NULL\n"
            ");"
        ),
        "example_view": "",
        "related_sources": [
            {
                "label": "Lokales Material: EERM und Grundbegriffe",
                "url": "/generated/informationen/teil-b/01_grundlagen_modellierung_eerm.html",
            },
        ],
    },
    {
        "key": "fremdschluessel",
        "category": "Modellierung",
        "aliases": {"fremdschluessel", "fremdschlüssel", "foreign key",
                    "fk", "beziehung", "referenz",
                    "referentielle integritaet"},
        "summary": (
            "Ein Fremdschluessel referenziert den Primaerschluessel einer "
            "anderen Tabelle und sichert die referentielle Integritaet."
        ),
        "syntax": (
            "FOREIGN KEY (fk_spalte)\n"
            "  REFERENCES andere_tabelle(pk_spalte);"
        ),
        "example_sql": (
            "CREATE TABLE bestellung (\n"
            "  id INT PRIMARY KEY AUTO_INCREMENT,\n"
            "  kunde_id INT NOT NULL,\n"
            "  FOREIGN KEY (kunde_id) REFERENCES kunde(id)\n"
            "    ON DELETE RESTRICT\n"
            "    ON UPDATE CASCADE\n"
            ");"
        ),
        "example_view": "",
        "related_sources": [
            {
                "label": "W3Schools: SQL FOREIGN KEY",
                "url": "https://www.w3schools.com/sql/sql_foreignkey.asp",
            },
            {
                "label": "Lokales Material: Referentielle Integrität",
                "url": "/generated/informationen/teil-b/05_referentielle_integritaet.html",
            },
        ],
    },
)
