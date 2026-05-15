-- SQL-Struktur fuer Modellierungskontext: Kursplattform
-- Struktur-only Dump als Workbench-Ersatz fuer Referenzgrafik-Generierung

DROP DATABASE IF EXISTS kursplattformdb_2025;
CREATE DATABASE kursplattformdb_2025 CHARACTER SET utf8 COLLATE utf8_general_ci;
USE kursplattformdb_2025;

DROP TABLE IF EXISTS kurs_dozent;
DROP TABLE IF EXISTS anmeldungen;
DROP TABLE IF EXISTS termine;
DROP TABLE IF EXISTS dozenten;
DROP TABLE IF EXISTS kurse;
DROP TABLE IF EXISTS mitglieder;

CREATE TABLE mitglieder (
  mitglied_id INT PRIMARY KEY,
  vorname VARCHAR(80) NOT NULL,
  nachname VARCHAR(80) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  aktiv TINYINT NOT NULL DEFAULT 1
);

CREATE TABLE dozenten (
  dozent_id INT PRIMARY KEY,
  vorname VARCHAR(80) NOT NULL,
  nachname VARCHAR(80) NOT NULL,
  fachgebiet VARCHAR(120) NOT NULL,
  aktiv TINYINT NOT NULL DEFAULT 1
);

CREATE TABLE kurse (
  kurs_id INT PRIMARY KEY,
  titel VARCHAR(120) NOT NULL,
  beschreibung VARCHAR(255) NOT NULL,
  kategorie VARCHAR(80) NOT NULL,
  max_teilnehmer INT NOT NULL
);

CREATE TABLE termine (
  termin_id INT PRIMARY KEY,
  kurs_id INT NOT NULL,
  startzeit DATETIME NOT NULL,
  endzeit DATETIME NOT NULL,
  raum VARCHAR(80) NOT NULL,
  status VARCHAR(40) NOT NULL,
  CONSTRAINT fk_termine_kurse FOREIGN KEY (kurs_id) REFERENCES kurse(kurs_id)
);

CREATE TABLE anmeldungen (
  anmeldung_id INT PRIMARY KEY,
  mitglied_id INT NOT NULL,
  termin_id INT NOT NULL,
  angemeldet_am DATETIME NOT NULL,
  status VARCHAR(40) NOT NULL,
  CONSTRAINT fk_anmeldungen_mitglieder FOREIGN KEY (mitglied_id) REFERENCES mitglieder(mitglied_id),
  CONSTRAINT fk_anmeldungen_termine FOREIGN KEY (termin_id) REFERENCES termine(termin_id)
);

CREATE TABLE kurs_dozent (
  kurs_id INT NOT NULL,
  dozent_id INT NOT NULL,
  rolle VARCHAR(40) NOT NULL,
  PRIMARY KEY (kurs_id, dozent_id),
  CONSTRAINT fk_kurs_dozent_kurs FOREIGN KEY (kurs_id) REFERENCES kurse(kurs_id),
  CONSTRAINT fk_kurs_dozent_dozent FOREIGN KEY (dozent_id) REFERENCES dozenten(dozent_id)
);
