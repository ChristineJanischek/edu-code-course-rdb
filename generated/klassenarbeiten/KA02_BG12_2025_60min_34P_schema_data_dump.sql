-- KA02 BG12 2025 - 60 Minuten - Struktur- und Datendump
-- Gesamtziel: Mehrtabellenabfragen mit ausreichender Datenmenge
-- Parent-Tabellen: mitglieder (20), dozenten (20)

DROP DATABASE IF EXISTS ka02_bg12_2025_60min;
CREATE DATABASE ka02_bg12_2025_60min CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE ka02_bg12_2025_60min;

DROP TABLE IF EXISTS anmeldungen;
DROP TABLE IF EXISTS termine;
DROP TABLE IF EXISTS kurs_dozent;
DROP TABLE IF EXISTS kurse;
DROP TABLE IF EXISTS dozenten;
DROP TABLE IF EXISTS mitglieder;

CREATE TABLE mitglieder (
  mitglied_id INT PRIMARY KEY,
  vorname VARCHAR(50) NOT NULL,
  nachname VARCHAR(50) NOT NULL,
  stadt VARCHAR(80) NOT NULL,
  geburtsdatum DATE NOT NULL,
  aktiv TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE dozenten (
  dozent_id INT PRIMARY KEY,
  vorname VARCHAR(50) NOT NULL,
  nachname VARCHAR(50) NOT NULL,
  fachgebiet VARCHAR(80) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE kurse (
  kurs_id INT PRIMARY KEY,
  titel VARCHAR(120) NOT NULL,
  niveau ENUM('Einstieg','Mittel','Fortgeschritten') NOT NULL,
  max_teilnehmer INT NOT NULL,
  status ENUM('geplant','aktiv','abgeschlossen') NOT NULL DEFAULT 'aktiv'
);

CREATE TABLE kurs_dozent (
  kurs_id INT NOT NULL,
  dozent_id INT NOT NULL,
  rolle ENUM('Hauptdozent','Co-Dozent') NOT NULL,
  PRIMARY KEY (kurs_id, dozent_id),
  CONSTRAINT fk_kd_kurs FOREIGN KEY (kurs_id) REFERENCES kurse(kurs_id),
  CONSTRAINT fk_kd_dozent FOREIGN KEY (dozent_id) REFERENCES dozenten(dozent_id)
);

CREATE TABLE termine (
  termin_id INT PRIMARY KEY,
  kurs_id INT NOT NULL,
  start_datum DATE NOT NULL,
  start_uhrzeit TIME NOT NULL,
  ende_uhrzeit TIME NOT NULL,
  raum VARCHAR(30) NOT NULL,
  CONSTRAINT fk_termine_kurs FOREIGN KEY (kurs_id) REFERENCES kurse(kurs_id)
);

CREATE TABLE anmeldungen (
  anmeldung_id INT PRIMARY KEY,
  mitglied_id INT NOT NULL,
  kurs_id INT NOT NULL,
  anmeldedatum DATE NOT NULL,
  status ENUM('angemeldet','warteliste','storniert') NOT NULL DEFAULT 'angemeldet',
  CONSTRAINT fk_anm_mitglied FOREIGN KEY (mitglied_id) REFERENCES mitglieder(mitglied_id),
  CONSTRAINT fk_anm_kurs FOREIGN KEY (kurs_id) REFERENCES kurse(kurs_id)
);

-- Parenttable mitglieder: 20 Datensaetze
INSERT INTO mitglieder VALUES
(1,'Lena','Mayer','Stuttgart','2007-03-12',1),
(2,'Noah','Klein','Esslingen','2006-11-05',1),
(3,'Mia','Schuster','Ludwigsburg','2007-07-21',1),
(4,'Elias','Bauer','Waiblingen','2006-02-18',1),
(5,'Lea','Wolf','Stuttgart','2007-09-09',1),
(6,'Finn','Schmidt','Fellbach','2006-12-01',1),
(7,'Emma','Wagner','Esslingen','2007-04-17',1),
(8,'Paul','Haas','Backnang','2006-10-10',1),
(9,'Lina','Keller','Waiblingen','2007-01-30',1),
(10,'Jonas','Beck','Stuttgart','2006-08-14',1),
(11,'Nina','Richter','Esslingen','2007-05-02',1),
(12,'Tim','Neumann','Ludwigsburg','2006-03-27',1),
(13,'Sara','Huber','Stuttgart','2007-06-19',1),
(14,'Ben','Graf','Waiblingen','2006-09-12',1),
(15,'Anna','Lorenz','Fellbach','2007-02-23',1),
(16,'Luca','Seidel','Stuttgart','2006-01-16',1),
(17,'Clara','Pfeifer','Esslingen','2007-08-07',1),
(18,'Max','Brandt','Ludwigsburg','2006-05-29',1),
(19,'Julia','Voss','Backnang','2007-10-03',1),
(20,'David','Krueger','Stuttgart','2006-06-25',1);

-- Parenttable dozenten: 20 Datensaetze
INSERT INTO dozenten VALUES
(1,'Martin','Kurz','SQL','martin.kurz@schule.de'),
(2,'Petra','Lang','Datenmodellierung','petra.lang@schule.de'),
(3,'Uwe','Stein','Python','uwe.stein@schule.de'),
(4,'Heike','Graf','Normalisierung','heike.graf@schule.de'),
(5,'Thomas','Berg','DB-Administration','thomas.berg@schule.de'),
(6,'Mona','Brand','SQL','mona.brand@schule.de'),
(7,'Nils','Wolf','EERM','nils.wolf@schule.de'),
(8,'Karin','Otto','Datenanalyse','karin.otto@schule.de'),
(9,'Jana','Winkler','Programmierung','jana.winkler@schule.de'),
(10,'Dirk','Herz','Workbench','dirk.herz@schule.de'),
(11,'Sven','Schulz','SQL','sven.schulz@schule.de'),
(12,'Nora','Simon','EERM','nora.simon@schule.de'),
(13,'Ralf','Koch','Datenbanken','ralf.koch@schule.de'),
(14,'Iris','Ackermann','Didaktik','iris.ackermann@schule.de'),
(15,'Timo','Arndt','BI','timo.arndt@schule.de'),
(16,'Eva','Lenz','SQL','eva.lenz@schule.de'),
(17,'Sascha','Jung','Normalisierung','sascha.jung@schule.de'),
(18,'Maren','Kuhn','EERM','maren.kuhn@schule.de'),
(19,'Olaf','Reuter','Programmierung','olaf.reuter@schule.de'),
(20,'Rita','Moser','Datenqualitaet','rita.moser@schule.de');

INSERT INTO kurse VALUES
(101,'SQL Grundlagen','Einstieg',20,'aktiv'),
(102,'JOIN und Aggregation','Mittel',20,'aktiv'),
(103,'EERM mit Workbench','Mittel',18,'aktiv'),
(104,'Normalisierung bis 3NF','Mittel',18,'aktiv'),
(105,'Performance mit Indizes','Fortgeschritten',16,'geplant'),
(106,'SQL Reporting','Fortgeschritten',16,'aktiv'),
(107,'Datenqualitaet in Projekten','Mittel',18,'aktiv'),
(108,'Programmierung und Struktogramm','Einstieg',22,'aktiv');

INSERT INTO kurs_dozent VALUES
(101,1,'Hauptdozent'),(101,6,'Co-Dozent'),
(102,11,'Hauptdozent'),(102,2,'Co-Dozent'),
(103,7,'Hauptdozent'),(103,10,'Co-Dozent'),
(104,4,'Hauptdozent'),(104,17,'Co-Dozent'),
(105,5,'Hauptdozent'),(105,13,'Co-Dozent'),
(106,16,'Hauptdozent'),(106,8,'Co-Dozent'),
(107,20,'Hauptdozent'),(107,14,'Co-Dozent'),
(108,9,'Hauptdozent'),(108,3,'Co-Dozent');

INSERT INTO termine VALUES
(1001,101,'2026-05-20','08:00:00','09:30:00','R101'),
(1002,101,'2026-05-27','08:00:00','09:30:00','R101'),
(1003,102,'2026-05-21','10:00:00','11:30:00','R103'),
(1004,102,'2026-05-28','10:00:00','11:30:00','R103'),
(1005,103,'2026-05-22','08:00:00','09:30:00','R201'),
(1006,103,'2026-05-29','08:00:00','09:30:00','R201'),
(1007,104,'2026-05-23','10:00:00','11:30:00','R202'),
(1008,104,'2026-05-30','10:00:00','11:30:00','R202'),
(1009,105,'2026-06-03','12:00:00','13:30:00','R301'),
(1010,106,'2026-06-04','08:00:00','09:30:00','R302'),
(1011,107,'2026-06-05','10:00:00','11:30:00','R303'),
(1012,108,'2026-06-06','12:00:00','13:30:00','R304');

INSERT INTO anmeldungen VALUES
(5001,1,101,'2026-05-01','angemeldet'),
(5002,1,102,'2026-05-01','angemeldet'),
(5003,2,103,'2026-05-02','angemeldet'),
(5004,2,101,'2026-05-02','warteliste'),
(5005,3,104,'2026-05-03','angemeldet'),
(5006,3,102,'2026-05-03','angemeldet'),
(5007,4,101,'2026-05-04','angemeldet'),
(5008,4,108,'2026-05-04','angemeldet'),
(5009,5,103,'2026-05-04','storniert'),
(5010,5,107,'2026-05-05','angemeldet'),
(5011,6,106,'2026-05-05','angemeldet'),
(5012,6,104,'2026-05-05','angemeldet'),
(5013,7,101,'2026-05-06','angemeldet'),
(5014,8,102,'2026-05-06','angemeldet'),
(5015,9,103,'2026-05-06','angemeldet'),
(5016,10,104,'2026-05-07','angemeldet'),
(5017,11,105,'2026-05-07','warteliste'),
(5018,12,106,'2026-05-08','angemeldet'),
(5019,13,107,'2026-05-08','angemeldet'),
(5020,14,108,'2026-05-08','angemeldet'),
(5021,15,101,'2026-05-09','angemeldet'),
(5022,15,102,'2026-05-09','angemeldet'),
(5023,16,103,'2026-05-09','angemeldet'),
(5024,17,104,'2026-05-10','angemeldet'),
(5025,18,105,'2026-05-10','warteliste'),
(5026,19,106,'2026-05-10','angemeldet'),
(5027,20,107,'2026-05-10','angemeldet'),
(5028,20,108,'2026-05-10','angemeldet');

-- Beispielabfragen fuer Lehrkraefte
-- 1) Mitglied, Kurs, Dozent, Termin
-- SELECT m.nachname, m.vorname, k.titel, d.nachname AS dozent, t.start_datum
-- FROM anmeldungen a
-- JOIN mitglieder m ON m.mitglied_id = a.mitglied_id
-- JOIN kurse k ON k.kurs_id = a.kurs_id
-- JOIN kurs_dozent kd ON kd.kurs_id = k.kurs_id
-- JOIN dozenten d ON d.dozent_id = kd.dozent_id
-- JOIN termine t ON t.kurs_id = k.kurs_id
-- WHERE a.status = 'angemeldet'
-- ORDER BY m.nachname, t.start_datum;
