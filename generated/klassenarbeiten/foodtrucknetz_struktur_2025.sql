-- SQL-Struktur Teil C (Version 3)
-- Kompakter SQL-Kontext mit 6 Entitaetstypen

DROP DATABASE IF EXISTS foodtrucknetzdb_2025;
CREATE DATABASE foodtrucknetzdb_2025 CHARACTER SET utf8 COLLATE utf8_general_ci;
USE foodtrucknetzdb_2025;

DROP TABLE IF EXISTS zahlungen;
DROP TABLE IF EXISTS bestellungen;
DROP TABLE IF EXISTS produkte;
DROP TABLE IF EXISTS trucks;
DROP TABLE IF EXISTS standorte;
DROP TABLE IF EXISTS kunden;

CREATE TABLE kunden (
  kunde_id INT PRIMARY KEY,
  vorname VARCHAR(50) NOT NULL,
  nachname VARCHAR(50) NOT NULL,
  bonuslevel ENUM('Bronze','Silber','Gold') NOT NULL,
  registriert_am DATE NOT NULL,
  aktiv TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE standorte (
  standort_id INT PRIMARY KEY,
  standortname VARCHAR(100) NOT NULL,
  stadtteil VARCHAR(80) NOT NULL,
  aktiv TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE trucks (
  truck_id INT PRIMARY KEY,
  standort_id INT NOT NULL,
  truckname VARCHAR(100) NOT NULL,
  status ENUM('offen','pause','wartung') NOT NULL DEFAULT 'offen',
  CONSTRAINT fk_truck_standort FOREIGN KEY (standort_id) REFERENCES standorte(standort_id)
);

CREATE TABLE produkte (
  produkt_id INT PRIMARY KEY,
  truck_id INT NOT NULL,
  produktname VARCHAR(100) NOT NULL,
  kategorie VARCHAR(80) NOT NULL,
  preis DECIMAL(6,2) NOT NULL,
  verfuegbar TINYINT(1) NOT NULL DEFAULT 1,
  CONSTRAINT fk_produkt_truck FOREIGN KEY (truck_id) REFERENCES trucks(truck_id)
);

CREATE TABLE bestellungen (
  bestellung_id INT PRIMARY KEY,
  kunde_id INT NOT NULL,
  truck_id INT NOT NULL,
  produkt_id INT NOT NULL,
  bestellt_am DATETIME NOT NULL,
  status ENUM('neu','abgeschlossen','storniert') NOT NULL DEFAULT 'neu',
  CONSTRAINT fk_bestellung_kunde FOREIGN KEY (kunde_id) REFERENCES kunden(kunde_id),
  CONSTRAINT fk_bestellung_truck FOREIGN KEY (truck_id) REFERENCES trucks(truck_id),
  CONSTRAINT fk_bestellung_produkt FOREIGN KEY (produkt_id) REFERENCES produkte(produkt_id)
);

CREATE TABLE zahlungen (
  zahlung_id INT PRIMARY KEY,
  bestellung_id INT NOT NULL,
  betrag DECIMAL(7,2) NOT NULL,
  zahlart ENUM('Karte','App','Bar') NOT NULL,
  bezahlt_am DATETIME NOT NULL,
  status ENUM('offen','bezahlt','erstattet') NOT NULL DEFAULT 'bezahlt',
  CONSTRAINT fk_zahlung_bestellung FOREIGN KEY (bestellung_id) REFERENCES bestellungen(bestellung_id)
);
