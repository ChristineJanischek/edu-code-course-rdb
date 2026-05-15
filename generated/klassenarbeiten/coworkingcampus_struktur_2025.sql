-- SQL-Struktur Teil C (Version 2)
-- Kompakter SQL-Kontext mit 6 Entitaetstypen

DROP DATABASE IF EXISTS coworkingcampusdb_2025;
CREATE DATABASE coworkingcampusdb_2025 CHARACTER SET utf8 COLLATE utf8_general_ci;
USE coworkingcampusdb_2025;

DROP TABLE IF EXISTS zahlungen;
DROP TABLE IF EXISTS supporttickets;
DROP TABLE IF EXISTS buchungen;
DROP TABLE IF EXISTS arbeitsplaetze;
DROP TABLE IF EXISTS standorte;
DROP TABLE IF EXISTS kunden;

CREATE TABLE kunden (
  kunde_id INT PRIMARY KEY,
  vorname VARCHAR(50) NOT NULL,
  nachname VARCHAR(50) NOT NULL,
  studiengang VARCHAR(80) NOT NULL,
  registriert_am DATE NOT NULL,
  aktiv TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE standorte (
  standort_id INT PRIMARY KEY,
  bezeichnung VARCHAR(100) NOT NULL,
  gebaeude VARCHAR(80) NOT NULL,
  etage INT NOT NULL,
  aktiv TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE arbeitsplaetze (
  platz_id INT PRIMARY KEY,
  standort_id INT NOT NULL,
  tarifname VARCHAR(80) NOT NULL,
  stundenpreis DECIMAL(6,2) NOT NULL,
  max_personen INT NOT NULL,
  platzcode VARCHAR(30) NOT NULL UNIQUE,
  status ENUM('frei','belegt','gesperrt') NOT NULL DEFAULT 'frei',
  CONSTRAINT fk_platz_standort FOREIGN KEY (standort_id) REFERENCES standorte(standort_id)
);

CREATE TABLE buchungen (
  buchung_id INT PRIMARY KEY,
  kunde_id INT NOT NULL,
  platz_id INT NOT NULL,
  startzeit DATETIME NOT NULL,
  endzeit DATETIME,
  status ENUM('laufend','abgeschlossen','storniert') NOT NULL DEFAULT 'laufend',
  CONSTRAINT fk_buchung_kunde FOREIGN KEY (kunde_id) REFERENCES kunden(kunde_id),
  CONSTRAINT fk_buchung_platz FOREIGN KEY (platz_id) REFERENCES arbeitsplaetze(platz_id)
);

CREATE TABLE supporttickets (
  ticket_id INT PRIMARY KEY,
  kunde_id INT NOT NULL,
  buchung_id INT,
  erstellt_am DATETIME NOT NULL,
  prioritaet ENUM('niedrig','mittel','hoch') NOT NULL,
  status ENUM('offen','in_bearbeitung','geloest') NOT NULL DEFAULT 'offen',
  CONSTRAINT fk_ticket_kunde FOREIGN KEY (kunde_id) REFERENCES kunden(kunde_id),
  CONSTRAINT fk_ticket_buchung FOREIGN KEY (buchung_id) REFERENCES buchungen(buchung_id)
);

CREATE TABLE zahlungen (
  zahlung_id INT PRIMARY KEY,
  buchung_id INT NOT NULL,
  betrag DECIMAL(7,2) NOT NULL,
  zahlart ENUM('Karte','Lastschrift','App') NOT NULL,
  bezahlt_am DATETIME NOT NULL,
  zahlstatus ENUM('offen','bezahlt','storniert') NOT NULL DEFAULT 'bezahlt',
  CONSTRAINT fk_zahlung_buchung FOREIGN KEY (buchung_id) REFERENCES buchungen(buchung_id)
);
