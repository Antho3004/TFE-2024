import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def ajouter_utilisateur(nom, prenom, email, mot_de_passe):
    mot_de_passe_hache = bcrypt.generate_password_hash(mot_de_passe).decode('utf-8')
    
    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe)
                VALUES (?, ?, ?, ?)
            ''', (nom, prenom, email, mot_de_passe_hache))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False
