#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()

    sql = '''
            SELECT 
                boisson.nom_boisson AS nom,
                boisson.id_boisson AS id_article,
                boisson.prix_boisson AS prix,
                boisson.stock_boisson AS stock,
                boisson.photo_boisson AS image,
                type_boisson.nom_type_boisson AS libelle
            FROM boisson
            INNER JOIN type_boisson 
                ON boisson.type_boisson_id = type_boisson.id_type_boisson
            ORDER BY boisson.nom_boisson;
        '''
    mycursor.execute(sql)
    boissons = mycursor.fetchall()
    articles = boissons


    id_client = session['id_user']
    print(id_client)
    mycursor = get_db().cursor()

    sqlPanier='''
    SELECT
        boisson.nom_boisson AS nom,
        ligne_panier.quantite_ligne_panier AS quantite,
        boisson.prix_boisson AS prix
    FROM ligne_panier
    INNER JOIN boisson ON boisson.id_boisson=ligne_panier.boisson_id
    WHERE ligne_panier.utilisateur_id=%s;
    '''

    mycursor.execute(sqlPanier,id_client)
    boissons_panier = mycursor.fetchall()
    articles_panier = boissons_panier
    print(articles_panier)

    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    # articles =[]


    # pour le filtre
    types_article = []


    if len(articles_panier) >= 1:
        prix_total = None
        # mycursor = get_db().cursor()
        #
        # sqlPrixTot = '''
        #     SELECT
        #         boisson.prix_boisson * COUNT(ligne_panier.quantite_ligne_panier) AS prix_total
        #     FROM ligne_panier
        #     INNER JOIN boisson ON ligne_panier.boisson_id=boisson.id_boisson
        #     WHERE ligne_panier.utilisateur_id=2
        #     GROUP BY ligne_panier.boisson_id;
        #  '''
        #
        # mycursor.execute(sqlPrixTot, id_client)
        # prix_total = mycursor.fetchone()
        # print(prix_total)
    else:
        prix_total = None



    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article
                           )
