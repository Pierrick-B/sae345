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
    sql = ''' selection des articles d'un panier 
    '''
    articles_panier = []
    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = ''' selection du contenu du panier de l'utilisateur '''
    items_ligne_panier = []
    # if items_ligne_panier is None or len(items_ligne_panier) < 1:
    #     flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
    #     return redirect('/client/article/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    #a = datetime.strptime('my date', "%b %d %Y %H:%M")

    sql = ''' creation de la commande '''

    sql = '''SELECT last_insert_id() as last_insert_id'''
    # numéro de la dernière commande
    for item in items_ligne_panier:
        sql = ''' suppression d'une ligne de panier '''
        sql = "  ajout d'une ligne de commande'"

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT 
            commande.id_commande, 
            commande.date_achat_commande, 
            COUNT(ligne_commande.boisson_id) AS nbr_articles, 
            SUM(ligne_commande.prix_ligne_commande * ligne_commande.quantite_ligne_commande) AS cout_total, 
            commande.etat_id, 
            utilisateur.login 
            FROM 
            commande
            JOIN 
                ligne_commande ON commande.id_commande = ligne_commande.commande_id
            JOIN 
                utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur  -- Changer id_client par utilisateur_id
            WHERE 
                utilisateur.id_utilisateur = %s
            GROUP BY 
                commande.id_commande, commande.date_achat_commande, commande.etat_id, utilisateur.login
            ORDER BY 
                commande.etat_id, commande.date_achat_commande DESC;


'''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()
    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' selection du détails d'une commande '''

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

