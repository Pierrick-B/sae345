#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    sql = '''
    DROP TABLE IF EXISTS ligne_panier,
                        ligne_commande,
                        commande,
                        boisson,
                        etat,
                        utilisateur,
                        arome,
                        type_boisson;
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE type_boisson(
       id_type_boisson INT AUTO_INCREMENT,
       nom_type_boisson VARCHAR(255),
       PRIMARY KEY(id_type_boisson)
    );
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE arome(
       id_arome INT AUTO_INCREMENT,
       nom_arome VARCHAR(255),
       PRIMARY KEY(id_arome)
    );
    '''
    mycursor.execute(sql)

    sql = '''
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
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE etat(
       id_etat INT AUTO_INCREMENT,
       libelle_etat VARCHAR(255),
       PRIMARY KEY(id_etat)
    );
    '''
    mycursor.execute(sql)

    sql = '''
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
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE commande(
       id_commande INT AUTO_INCREMENT,
       date_achat_commande DATE,
       etat_id INT NOT NULL,
       utilisateur_id INT NOT NULL,
       PRIMARY KEY(id_commande),
       FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
       FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
    );
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE ligne_commande(
       boisson_id INT NOT NULL,
       commande_id INT NOT NULL,
       quantite_ligne_commande INT,
       prix_ligne_commande DECIMAL(15,2),
       PRIMARY KEY(boisson_id, commande_id),
       FOREIGN KEY(boisson_id) REFERENCES boisson(id_boisson),
       FOREIGN KEY(commande_id) REFERENCES commande(id_commande)
    );
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE ligne_panier(
       boisson_id INT NOT NULL,
       utilisateur_id INT NOT NULL,
       quantite_ligne_panier INT,
       date_ajout_ligne_panier VARCHAR(255),
       PRIMARY KEY(boisson_id, utilisateur_id),
       FOREIGN KEY(boisson_id) REFERENCES boisson(id_boisson),
       FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
    );
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO type_boisson (nom_type_boisson) VALUES
    ('Soda'), ('Jus de fruit'), ('Alcool'), ('Hydratant');
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO arome (nom_arome) VALUES
    ('Sans arôme'), ('Cola'), ('Cerise'), ('Orange'), ('Citron'), ('Framboise'),
    ('Fraise'), ('Pêche'), ('Pomme'), ('Raisin'), ('Mangue'), ('Tropical'),
    ('Multifruits'), ('Cassis'), ('Ananas'), ('Autre');
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO utilisateur (id_utilisateur, login, email, password, role, nom, est_actif) VALUES
    (1, 'admin', 'admin@admin.fr', 'hash1', 'ROLE_admin', 'admin', 1),
    (2, 'client', 'client@client.fr', 'hash2', 'ROLE_client', 'client', 1),
    (3, 'client2', 'client2@client2.fr', 'hash3', 'ROLE_client', 'client2', 1);
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO etat (id_etat, libelle_etat) VALUES
    (1, 'En préparation'), (2, 'Expédiée');
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO boisson (nom_boisson, prix_boisson, volume_boisson, description_boisson, fournisseur_boisson, marque_boisson, photo_boisson, stock_boisson, type_boisson_id, arome_id) VALUES
    ('Coca-Cola', 1.50, '330ml', 'Boisson gazeuse au goût de Cola', 'Coca-Cola Company', 'Coca-Cola', 'coca_cola.png', 12, 1, 2),
    ('Fanta Orange', 1.50, '330ml', 'Boisson gazeuse sucrée au goût d''orange', 'Coca-Cola Company', 'Fanta', 'fanta_orange.png', 14, 1, 4),
    ('Whisky', 49.90, '750ml', 'Whisky écossais de grande qualité', 'Diageo', 'Johnnie Walker', 'whisky.png', 14, 3, 16);
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO commande (date_achat_commande, etat_id, utilisateur_id) VALUES
    ('2025-01-15', 1, 2),
    ('2025-01-16', 2, 2),
    ('2025-01-17', 2, 3);
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO ligne_commande (boisson_id, commande_id, quantite_ligne_commande, prix_ligne_commande) VALUES
    (1, 1, 2, 99.80),
    (2, 1, 1, 25.50),
    (3, 2, 3, 96.00);
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO ligne_panier (boisson_id, utilisateur_id, quantite_ligne_panier, date_ajout_ligne_panier) VALUES
    (1, 2, 1, '2025-01-10'),
    (2, 2, 2, '2025-01-11'),
    (3, 3, 1, '2025-01-12');
    '''
    mycursor.execute(sql)

    get_db().commit()

    return redirect('/')
