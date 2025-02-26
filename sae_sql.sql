# DROP DATABASE IF EXISTS sae345;
# CREATE DATABASE sae345;
USE sae345;

DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS boisson;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS arome;
DROP TABLE IF EXISTS type_boisson;
DROP TABLE commande_adresse;

CREATE TABLE type_boisson(
   id_type_boisson INT AUTO_INCREMENT,
   nom_type_boisson VARCHAR(255),
   PRIMARY KEY(id_type_boisson)
);



CREATE TABLE arome(
   id_arome INT AUTO_INCREMENT,
   nom_arome VARCHAR(255),
   PRIMARY KEY(id_arome)
);



CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(255),
   email VARCHAR(255),
   nom VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   est_actif BOOLEAN,
   PRIMARY KEY(id_utilisateur)
);


CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(255),
   PRIMARY KEY(id_etat)
);

CREATE TABLE boisson(
   id_boisson INT AUTO_INCREMENT,
   nom_boisson VARCHAR(255),
   prix_boisson DECIMAL(15,2),
   volume_boisson VARCHAR(255),
   description_boisson VARCHAR(255),
   fournisseur_boisson VARCHAR(255),
   marque_boisson VARCHAR(255),
   photo_boisson VARCHAR(255),
   stock_boisson INT,
   type_boisson_id INT NOT NULL,
   arome_id INT NOT NULL,
   PRIMARY KEY(id_boisson),
   FOREIGN KEY(type_boisson_id) REFERENCES type_boisson(id_type_boisson),
   FOREIGN KEY(arome_id) REFERENCES arome(id_arome)
);



CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat_commande DATE,
   etat_id INT NOT NULL,
   utilisateur_id INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ligne_commande(
   boisson_id INT NOT NULL,
   commande_id INT NOT NULL,
   quantite_ligne_commande INT,
   prix_ligne_commande DECIMAL(15,2),
   PRIMARY KEY(boisson_id, commande_id),
   FOREIGN KEY(boisson_id) REFERENCES boisson(id_boisson),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande)
);

CREATE TABLE ligne_panier(
   boisson_id INT NOT NULL,
   utilisateur_id INT NOT NULL,
   quantite_ligne_panier INT,
   date_ajout_ligne_panier VARCHAR(255),
   PRIMARY KEY(boisson_id, utilisateur_id),
   FOREIGN KEY(boisson_id) REFERENCES boisson(id_boisson),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);


CREATE TABLE commande_adresse (
   id_commande_adresse INT AUTO_INCREMENT PRIMARY KEY,
   commande_id INT,
   nom_livraison VARCHAR(255),
   rue_livraison VARCHAR(255),
   code_postal_livraison VARCHAR(20),
   ville_livraison VARCHAR(255),
   nom_facturation VARCHAR(255),
   rue_facturation VARCHAR(255),
   code_postal_facturation VARCHAR(20),
   ville_facturation VARCHAR(255),
   FOREIGN KEY (commande_id) REFERENCES commande(id_commande)
);

INSERT INTO type_boisson(id_type_boisson,nom_type_boisson) VALUES
(NULL,'Soda'),
(NULL,'Jus de fruit'),
(NULL,'Alcool'),
(NULL,'Hydratant'); -- eau


INSERT INTO arome(id_arome,nom_arome) VALUES

(NULL,'Sans arôme'),
(NULL,'Cola'),

-- Fruits
(NULL,'Cerise'),
(NULL,'Orange'),
(NULL,'Citron'),
(NULL,'Framboise'),
(NULL,'Fraise'),
(NULL,'Pêche'),
(NULL,'Pomme'),
(NULL,'Raison'),
(NULL,'Mangue'),
(NULL,'Tropical'),
(NULL,'Multifruits'),
(NULL,'Cassis'),
(NULL,'Ananas'),
(NULL,'Autre');

INSERT INTO etat(id_etat,libelle_etat) VALUES
(NULL,'En préparation'),
(NULL,'Envoyé'),
(NULL,'Livré');




INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'scrypt:32768:8:1$irSP6dJEjy1yXof2$56295be51bb989f467598b63ba6022405139656d6609df8a71768d42738995a21605c9acbac42058790d30fd3adaaec56df272d24bed8385e66229c81e71a4f4',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'scrypt:32768:8:1$iFP1d8bdBmhW6Sgc$7950bf6d2336d6c9387fb610ddaec958469d42003fdff6f8cf5a39cf37301195d2e5cad195e6f588b3644d2a9116fa1636eb400b0cb5537603035d9016c15910',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'scrypt:32768:8:1$l3UTNxiLZGuBKGkg$ae3af0d19f0d16d4a495aa633a1cd31ac5ae18f98a06ace037c0f4fb228ed86a2b6abc64262316d0dac936eb72a67ae82cd4d4e4847ee0fb0b19686ee31194b3',
    'ROLE_client','client2','1');

INSERT INTO boisson (id_boisson,nom_boisson, prix_boisson, volume_boisson, description_boisson, fournisseur_boisson, marque_boisson, photo_boisson, stock_boisson, type_boisson_id, arome_id) VALUES

-- SODA
(NULL,'Coca-Cola', 1.50, '330ml', 'Boisson gazeuse sucrée au goût de Cola', 'Coca-Cola Company', 'Coca-Cola', 'coca_cola.png',12, 1, 2),
(NULL,'Coca-Cola Cherry',1.60,'330ml','Boisson gazeuse sucrée au goût de cerise', 'Coca-Cola Company', 'Coca-Cola', 'coca_cola_cherry.png',10, 1, 3),
(NULL,'Coca-Cola Pêche',1.70,'330ml','Boisson gazeuse sucrée au goût de pêche', 'Coca-Cola Company', 'Coca-Cola', 'coca_cola_peche.jpg',7, 1, 8),
(NULL,'Coca-Cola Citron',1.55,'330ml','Boisson gazeuse sucrée au goût de citron', 'Coca-Cola Company', 'Coca-Cola', 'coca_cola_citron.png',9, 1, 5),

(NULL,'Fanta Orange', 1.50, '330ml', 'Boisson gazeuse sucrée au goût d\'orange', 'Coca-Cola Company', 'Fanta', 'fanta_orange.png',14, 1, 4),
(NULL,'Fanta Citron', 1.55, '330ml', 'Boisson gazeuse sucrée au goût de citron', 'Coca-Cola Company', 'Fanta', 'fanta_citron.png', 12,1, 5),
(NULL,'Fanta Fraise', 1.60, '330ml', 'Boisson gazeuse sucrée au goût de fraise', 'Coca-Cola Company', 'Fanta', 'fanta_fraise.jpg', 8,1, 7),
(NULL,'Fanta Raisin', 1.45, '330ml', 'Boisson gazeuse sucrée au goût de raisin', 'Coca-Cola Company', 'Fanta', 'fanta_raisin.png', 6,1, 10),
(NULL,'Fanta Cassis', 1.60, '330ml', 'Boisson gazeuse sucrée au goût de cassis', 'Coca-Cola Company', 'Fanta', 'fanta_cassis.jpg', 5,1, 14),
(NULL,'Fanta Framboise', 1.50, '330ml', 'Boisson gazeuse sucrée au goût de framboise', 'Coca-Cola Company', 'Fanta', 'fanta_framboise.png', 3,1, 6),
(NULL,'Fanta Pomme', 1.50, '330ml', 'Boisson gazeuse sucrée au goût de pomme', 'Coca-Cola Company', 'Fanta', 'fanta_pomme.png', 7,1, 9),

(NULL,'Lipton Pêche', 1.50, '330ml', 'Boisson sucrée au goût de pêche', 'Unilever', 'Lipton', 'lipton.jpg', 10,1, 8),
(NULL,'Lipton Citron', 1.60, '330ml', 'Boisson sucrée au goût de citron', 'Unilever', 'Lipton', 'lipton_citron.jpg', 18,1, 5),
(NULL,'Lipton Framboise', 1.70, '330ml', 'Boisson sucrée au goût de framboise', 'Unilever', 'Lipton', 'lipton_framboise.jpg',10, 1, 6),
(NULL,'Lipton Tropical', 1.40, '500ml', 'Boisson sucrée au goût tropical', 'Unilever', 'Lipton', 'lipton_tropical.jpg', 6,1, 12),
(NULL,'Lipton Mangue', 1.50, '330ml', 'Boisson sucrée au goût de mangue', 'Unilever', 'Lipton', 'lipton_mangue.jpeg', 8,1, 11),

(NULL,'Oasis Tropical', 1.50, '330ml', 'Boisson sucrée au goût tropical', 'Orangina Suntory France', 'Oasis', 'oasis.jpg',16, 1, 12),

(NULL,'Orangina', 1.50, '330ml', 'Boisson sucrée au goût tropical', 'Orangina Suntory France', 'Orangina', 'orangina.png', 14,1, 4),

-- JUS DE FRUIT
(NULL,'Jus d\'orange', 2.00, '1L', 'Jus d\'orange 100% naturel', 'Tropicana', 'Tropicana', 'jus_orange.png', 8,2, 4),
(NULL,'Jus de pomme', 2.00, '1L', 'Jus de pomme 100% naturel', 'Tropicana', 'Tropicana', 'jus_pomme.png', 5,2, 9),
(NULL,'Jus de raisin', 2.40, '1L', 'Jus de raisin 100% naturel', 'Tropicana', 'Tropicana', 'jus_raisin.png', 8,2, 10),
(NULL,'Jus d\'ananas', 2.30, '1L', 'Jus d\'ananas 100% naturel', 'Tropicana', 'Tropicana', 'jus_ananas.png', 4,2, 15),
(NULL,'Jus multifruit', 1.80, '1L', 'Jus multifruit 100% naturel', 'Tropicana', 'Tropicana', 'jus_multifruit.png', 14,2, 13),

-- ALCOOL
(NULL, 'Whisky', 49.90, '750ml', 'Whisky écossais de grande qualité', 'Diageo', 'Johnnie Walker', 'whisky.png', 14,3, 16),
(NULL, 'Vodka', 25.50, '700ml', 'Vodka pure et cristalline', 'Pernod Ricard', 'Absolut', 'vodka.jpg', 10,3, 1),
(NULL, 'Rhum', 32.00, '750ml', 'Rhum brun aux arômes épicés', 'Bacardi Limited', 'Bacardi', 'rhum.jpg', 8,3,16),
(NULL, 'Ricard', 18.90, '700ml', 'Pastis de Marseille emblématique', 'Pernod Ricard', 'Ricard', 'ricard.jpg', 5,3, 16),
(NULL, 'Bière', 2.50, '330ml', 'Bière blonde rafraîchissante', 'Heineken', 'Heineken', 'biere.jpg', 24,3, 16),
(NULL, 'Cidre', 4.90, '750ml', 'Cidre brut aux saveurs fruitées', 'Les Celliers Associés', 'Loïc Raison', 'cidre.jpg',13, 3, 16),

-- EAU (Badoit, Carrola,)
(NULL,'Eau minérale', 0.80, '500ml', 'Eau minérale naturelle', 'Evian', 'Evian', 'eau_minerale.jpg', 20,4, 1),
(NULL,'Eau de source', 0.90, '500ml', 'Eau naturelle de source', 'Evian', 'Evian', 'eau_de_source.jpg', 18,4, 1),
(NULL,'Eau alcaline', 1.80, '500ml', 'Eau avec un pH élevé', 'Essentia', 'Essentia', 'eau_alcaline.jpg', 21,4, 1),

(NULL,'Eau pétillante', 2.20, '1500ml', 'Eau gazeuse naturelle', 'Perrier', 'Perrier', 'eau_petillante.png', 21,4, 1),
(NULL,'Eau minérale gazeuse', 1.30, '500ml', 'Eau minérale avec bulles', 'San Pellegrino', 'San Pellegrino', 'eau_minerale_gazeuse.jpg',17, 4, 1),

(NULL,'Eau aromatisée à la fraise', 1.50, '500ml', 'Eau avec arôme naturel de fraise', 'Hint', 'Hint', 'eau_aromatisee_fraise.jpg', 16,4, 7);


INSERT INTO commande (id_commande, date_achat_commande, etat_id, utilisateur_id) VALUES
(NULL, '2025-01-15', 1, 1),
(NULL, '2025-01-16', 2, 2),
(NULL, '2025-01-17', 3, 3);

INSERT INTO ligne_commande (boisson_id, commande_id, quantite_ligne_commande, prix_ligne_commande) VALUES
(1, 1, 2, 3.00),
(2, 1, 1, 1.60),
(3, 2, 3, 5.10),
(5, 3, 6, 9.00);

INSERT INTO ligne_panier (boisson_id, utilisateur_id, quantite_ligne_panier, date_ajout_ligne_panier) VALUES
(1, 1, 1, '2025-01-10'),
(2, 1, 2, '2025-01-11'),
(3, 2, 1, '2025-01-12'),
(5, 3, 3, '2025-01-13');



INSERT INTO commande_adresse (commande_id, nom_livraison, rue_livraison, code_postal_livraison, ville_livraison, nom_facturation, rue_facturation, code_postal_facturation, ville_facturation)
VALUES
(1, 'John Doe', '123 Rue de Paris', '75001', 'Paris', 'John Doe', '123 Rue de Paris', '75001', 'Paris'),
(2, 'Jane Smith', '456 Avenue de la République', '69001', 'Lyon', 'Jane Smith', '456 Avenue de la République', '69001', 'Lyon'),
(3, 'Alice Johnson', '789 Boulevard Saint-Germain', '75005', 'Paris', 'Alice Johnson', '789 Boulevard Saint-Germain', '75005', 'Paris');



SELECT * FROM type_boisson;
SELECT * FROM arome;
SELECT * FROM boisson;
SELECT * FROM commande;
SELECT * FROM ligne_commande;
SELECT * FROM ligne_panier;

SELECT
    boisson.nom_boisson AS nom,
    boisson.id_boisson AS id_article,
    boisson.stock_boisson AS stock,
    boisson.type_boisson_id AS type_article_id,
    type_boisson.nom_type_boisson AS libelle
FROM boisson
INNER JOIN type_boisson ON boisson.type_boisson_id = type_boisson.id_type_boisson
ORDER BY boisson.type_boisson_id;

SELECT
    boisson.id_boisson AS id,
    boisson.nom_boisson AS nom,
    boisson.arome_id AS id_arome,
    arome.nom_arome AS nom_arome
FROM boisson
INNER JOIN arome ON arome.id_arome=boisson.arome_id
ORDER BY boisson.id_boisson;

SELECT
    commande.id_commande AS id_commade,
    etat.libelle_etat AS etat
FROM commande
INNER JOIN etat ON commande.etat_id=etat.id_etat;

SELECT
    boisson.nom_boisson AS boisson,
    ligne_commande.quantite_ligne_commande
FROM ligne_commande
INNER JOIN boisson ON boisson.id_boisson=ligne_commande.boisson_id;

SELECT
    utilisateur.nom AS utilisateur,
    ligne_panier.date_ajout_ligne_panier
FROM ligne_panier
INNER JOIN utilisateur ON utilisateur.id_utilisateur=ligne_panier.utilisateur_id;
