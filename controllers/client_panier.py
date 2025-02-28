#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    db = get_db()
    mycursor = db.cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')

    sql = '''SELECT * FROM ligne_panier WHERE boisson_id = %s AND utilisateur_id = %s'''
    mycursor.execute(sql, (id_article, id_client))
    articles_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM boisson WHERE id_boisson = %s", (id_article,))
    article = mycursor.fetchone()

    if not (articles_panier is None) and article['stock_boisson'] >=int(quantite):
        tuple_update = (quantite, id_client, id_article)
        sql = '''UPDATE ligne_panier SET quantite_ligne_panier = quantite_ligne_panier+%s WHERE utilisateur_id = %s AND boisson_id = %s'''
        mycursor.execute(sql, tuple_update)
        sql = '''UPDATE boisson SET stock_boisson = stock_boisson-%s WHERE id_boisson = %s'''
        mycursor.execute(sql, (quantite, id_article))
    else:
        if article['stock_boisson'] >= int(quantite):
            tuple_insert = (id_article, id_client, quantite)
            sql = '''INSERT INTO ligne_panier(boisson_id ,utilisateur_id, quantite_ligne_panier, date_ajout_ligne_panier) VALUES (%s, %s, %s, current_timestamp )'''
            mycursor.execute(sql, tuple_insert)
            sql = '''UPDATE boisson SET stock_boisson = stock_boisson-%s WHERE id_boisson = %s'''
            mycursor.execute(sql, (quantite, id_article))

    db.commit()
    return redirect('/client/article/show')
    # ---------
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

# ajout dans le panier d'un article


    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():

    id_client = session['id_user']
    id_article = request.form.get('id_article','')
    # print("ID ARTICLE : ",id_article)
    # print("ID UTILISATEUR : ", id_client)
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)
    mycursor = get_db().cursor()
    sqlBoisson = ''' 
        SELECT 
            ligne_panier.quantite_ligne_panier AS quantite
        FROM ligne_panier
        WHERE ligne_panier.boisson_id = %s AND ligne_panier.utilisateur_id=%s ;
    '''
    mycursor.execute(sqlBoisson,(id_article,id_client))
    article_panier=mycursor.fetchone()
    # print("VOICI L'ARTICLE DONT ON VEUT ENLEVER UN ELEMENT DANS LE PANIER : ",article_panier)

    if not(article_panier is None) and article_panier['quantite'] > 1:
        # print("LA QUANTITE EST SUPERIEUR À 1")

        db = get_db()
        mycursor = db.cursor()
        sqlEnleve = ''' UPDATE ligne_panier SET ligne_panier.quantite_ligne_panier=ligne_panier.quantite_ligne_panier-1 WHERE ligne_panier.boisson_id = %s ;'''
        mycursor.execute(sqlEnleve, id_article)
        db.commit()

    else:
        # print("LA QUANTITE EST ÉGALE À 1")
        db = get_db()
        mycursor = db.cursor()
        sqlDelete = ''' DELETE FROM ligne_panier WHERE ligne_panier.boisson_id = %s AND ligne_panier.utilisateur_id=%s;'''
        mycursor.execute(sqlDelete, (id_article, id_client))
        db.commit()

    db = get_db()
    mycursor = db.cursor()
    sqlAjout = '''UPDATE boisson SET boisson.stock_boisson = boisson.stock_boisson+1 WHERE boisson.id_boisson = %s; '''
    mycursor.execute(sqlAjout, id_article)
    db.commit()



@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite=request.form.get('quantite')
    #print("ID UTILISATEUR : ",id_client)
    #print("ID ARTICLE : ", id_article)
    #print("QUANTITÉ : ", quantite)

    mycursor = get_db().cursor()
    sqlLigne = '''  
    SELECT
        ligne_panier.quantite_ligne_panier AS quantite
    FROM ligne_panier
    WHERE ligne_panier.boisson_id = %s AND ligne_panier.utilisateur_id = %s ;'''
    mycursor.execute(sqlLigne,(id_article,id_client))
    ligne=mycursor.fetchone()
    #print(ligne)

    db = get_db()
    mycursor = db.cursor()
    sqlDelete = ''' DELETE FROM ligne_panier WHERE ligne_panier.boisson_id = %s AND ligne_panier.utilisateur_id=%s;'''
    mycursor.execute(sqlDelete, (id_article, id_client))
    db.commit()

    db = get_db()
    mycursor = db.cursor()
    sqlAjout = '''UPDATE boisson SET boisson.stock_boisson = boisson.stock_boisson+%s WHERE boisson.id_boisson = %s; '''
    mycursor.execute(sqlAjout,(quantite, id_article))
    db.commit()

    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    id_client = session['id_user']
    #print("ID UTILISATEUR : ", id_client)

    mycursor=get_db().cursor()
    sqlPanier = '''
        SELECT 
            ligne_panier.boisson_id AS id_boisson,
            ligne_panier.quantite_ligne_panier AS quantite
            
        FROM ligne_panier
        WHERE ligne_panier.utilisateur_id = %s;'''
    mycursor.execute(sqlPanier,id_client)
    items_panier=mycursor.fetchall()
    #print(items_panier)

    for item in items_panier:
        #print(item)
        id_boisson=item['id_boisson']
        quantite=item['quantite']
        #print('ID BOISSON : ',id_boisson)
        #print('QUANTITE : ',quantite)

        db = get_db()
        mycursor = db.cursor()
        sqlDelete = ''' DELETE FROM ligne_panier WHERE ligne_panier.boisson_id=%s AND ligne_panier.utilisateur_id=%s;'''
        mycursor.execute(sqlDelete, (id_boisson, id_client))
        db.commit()

        db = get_db()
        mycursor = db.cursor()
        sqlAjout='''UPDATE boisson SET boisson.stock_boisson = boisson.stock_boisson+%s WHERE boisson.id_boisson = %s;'''
        mycursor.execute(sqlAjout, (quantite,id_boisson))
        db.commit()

    return redirect('/client/article/show')



@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    #print("LA LISTE DES TYPE BOISSONS DU FILTRE EST : ",filter_types)

    if (filter_word and filter_word!=""):
        session["filter_word"] = filter_word
    if (filter_prix_min and filter_prix_min!=""):
        session["filter_prix_min"] = filter_prix_min
    if (filter_prix_max and filter_prix_max!=""):
        session["filter_prix_max"] = filter_prix_max
    if (filter_types and filter_types!=[]):
        session['filter_types']=[]
        for i in filter_types:
            session['filter_types'].append(i)


    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():

    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)

    print("suppr filtre")
    return redirect('/client/article/show')
