-- KA02 BG12 2025 - 60 Minuten - SQL-Teil (separater 3NF-Kontext)
-- Kontext Teil C: Stadtfahrradverleih (nicht identisch mit Teil-B-Modellierung)
-- STRUKTUR-DEFINITION (kompakt, 6 Entitaetstypen)

DROP DATABASE IF EXISTS stadtfahrradverleihdb_2025;
CREATE DATABASE stadtfahrradverleihdb_2025 CHARACTER SET utf8 COLLATE utf8_general_ci;
USE stadtfahrradverleihdb_2025;

DROP TABLE IF EXISTS zahlungen;
DROP TABLE IF EXISTS wartungen;
DROP TABLE IF EXISTS ausleihen;
DROP TABLE IF EXISTS fahrraeder;
DROP TABLE IF EXISTS stationen;
DROP TABLE IF EXISTS kunden;

CREATE TABLE kunden (
  kunde_id INT PRIMARY KEY,
  vorname VARCHAR(50) NOT NULL,
  nachname VARCHAR(50) NOT NULL,
  wohnort VARCHAR(80) NOT NULL,
  registriert_am DATE NOT NULL,
  aktiv TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE stationen (
  station_id INT PRIMARY KEY,
  stationsname VARCHAR(120) NOT NULL,
  stadtteil VARCHAR(80) NOT NULL,
  kapazitaet INT NOT NULL,
  aktiv TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE fahrraeder (
  fahrrad_id INT PRIMARY KEY,
  station_id INT NOT NULL,
  typname VARCHAR(80) NOT NULL,
  stundenpreis DECIMAL(6,2) NOT NULL,
  seriennummer VARCHAR(60) NOT NULL UNIQUE,
  zustand ENUM('verfuegbar','vermietet','wartung') NOT NULL DEFAULT 'verfuegbar',
  CONSTRAINT fk_fahrraeder_station FOREIGN KEY (station_id) REFERENCES stationen(station_id)
);

CREATE TABLE ausleihen (
  ausleihe_id INT PRIMARY KEY,
  kunde_id INT NOT NULL,
  fahrrad_id INT NOT NULL,
  start_station_id INT NOT NULL,
  ziel_station_id INT NOT NULL,
  startzeit DATETIME NOT NULL,
  endzeit DATETIME,
  status ENUM('laufend','abgeschlossen','storniert') NOT NULL DEFAULT 'laufend',
  CONSTRAINT fk_ausleihe_kunde FOREIGN KEY (kunde_id) REFERENCES kunden(kunde_id),
  CONSTRAINT fk_ausleihe_fahrrad FOREIGN KEY (fahrrad_id) REFERENCES fahrraeder(fahrrad_id),
  CONSTRAINT fk_ausleihe_start_station FOREIGN KEY (start_station_id) REFERENCES stationen(station_id),
  CONSTRAINT fk_ausleihe_ziel_station FOREIGN KEY (ziel_station_id) REFERENCES stationen(station_id)
);

CREATE TABLE wartungen (
  wartung_id INT PRIMARY KEY,
  fahrrad_id INT NOT NULL,
  wartungsdatum DATE NOT NULL,
  wartungsart ENUM('Inspektion','Reparatur','Sicherheitscheck') NOT NULL,
  bemerkung VARCHAR(255) NOT NULL,
  CONSTRAINT fk_wartung_fahrrad FOREIGN KEY (fahrrad_id) REFERENCES fahrraeder(fahrrad_id)
);

CREATE TABLE zahlungen (
  zahlung_id INT PRIMARY KEY,
  ausleihe_id INT NOT NULL,
  betrag DECIMAL(7,2) NOT NULL,
  zahlart ENUM('Karte','Lastschrift','App') NOT NULL,
  bezahlt_am DATETIME NOT NULL,
  zahlstatus ENUM('offen','bezahlt','storniert') NOT NULL DEFAULT 'bezahlt',
  CONSTRAINT fk_zahlung_ausleihe FOREIGN KEY (ausleihe_id) REFERENCES ausleihen(ausleihe_id)
);
