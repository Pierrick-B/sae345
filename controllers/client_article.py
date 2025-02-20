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

    sqlBoisson = '''
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
            WHERE 1=1
        '''

    # print("CECI EST LA SESSION : ", session)

    if 'filter_word' in session:
        sqlBoisson+=f" AND boisson.nom_boisson LIKE '%{session['filter_word']}%'"
    if (session.get('filter_prix_min')):
        sqlBoisson+=f" AND boisson.prix_boisson > {session['filter_prix_min']} "
    if (session.get('filter_prix_max')):
        sqlBoisson+=f" AND boisson.prix_boisson < {session['filter_prix_max']} "
    if (session.get('filter_types')):
        sqlBoisson+=f" AND (boisson.type_boisson_id={session['filter_types'][0]}"
        for id in session['filter_types']:
            sqlBoisson+=f" OR boisson.type_boisson_id={id}"
        sqlBoisson+=f") "

    sqlBoisson += f" ORDER BY boisson.nom_boisson;"
    mycursor.execute(sqlBoisson)
    boissons = mycursor.fetchall()
    articles = boissons


    id_client = session['id_user']
    # print(id_client)
    mycursor = get_db().cursor()

    sqlPanier='''
    SELECT
        boisson.id_boisson AS id_article,
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

    mycursor = get_db().cursor()
    sqlTypeBoisson='''
    SELECT 
        type_boisson.id_type_boisson AS id_type_article,
        type_boisson.nom_type_boisson AS libelle
    FROM type_boisson;
    '''
    mycursor.execute(sqlTypeBoisson)
    types_article = mycursor.fetchall()
    # print(types_article)


    if len(articles_panier) >= 1:
        mycursor = get_db().cursor()

        sqlPrixTot = '''           
            SELECT 
                SUM(boisson.prix_boisson * ligne_panier.quantite_ligne_panier) AS prix_total
            FROM utilisateur 
            INNER JOIN ligne_panier ON ligne_panier.utilisateur_id=utilisateur.id_utilisateur
            INNER JOIN boisson ON boisson.id_boisson=ligne_panier.boisson_id
            WHERE utilisateur.id_utilisateur=%s
            GROUP BY utilisateur.id_utilisateur;
         '''

        mycursor.execute(sqlPrixTot, id_client)
        prix_total = mycursor.fetchone()
        # print("LE PRIX TOT EST : ",prix_total)
    else:
        prix_total = None



    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           )
