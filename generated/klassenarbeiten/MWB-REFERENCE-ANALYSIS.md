# MWB Reference Analysis

Ausgewertet wurden native MySQL-Workbench-Archive aus dem Referenzordner.

## Ableitbare Generatorregeln

- Native Archive enthalten `document.mwb.xml`, `lock`lock`PROTECT_2__b`.
- Die Referenzmodelle verwende`utf8`PROTECT_4__neral_ci`.
- Das sichtbare Nutzschema ist vom leeren Workb`mydb`mydb`-Schema getrennt.
- Tabellen besitzen PRIMARY-Indexes und zu Fremdschluesseln passende Zusatzindizes.

## betreuung.mwb

Archive-Entries:
- @db/data.db
- document.mwb.xml
- lock

- Schema: mydb
  - Charset: utf8
  - Collation: utf8_general_ci
  - Tabellen: 0
- Schema: moebelhaus
  - Charset: (leer)
  - Collation: (leer)
  - Tabellen: 5
    - kinder: columns=4, fks=1, indices=2
      - Spalten: idKind, name, vorname, Kunde_idKunde
      - FKs: fk_Kind_Kunde1
      - Indizes: PRIMARY, fk_Kind_Kunde1_idx
    - kunden: columns=4, fks=0, indices=1
      - Spalten: idKunde, name, vorname, mobil
      - Indizes: PRIMARY
    - aktivitaeten: columns=2, fks=0, indices=1
      - Spalten: idAktivitaet, bezeichnung
      - Indizes: PRIMARY
    - betreuungen: columns=1, fks=0, indices=1
      - Spalten: idBetreuung
      - Indizes: PRIMARY
    - teilnahmen: columns=3, fks=3, indices=4
      - Spalten: Kind_idKind, Betreuung_idBetreuung, Aktivitaet_idAktivitaet
      - FKs: fk_Kind_has_Betreuung_Kind, fk_Kind_has_Betreuung_Betreuung1, fk_Kind_has_Betreuung_Aktivitaet1
      - Indizes: PRIMARY, fk_Kind_has_Betreuung_Betreuung1_idx, fk_Kind_has_Betreuung_Kind_idx, fk_Kind_has_Betreuung_Aktivitaet1_idx

## freizeitpark.mwb

Archive-Entries:
- @db/data.db
- document.mwb.xml
- lock

- Schema: mydb
  - Charset: utf8
  - Collation: utf8_general_ci
  - Tabellen: 0
- Schema: eurowater
  - Charset: (leer)
  - Collation: (leer)
  - Tabellen: 5
    - attraktion: columns=6, fks=2, indices=3
      - Spalten: idattraktion, bezeichnung, mindestgroesse, mindestalter, kategorie_nummer, themenbereich_idthemenbereich
      - FKs: fk_attraktion_kategorie, fk_attraktion_themenbereich1
      - Indizes: PRIMARY, fk_attraktion_kategorie_idx, fk_attraktion_themenbereich1_idx
    - besucher: columns=4, fks=0, indices=1
      - Spalten: idbesucher, vorname, nachname, geburtsdatum
      - Indizes: PRIMARY
    - kategorie: columns=2, fks=0, indices=1
      - Spalten: nummer, kateogoriename
      - Indizes: PRIMARY
    - themenbereich: columns=2, fks=0, indices=1
      - Spalten: idthemenbereich, thema
      - Indizes: PRIMARY
    - Besuchsposition: columns=2, fks=2, indices=3
      - Spalten: attraktion_idattraktion, besucher_idbesucher
      - FKs: fk_attraktion_has_besucher_attraktion1, fk_attraktion_has_besucher_besucher1
      - Indizes: PRIMARY, fk_attraktion_has_besucher_besucher1_idx, fk_attraktion_has_besucher_attraktion1_idx

## parkplaetze.mwb

Archive-Entries:
- @db/data.db
- document.mwb.xml
- lock

- Schema: mydb
  - Charset: utf8
  - Collation: utf8_general_ci
  - Tabellen: 0
- Schema: freizeitpark_parkplatz
  - Charset: (leer)
  - Collation: (leer)
  - Tabellen: 4
    - parklatz: columns=3, fks=1, indices=2
      - Spalten: prakplatzNr, preis, kategorie_idkategorie
      - FKs: fk_parklatz_kategorie1
      - Indizes: PRIMARY, fk_parklatz_kategorie1_idx
    - fahrzeug: columns=3, fks=0, indices=1
      - Spalten: idfahrzeug, kennzeichen, breite
      - Indizes: PRIMARY
    - parklatz_has_fahrzeug: columns=3, fks=2, indices=3
      - Spalten: parklatz_prakplatzNr, fahrzeug_idfahrzeug, datum
      - FKs: fk_parklatz_has_fahrzeug_parklatz, fk_parklatz_has_fahrzeug_fahrzeug1
      - Indizes: PRIMARY, fk_parklatz_has_fahrzeug_fahrzeug1_idx, fk_parklatz_has_fahrzeug_parklatz_idx
    - kategorie: columns=2, fks=0, indices=1
      - Spalten: idkategorie, bezeichnung
      - Indizes: PRIMARY
