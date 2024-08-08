import sqlite3
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

class User(UserMixin):
    def __init__(self, id, nom, email):
        self.id = id
        self.nom = nom
        self.email = email

    @staticmethod
    def get(user_id):
        try:
            with sqlite3.connect('data.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id_utilisateur, nom, email FROM utilisateurs WHERE id_utilisateur = ?', (user_id,))
                user = cursor.fetchone()
                if user:
                    return User(user[0], user[1], user[2])
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
        return None

def recherche_utilisateur(nom_utilisateur, mot_de_passe):
    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id_utilisateur, nom, email, mot_de_passe FROM utilisateurs WHERE nom = ?', (nom_utilisateur,))
            utilisateur = cursor.fetchone()
            if utilisateur and utilisateur[3] and bcrypt.check_password_hash(utilisateur[3], mot_de_passe):
                return User(utilisateur[0], utilisateur[1], utilisateur[2])
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    return None
