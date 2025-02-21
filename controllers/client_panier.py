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
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = ''' SELECT * FROM ligne_panier WHERE id_boisson = %s AND utilisateur_id = %s'''
    article_panier=[]
    mycursor.execute(sql, (id_client, id_article))
    article_panier = mycursor.fetchone()


    if not(article_panier is None) and article_panier['quantite'] > 1:
        tuple_update = (quantite, id_client, id_article)
        sql = '''UPDATE ligne_panier SET quantite_ligne_panier = quantite_ligne_panier+%s WHERE utilisateur_id = %s AND id_boisson = %s'''
        mycursor.execute(sql, tuple_update)
    else:
        tuple_insert = (id_client, id_article, quantite)
        sql = '''DELETE FROM ligne_panier(utilisateur_id, id_boisson, quantite_ligne_panier, date_ajout_ligne_panier) VALUES (%s, %s, %s, current_timestop )'''
        mycursor.execute(sql, tuple_insert)

    # mise à jour du stock de l'article disponible
    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' SELECT * FROM ligne_panier'''
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de l'article pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_article = request.form.get('id_declinaison_article')

    sql = ''' selection de ligne du panier '''

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    print("LA LISTE DES TYPE BOISSONS DU FILTRE EST : ",filter_types)



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

    # test des variables puis
    # mise en session des variables
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)

    print("suppr filtre")
    return redirect('/client/article/show')
