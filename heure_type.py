import sqlite3

def ajouter_heure_type(heure, date, id_utilisateur):
    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO type_reveil (heure, date, id_utilisateur) VALUES (?, ?, ?)
            ''', (heure, date, id_utilisateur))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return False

def obtenir_heures_type(id_utilisateur):
    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT heure, date FROM type_reveil WHERE id_utilisateur = ?
            ''', (id_utilisateur,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return []

def obtenir_heure_type(heure, date, id_utilisateur):
    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT heure, date FROM type_reveil WHERE heure = ? AND date = ? AND id_utilisateur = ?
            ''', (heure, date, id_utilisateur))
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return None

def modifier_heure_type(heure, date, nouvelle_heure, nouvelle_date, id_utilisateur):
    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE type_reveil SET heure = ?, date = ? WHERE heure = ? AND date = ? AND id_utilisateur = ?
            ''', (nouvelle_heure, nouvelle_date, heure, date, id_utilisateur))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return False

def supprimer_heure_type(heure, date, id_utilisateur):
    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM type_reveil WHERE heure = ? AND date = ? AND id_utilisateur = ?
            ''', (heure, date, id_utilisateur))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return False
