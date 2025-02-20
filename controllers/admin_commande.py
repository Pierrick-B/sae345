#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''SELECT 
                commande.id_commande, 
                commande.etat_id, 
                utilisateur.login, 
                commande.date_achat_commande AS date_achat, 
                SUM(ligne_commande.quantite_ligne_commande) AS nombre_boissons, 
                SUM(ligne_commande.prix_ligne_commande * ligne_commande.quantite_ligne_commande) AS cout_total, 
                etat.libelle_etat AS etat_commande
            FROM commande
            INNER JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
            INNER JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
            INNER JOIN etat ON commande.etat_id = etat.id_etat
            GROUP BY commande.id_commande, commande.etat_id
            ORDER BY commande.etat_id ASC;'''

    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    # print(id_commande)
    if id_commande != None:
        sql = '''
            SELECT 
                utilisateur.nom AS nom_client,
                utilisateur.login AS login_client,
                utilisateur.email AS email_client,
                boisson.nom_boisson AS nom,
                ligne_commande.quantite_ligne_commande AS quantite, 
                ligne_commande.prix_ligne_commande AS prix, 
                (ligne_commande.quantite_ligne_commande * ligne_commande.prix_ligne_commande) AS prix_ligne
            FROM ligne_commande
            INNER JOIN boisson ON ligne_commande.boisson_id = boisson.id_boisson
            INNER JOIN commande ON ligne_commande.commande_id = commande.id_commande
            INNER JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
            WHERE ligne_commande.commande_id = %s;
        '''

        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

        commande_adresses = []
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['GET', 'POST'])
def admin_commande_valider():
    db = get_db()
    mycursor = db.cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id is not None:
        print("Bouton valide commande id : ", commande_id)
        sql = '''UPDATE commande SET etat_id = 2 WHERE id_commande = %s;'''
        mycursor.execute(sql, (commande_id,))
        db.commit()
    return redirect('/admin/commande/show')

