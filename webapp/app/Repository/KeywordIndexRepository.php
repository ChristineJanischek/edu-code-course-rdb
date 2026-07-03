<?php

declare(strict_types=1);

/**
 * Repository fuer alle lernbaren Stichwort-Eintraege des Portals.
 *
 * Single Source of Truth fuer den Keyword-Index.
 * Eintraege verweisen auf konkretes Lernmaterial aus /generated/.
 * Der title-Wert wird clientseitig fuer die lokale Stichwortsuche genutzt;
 * er sollte den SQL-Begriff oder Fachbegriff direkt enthalten.
 */
final class KeywordIndexRepository
{
    /**
     * Gibt alle Stichwort-Eintraege zurueck.
     *
     * @return list<array{topic: string, title: string, href: string}>
     */
    public function findAll(): array
    {
        return [
            // --- SQL-Aggregation ---
            [
                'topic' => 'SQL-Aggregation',
                'title' => 'GROUP BY Gruppierung',
                'href'  => '/generated/informationen/teil-c/06_gruppierung_in_sql.html',
            ],
            [
                'topic' => 'SQL-Aggregation',
                'title' => 'HAVING Gruppenfilter',
                'href'  => '/generated/informationen/teil-c/06_gruppierung_in_sql.html',
            ],
            [
                'topic' => 'SQL-Aggregation',
                'title' => 'COUNT SUM AVG MIN MAX Aggregatfunktionen',
                'href'  => '/generated/informationen/teil-c/04_funktionen_in_sql.html',
            ],
            // --- SQL-Verbund ---
            [
                'topic' => 'SQL-Verbund',
                'title' => 'JOIN INNER JOIN LEFT JOIN Tabellenverbund',
                'href'  => '/generated/informationen/teil-c/01_sql_abfragen_ueber_mehrere_tabellen.html',
            ],
            // --- SQL-Filter ---
            [
                'topic' => 'SQL-Filter',
                'title' => 'WHERE Selektion Bedingung LIKE',
                'href'  => '/generated/informationen/teil-c/03_selektion_in_sql.html',
            ],
            [
                'topic' => 'SQL-Filter',
                'title' => 'ORDER BY Sortierung ASC DESC',
                'href'  => '/generated/informationen/teil-c/03_selektion_in_sql.html',
            ],
            // --- SQL-Grundlagen ---
            [
                'topic' => 'SQL-Grundlagen',
                'title' => 'SELECT Projektion Spaltenauswahl',
                'href'  => '/generated/informationen/teil-c/02_projektion_in_sql.html',
            ],
            [
                'topic' => 'SQL-Grundlagen',
                'title' => 'DISTINCT Duplikate entfernen Redundanz',
                'href'  => '/generated/informationen/teil-c/07_redundanzen_in_abfrageergebnissen.html',
            ],
            [
                'topic' => 'SQL-Grundlagen',
                'title' => 'Datumsfunktionen DATE YEAR MONTH',
                'href'  => '/generated/informationen/teil-c/05_datum_funktionen_in_datenbankabfragen_sql.html',
            ],
            // --- SQL-DML ---
            [
                'topic' => 'SQL-DML',
                'title' => 'INSERT INTO Daten einfuegen',
                'href'  => '/generated/informationen/teil-c/08_daten_einfuegen.html',
            ],
            [
                'topic' => 'SQL-DML',
                'title' => 'UPDATE SET Daten aendern',
                'href'  => '/generated/informationen/teil-c/09_daten_aendern.html',
            ],
            [
                'topic' => 'SQL-DML',
                'title' => 'DELETE FROM Daten loeschen',
                'href'  => '/generated/informationen/teil-c/10_daten_loeschen.html',
            ],
            // --- Normalisierung ---
            [
                'topic' => 'Normalisierung',
                'title' => '3NF Normalform Abhaengigkeiten transitiv',
                'href'  => '/generated/informationen/teil-b/03_normalisierung_bis_3nf.html',
            ],
            [
                'topic' => 'Normalisierung',
                'title' => 'Redundanzen Anomalien erkennen',
                'href'  => '/generated/informationen/teil-b/04_redundanzen.html',
            ],
            // --- Modellierung ---
            [
                'topic' => 'Modellierung',
                'title' => 'EERM Entitaetstyp Attribut Beziehungstyp',
                'href'  => '/generated/informationen/teil-b/01_grundlagen_modellierung_eerm.html',
            ],
            [
                'topic' => 'Modellierung',
                'title' => 'Kardinalitaet 1:n n:m Beziehung',
                'href'  => '/generated/informationen/teil-b/02_kardinalitaeten_eine_saetze_mengenmaessig.html',
            ],
            [
                'topic' => 'Modellierung',
                'title' => 'Fremdschluessel Referentielle Integritaet Foreign Key',
                'href'  => '/generated/informationen/teil-b/05_referentielle_integritaet.html',
            ],
            // --- Uebersichten & Uebungen ---
            [
                'topic' => 'Stichwortverzeichnis',
                'title' => 'SQL-Klausel-Kompass RDB-Begriffe',
                'href'  => '/generated/informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.html',
            ],
            [
                'topic' => 'Uebungen',
                'title' => 'UE01 Foodtrucknetz SQL-Abfragen',
                'href'  => '/generated/uebungen/UE01_foodtrucknetz_sql_abfragen.html',
            ],
            [
                'topic' => 'Uebungen',
                'title' => 'UE02 Stadtfahrradverleih SQL-Abfragen',
                'href'  => '/generated/uebungen/UE02_stadtfahrradverleih_sql_abfragen.html',
            ],
        ];
    }
}
