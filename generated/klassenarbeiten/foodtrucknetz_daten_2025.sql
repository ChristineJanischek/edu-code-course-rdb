-- SQL-Daten Teil C (Version 3, kompakt mit 6 Entitaetstypen)
USE foodtrucknetzdb_2025;

INSERT INTO kunden VALUES
(1,'Mara','Klein','Gold','2024-01-08',1),
(2,'Nico','Brandt','Silber','2024-01-15',1),
(3,'Omar','Saad','Bronze','2024-02-03',1),
(4,'Pia','Lorenz','Silber','2024-02-21',1),
(5,'Quin','Roth','Gold','2024-03-10',1),
(6,'Rina','Pham','Bronze','2024-03-28',1);

INSERT INTO standorte VALUES
(10,'Innenstadt','Mitte',1),
(11,'Campuspark','Nord',1),
(12,'Seepromenade','West',1);

INSERT INTO trucks VALUES
(100,10,'Urban Bites','offen'),
(101,11,'Campus Curry','offen'),
(102,12,'Lake Tacos','wartung');

INSERT INTO produkte VALUES
(200,100,'Falafel Wrap','Wrap',7.50,1),
(201,100,'Pommes Box','Snack',4.00,1),
(202,101,'Veggie Bowl','Bowl',8.20,1),
(203,101,'Linsensuppe','Suppe',5.60,1),
(204,102,'Fish Taco','Taco',6.80,0),
(205,102,'Mais Taco','Taco',6.20,1);

INSERT INTO bestellungen VALUES
(3000,1,100,200,'2025-03-10 12:10:00','abgeschlossen'),
(3001,2,100,201,'2025-03-10 12:18:00','abgeschlossen'),
(3002,1,101,202,'2025-03-11 13:05:00','abgeschlossen'),
(3003,3,101,203,'2025-03-11 13:20:00','neu'),
(3004,4,100,200,'2025-03-12 11:55:00','abgeschlossen'),
(3005,5,101,202,'2025-03-12 12:40:00','abgeschlossen');

INSERT INTO zahlungen VALUES
(4000,3000,7.50,'Karte','2025-03-10 12:11:00','bezahlt'),
(4001,3001,4.00,'App','2025-03-10 12:19:00','bezahlt'),
(4002,3002,8.20,'Bar','2025-03-11 13:06:00','bezahlt'),
(4003,3004,7.50,'Karte','2025-03-12 11:56:00','bezahlt'),
(4004,3005,8.20,'App','2025-03-12 12:41:00','bezahlt');
