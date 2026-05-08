INSERT INTO vets 1, 'James', 'Carter');
INSERT INTO vets 2, 'Helen', 'Leary');
INSERT INTO vets 3, 'Linda', 'Douglas');
INSERT INTO vets 4, 'Rafael', 'Ortega');
INSERT INTO vets 5, 'Henry', 'Stevens');
INSERT INTO vets 6, 'Sharon', 'Jenkins');

INSERT INTO specialties 1, 'radiology');
INSERT INTO specialties 2, 'surgery');
INSERT INTO specialties 3, 'dentistry');

INSERT INTO vet_specialties 2, 1);
INSERT INTO vet_specialties 3, 2);
INSERT INTO vet_specialties 3, 3);
INSERT INTO vet_specialties 4, 2);
INSERT INTO vet_specialties 5, 1);

INSERT INTO types 1, 'cat');
INSERT INTO types 2, 'dog');
INSERT INTO types 3, 'lizard');
INSERT INTO types 4, 'snake');
INSERT INTO types 5, 'bird');
INSERT INTO types 6, 'hamster');

INSERT INTO owners 1, 'George', 'Franklin', '110 W. Liberty St.', 'Madison', '6085551023');
INSERT INTO owners 2, 'Betty', 'Davis', '638 Cardinal Ave.', 'Sun Prairie', '6085551749');
INSERT INTO owners 3, 'Eduardo', 'Rodriquez', '2693 Commerce St.', 'McFarland', '6085558763');
INSERT INTO owners 4, 'Harold', 'Davis', '563 Friendly St.', 'Windsor', '6085553198');
INSERT INTO owners 5, 'Peter', 'McTavish', '2387 S. Fair Way', 'Madison', '6085552765');
INSERT INTO owners 6, 'Jean', 'Coleman', '105 N. Lake St.', 'Monona', '6085552654');
INSERT INTO owners 7, 'Jeff', 'Black', '1450 Oak Blvd.', 'Monona', '6085555387');
INSERT INTO owners 8, 'Maria', 'Escobito', '345 Maple St.', 'Madison', '6085557683');
INSERT INTO owners 9, 'David', 'Schroeder', '2749 Blackhawk Trail', 'Madison', '6085559435');
INSERT INTO owners 10, 'Carlos', 'Estaban', '2335 Independence La.', 'Waunakee', '6085555487');

INSERT INTO pets VALUES (1, 'Leo', '2010-09-07', 1, 1, NULL, NULL);
INSERT INTO pets VALUES (2, 'Basil', '2012-08-06', 6, 2, NULL, NULL);
INSERT INTO pets VALUES (3, 'Rosy', '2011-04-17', 2, 3, NULL, NULL);
INSERT INTO pets VALUES (4, 'Jewel', '2010-03-07', 2, 3, NULL, NULL);
INSERT INTO pets VALUES (5, 'Iggy', '2010-11-30', 3, 4, NULL, NULL);
INSERT INTO pets VALUES (6, 'George', '2010-01-20', 4, 5, NULL, NULL);
INSERT INTO pets VALUES (7, 'Samantha', '2012-09-04', 1, 6, NULL, NULL);
INSERT INTO pets VALUES (8, 'Max', '2012-09-04', 1, 6, NULL, NULL);
INSERT INTO pets VALUES (9, 'Lucky', '2011-08-06', 5, 7, NULL, NULL);
INSERT INTO pets VALUES (10, 'Mulligan', '2007-02-24', 2, 8, NULL, NULL);
INSERT INTO pets VALUES (11, 'Freddy', '2010-03-09', 5, 9, NULL, NULL);
INSERT INTO pets VALUES (12, 'Lucky', '2010-06-24', 2, 10, NULL, NULL);
INSERT INTO pets VALUES (13, 'Sly', '2012-06-08', 1, 10, NULL, NULL);

INSERT INTO visits 1, 7, '2013-01-01', 'rabies shot');
INSERT INTO visits 2, 8, '2013-01-02', 'rabies shot');
INSERT INTO visits 3, 8, '2013-01-03', 'neutered');
INSERT INTO visits 4, 7, '2013-01-04', 'spayed');
