-- SQL-Daten Teil C (Version 2, kompakt mit 6 Entitaetstypen)
USE coworkingcampusdb_2025;

INSERT INTO kunden VALUES
(1,'Aylin','Demir','Informatik','2024-01-10',1),
(2,'Ben','Kraft','Wirtschaftsinformatik','2024-01-23',1),
(3,'Clara','Ng','Informatik','2024-02-11',1),
(4,'David','Becker','Maschinenbau','2024-02-19',1),
(5,'Elif','Yilmaz','Elektrotechnik','2024-03-02',1),
(6,'Finn','Schulz','Informatik','2024-03-21',1);

INSERT INTO standorte VALUES
(10,'Campus Hub A','Gebaeude A',1,1),
(11,'Campus Hub B','Gebaeude B',2,1),
(12,'Makerspace C','Gebaeude C',0,1);

INSERT INTO arbeitsplaetze VALUES
(100,10,'Basic',3.20,1,'A-101','frei'),
(101,10,'Team',5.50,4,'A-102','belegt'),
(102,11,'Basic',3.20,1,'B-201','frei'),
(103,11,'Focus',4.10,1,'B-202','gesperrt'),
(104,12,'Team',5.50,4,'C-001','frei'),
(105,12,'Focus',4.10,1,'C-002','belegt');

INSERT INTO buchungen VALUES
(2000,1,100,'2025-03-10 08:00:00','2025-03-10 10:00:00','abgeschlossen'),
(2001,2,101,'2025-03-10 09:00:00','2025-03-10 11:30:00','abgeschlossen'),
(2002,1,102,'2025-03-11 10:00:00','2025-03-11 12:00:00','abgeschlossen'),
(2003,3,105,'2025-03-11 13:00:00',NULL,'laufend'),
(2004,4,104,'2025-03-12 08:30:00','2025-03-12 10:30:00','abgeschlossen'),
(2005,5,101,'2025-03-12 11:00:00','2025-03-12 12:00:00','abgeschlossen'),
(2006,6,100,'2025-03-12 12:30:00',NULL,'laufend');

INSERT INTO supporttickets VALUES
(3000,2,2001,'2025-03-10 09:40:00','mittel','geloest'),
(3001,3,2003,'2025-03-11 13:25:00','hoch','in_bearbeitung'),
(3002,4,2004,'2025-03-12 09:05:00','niedrig','offen');

INSERT INTO zahlungen VALUES
(4000,2000,6.40,'Karte','2025-03-10 10:01:00','bezahlt'),
(4001,2001,13.75,'App','2025-03-10 11:31:00','bezahlt'),
(4002,2002,6.40,'Lastschrift','2025-03-11 12:01:00','bezahlt'),
(4003,2004,11.00,'Karte','2025-03-12 10:31:00','bezahlt'),
(4004,2005,5.50,'App','2025-03-12 12:01:00','bezahlt');
