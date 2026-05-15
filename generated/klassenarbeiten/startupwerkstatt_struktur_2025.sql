-- SQL-Struktur fuer Modellierungskontext: Startupwerkstatt
-- Struktur-only Dump als Workbench-Ersatz fuer Referenzgrafik-Generierung

DROP DATABASE IF EXISTS startupwerkstattdb_2025;
CREATE DATABASE startupwerkstattdb_2025 CHARACTER SET utf8 COLLATE utf8_general_ci;
USE startupwerkstattdb_2025;

DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS mentor_team;
DROP TABLE IF EXISTS pitches;
DROP TABLE IF EXISTS termine;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS mentoren;

CREATE TABLE teams (
  team_id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  projekt VARCHAR(150) NOT NULL
);

CREATE TABLE mentoren (
  mentor_id INT PRIMARY KEY,
  vorname VARCHAR(80) NOT NULL,
  nachname VARCHAR(80) NOT NULL,
  fachgebiet VARCHAR(120) NOT NULL
);

CREATE TABLE termine (
  termin_id INT PRIMARY KEY,
  datum DATE NOT NULL,
  ort VARCHAR(80) NOT NULL,
  mentor_id INT NOT NULL,
  CONSTRAINT fk_termine_mentoren FOREIGN KEY (mentor_id) REFERENCES mentoren(mentor_id)
);

CREATE TABLE pitches (
  pitch_id INT PRIMARY KEY,
  team_id INT NOT NULL,
  termin_id INT NOT NULL,
  titel VARCHAR(150) NOT NULL,
  status VARCHAR(40) NOT NULL,
  CONSTRAINT fk_pitches_teams FOREIGN KEY (team_id) REFERENCES teams(team_id),
  CONSTRAINT fk_pitches_termine FOREIGN KEY (termin_id) REFERENCES termine(termin_id)
);

CREATE TABLE mentor_team (
  mentor_id INT NOT NULL,
  team_id INT NOT NULL,
  rolle VARCHAR(40) NOT NULL,
  PRIMARY KEY (mentor_id, team_id),
  CONSTRAINT fk_mentor_team_mentoren FOREIGN KEY (mentor_id) REFERENCES mentoren(mentor_id),
  CONSTRAINT fk_mentor_team_teams FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE feedback (
  feedback_id INT PRIMARY KEY,
  pitch_id INT NOT NULL,
  kommentar VARCHAR(255) NOT NULL,
  CONSTRAINT fk_feedback_pitches FOREIGN KEY (pitch_id) REFERENCES pitches(pitch_id)
);
