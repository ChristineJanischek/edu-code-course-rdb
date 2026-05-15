-- KA02 BG12 2025 - SQL-Teil C Daten (kompakt, 6 Entitaetstypen)
USE stadtfahrradverleihdb_2025;

INSERT INTO kunden VALUES
(1,'Lea','Keller','Mitte','2024-01-10',1),
(2,'Noah','Weber','Nord','2024-02-02',1),
(3,'Mia','Schmidt','West','2024-03-18',1),
(4,'Elias','Nguyen','Sued','2024-04-04',1),
(5,'Lina','Bauer','Mitte','2024-04-29',1),
(6,'Paul','Hoffmann','Nord','2024-05-14',1);

INSERT INTO stationen VALUES
(10,'Hauptbahnhof','Mitte',30,1),
(11,'Campus Nord','Nord',22,1),
(12,'Stadtpark','West',18,1),
(13,'Rathaus','Sued',16,1);

INSERT INTO fahrraeder VALUES
(100,10,'City',3.50,'SN-C-100','verfuegbar'),
(101,10,'E-Bike',5.80,'SN-E-101','vermietet'),
(102,11,'Trekking',4.20,'SN-T-102','verfuegbar'),
(103,11,'City',3.50,'SN-C-103','wartung'),
(104,12,'E-Bike',5.80,'SN-E-104','verfuegbar'),
(105,12,'City',3.50,'SN-C-105','verfuegbar'),
(106,13,'Trekking',4.20,'SN-T-106','verfuegbar'),
(107,13,'City',3.50,'SN-C-107','vermietet');

INSERT INTO ausleihen VALUES
(2000,1,100,10,12,'2025-03-10 08:10:00','2025-03-10 09:05:00','abgeschlossen'),
(2001,2,101,10,11,'2025-03-10 09:20:00','2025-03-10 10:00:00','abgeschlossen'),
(2002,3,102,11,10,'2025-03-10 10:10:00',NULL,'laufend'),
(2003,1,104,12,13,'2025-03-11 08:00:00','2025-03-11 09:10:00','abgeschlossen'),
(2004,4,105,12,10,'2025-03-11 11:20:00','2025-03-11 12:15:00','abgeschlossen'),
(2005,5,106,13,12,'2025-03-12 07:40:00','2025-03-12 08:10:00','abgeschlossen'),
(2006,2,107,13,10,'2025-03-12 09:00:00',NULL,'laufend'),
(2007,6,100,10,11,'2025-03-12 12:30:00','2025-03-12 13:05:00','abgeschlossen');

INSERT INTO wartungen VALUES
(3000,103,'2025-03-05','Inspektion','Bremsen und Licht geprueft'),
(3001,104,'2025-03-06','Sicherheitscheck','Rahmen und Reifen kontrolliert'),
(3002,101,'2025-03-07','Reparatur','Akku-Stecker ersetzt');

INSERT INTO zahlungen VALUES
(4000,2000,6.90,'Karte','2025-03-10 09:07:00','bezahlt'),
(4001,2001,5.80,'App','2025-03-10 10:02:00','bezahlt'),
(4002,2003,8.70,'Lastschrift','2025-03-11 09:12:00','bezahlt'),
(4003,2004,6.30,'Karte','2025-03-11 12:20:00','bezahlt'),
(4004,2005,4.20,'App','2025-03-12 08:12:00','bezahlt'),
(4005,2007,4.50,'Karte','2025-03-12 13:10:00','bezahlt');
