-- SQL-Struktur fuer Modellierungskontext: Lernlabor
-- Struktur-only Dump als Workbench-Ersatz fuer Referenzgrafik-Generierung

DROP DATABASE IF EXISTS lernlabordb_2025;
CREATE DATABASE lernlabordb_2025 CHARACTER SET utf8 COLLATE utf8_general_ci;
USE lernlabordb_2025;

DROP TABLE IF EXISTS coach_einsaetze;
DROP TABLE IF EXISTS slots;
DROP TABLE IF EXISTS lernende;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS workshops;
DROP TABLE IF EXISTS geraete;
DROP TABLE IF EXISTS coachs;

CREATE TABLE lernende (
  lernende_id INT PRIMARY KEY,
  vorname VARCHAR(80) NOT NULL,
  nachname VARCHAR(80) NOT NULL,
  teamname VARCHAR(80) NOT NULL
);

CREATE TABLE teams (
  team_id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  status VARCHAR(40) NOT NULL
);

CREATE TABLE geraete (
  geraet_id INT PRIMARY KEY,
  bezeichnung VARCHAR(120) NOT NULL,
  raum VARCHAR(80) NOT NULL,
  status VARCHAR(40) NOT NULL
);

CREATE TABLE workshops (
  workshop_id INT PRIMARY KEY,
  titel VARCHAR(120) NOT NULL,
  thema VARCHAR(120) NOT NULL,
  max_teamgroesse INT NOT NULL
);

CREATE TABLE slots (
  slot_id INT PRIMARY KEY,
  workshop_id INT NOT NULL,
  geraet_id INT NOT NULL,
  startzeit DATETIME NOT NULL,
  endzeit DATETIME NOT NULL,
  CONSTRAINT fk_slots_workshops FOREIGN KEY (workshop_id) REFERENCES workshops(workshop_id),
  CONSTRAINT fk_slots_geraete FOREIGN KEY (geraet_id) REFERENCES geraete(geraet_id)
);

CREATE TABLE coachs (
  coach_id INT PRIMARY KEY,
  vorname VARCHAR(80) NOT NULL,
  nachname VARCHAR(80) NOT NULL,
  fachgebiet VARCHAR(120) NOT NULL
);

CREATE TABLE coach_einsaetze (
  coach_einsatz_id INT PRIMARY KEY,
  coach_id INT NOT NULL,
  team_id INT NOT NULL,
  slot_id INT NOT NULL,
  CONSTRAINT fk_coach_einsaetze_coachs FOREIGN KEY (coach_id) REFERENCES coachs(coach_id),
  CONSTRAINT fk_coach_einsaetze_teams FOREIGN KEY (team_id) REFERENCES teams(team_id),
  CONSTRAINT fk_coach_einsaetze_slots FOREIGN KEY (slot_id) REFERENCES slots(slot_id)
);
