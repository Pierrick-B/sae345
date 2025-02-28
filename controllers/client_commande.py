#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db



client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
        SELECT 
            boisson.nom_boisson AS nom,
            boisson.id_boisson AS id_article,
            ligne_panier.quantite_ligne_panier AS quantite,
            boisson.prix_boisson AS prix,
            boisson.photo_boisson AS image
        FROM ligne_panier
        INNER JOIN boisson ON ligne_panier.boisson_id = boisson.id_boisson
        WHERE ligne_panier.utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = '''
            SELECT SUM(boisson.prix_boisson * ligne_panier.quantite_ligne_panier) AS prix_total
            FROM ligne_panier
            INNER JOIN boisson ON ligne_panier.boisson_id = boisson.id_boisson
            WHERE ligne_panier.utilisateur_id = %s
        '''
        mycursor.execute(sql, (id_client,))
        prix_total = mycursor.fetchone()
    else:
        prix_total = None

    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           # , adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , validation=1
                           # , id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    db = get_db()
    mycursor = db.cursor()

    # choix de(s) (l')adresse(s)
    nom_livraison = request.form.get('nom_livraison', '')
    rue_livraison = request.form.get('rue_livraison', '')
    code_postal_livraison = request.form.get('code_postal_livraison', '')
    ville_livraison = request.form.get('ville_livraison', '')

    nom_facturation = request.form.get('nom_facturation', '')
    rue_facturation = request.form.get('rue_facturation', '')
    code_postal_facturation = request.form.get('code_postal_facturation', '')
    ville_facturation = request.form.get('ville_facturation', '')

    id_client = session['id_user']
    sql = '''
        SELECT 
            boisson.id_boisson AS id_article,
            ligne_panier.quantite_ligne_panier AS quantite,
            boisson.prix_boisson AS prix
        FROM ligne_panier
        INNER JOIN boisson ON ligne_panier.boisson_id = boisson.id_boisson
        WHERE ligne_panier.utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le panier', 'alert-warning')
        return redirect('/client/article/show')

    # Transaction start
    try:
        # Création de la commande
        sql = '''
            INSERT INTO commande (date_achat_commande, etat_id, utilisateur_id)
            VALUES (CURRENT_DATE(), 1, %s)
        '''
        mycursor.execute(sql, (id_client,))

        # Récupération de l'ID de la dernière commande
        sql = '''SELECT last_insert_id() as last_insert_id'''
        mycursor.execute(sql)
        last_insert_id = mycursor.fetchone()['last_insert_id']

        # Ajout des adresses de livraison et facturation
        sql = '''
            INSERT INTO commande_adresse 
            (commande_id, nom_livraison, rue_livraison, code_postal_livraison, ville_livraison, 
            nom_facturation, rue_facturation, code_postal_facturation, ville_facturation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        mycursor.execute(sql, (
            last_insert_id,
            nom_livraison, rue_livraison, code_postal_livraison, ville_livraison,
            nom_facturation, rue_facturation, code_postal_facturation, ville_facturation
        ))

        # Ajout des lignes de commande et suppression du panier
        for item in items_ligne_panier:
            # Suppression d'une ligne de panier
            sql = '''
                DELETE FROM ligne_panier 
                WHERE boisson_id = %s AND utilisateur_id = %s
            '''
            mycursor.execute(sql, (item['id_article'], id_client))

            # Ajout d'une ligne de commande
            sql = '''
                INSERT INTO ligne_commande 
                (boisson_id, commande_id, quantite_ligne_commande, prix_ligne_commande)
                VALUES (%s, %s, %s, %s)
            '''
            prix_ligne = item['prix'] * item['quantite']
            mycursor.execute(sql, (item['id_article'], last_insert_id, item['quantite'], prix_ligne))

        db.commit()
        flash(u'Commande ajoutée', 'alert-success')

    except Exception as e:
        db.rollback()
        flash(u'Erreur lors de l\'ajout de la commande: ' + str(e), 'alert-danger')

    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT 
            commande.id_commande, 
            commande.date_achat_commande AS date_achat, 
            SUM(ligne_commande.quantite_ligne_commande) AS nbr_articles, 
            SUM(ligne_commande.quantite_ligne_commande * boisson.prix_boisson) AS cout_total, -- Calcul de cout_total avec SUM
            commande.etat_id, 
            utilisateur.login 
            FROM 
                commande
            JOIN 
                ligne_commande ON commande.id_commande = ligne_commande.commande_id
            JOIN 
                boisson ON ligne_commande.boisson_id = boisson.id_boisson
            JOIN 
                utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur  
            WHERE 
                utilisateur.id_utilisateur = %s
            GROUP BY 
                commande.id_commande, 
                commande.date_achat_commande, 
                commande.etat_id, 
                utilisateur.login
            ORDER BY 
                commande.etat_id, 
                commande.date_achat_commande DESC;
'''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()
    articles_commande = []
    commande_adresses = ""
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = '''SELECT 
                boisson.nom_boisson AS nom,
                ligne_commande.quantite_ligne_commande AS quantite, 
                boisson.prix_boisson AS prix, 
                (ligne_commande.quantite_ligne_commande * boisson.prix_boisson) AS prix_ligne
                FROM ligne_commande
                INNER JOIN boisson ON ligne_commande.boisson_id = boisson.id_boisson
                INNER JOIN commande ON ligne_commande.commande_id = commande.id_commande
                INNER JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
                WHERE ligne_commande.commande_id = %s;
                '''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()
        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = '''SELECT 
                    commande_adresse.nom_livraison,
                    commande_adresse.rue_livraison,
                    commande_adresse.code_postal_livraison,
                    commande_adresse.ville_livraison,
                    commande_adresse.nom_facturation,
                    commande_adresse.rue_facturation,
                    commande_adresse.code_postal_facturation,
                    commande_adresse.ville_facturation,
                    CASE
                        WHEN commande_adresse.nom_livraison = commande_adresse.nom_facturation
                            AND commande_adresse.rue_livraison = commande_adresse.rue_facturation
                            AND commande_adresse.code_postal_livraison = commande_adresse.code_postal_facturation
                            AND commande_adresse.ville_livraison = commande_adresse.ville_facturation
                        THEN 'adresse_identique'
                        ELSE 'adresse_différente'
                    END AS adresse_identique
                FROM commande_adresse
                WHERE commande_adresse.commande_id = %s;'''
        mycursor.execute(sql, (id_commande,))
        commande_adresses = mycursor.fetchone()
    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )