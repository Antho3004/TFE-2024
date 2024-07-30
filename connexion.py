import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def recherche_utilisateur(nom_utilisateur, mot_de_passe):
    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id_utilisateur, nom, mot_de_passe FROM utilisateurs WHERE nom = ?
            ''', (nom_utilisateur,))
            utilisateur = cursor.fetchone()
            if utilisateur and utilisateur[2]:
                if bcrypt.check_password_hash(utilisateur[2], mot_de_passe):
                    return {"id": utilisateur[0], "nom": utilisateur[1]}
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    return None
