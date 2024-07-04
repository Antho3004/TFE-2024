import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def recherche_utilisateur(nom_utilisateur, mot_de_passe):
    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT nom, mot_de_passe FROM utilisateurs WHERE nom = ?
            ''', (nom_utilisateur,))
            utilisateur = cursor.fetchone()
            if utilisateur and utilisateur[1]:
                if bcrypt.check_password_hash(utilisateur[1], mot_de_passe):
                    return {"nom": utilisateur[0]}
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    return None
