from flask import Flask, render_template, request, redirect, url_for, session, flash
from inscription import ajouter_utilisateur, bcrypt
from connexion import recherche_utilisateur
from heure_type import ajouter_heure_type, obtenir_heures_type, obtenir_heure_type, modifier_heure_type, supprimer_heure_type

app = Flask(__name__)
app.secret_key = "2fb48ed61fe5f62c7ea52bd58128ca1179fdd8b162ac4cacc3da03e83a0b053f"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        if ajouter_utilisateur(nom, prenom, email, mot_de_passe):
            utilisateur = recherche_utilisateur(nom, mot_de_passe)
            session['nom_utilisateur'] = utilisateur['nom']
            session['id_utilisateur'] = utilisateur['id']
            flash('Inscription réussie et connecté!', 'success')
            return redirect(url_for('traitement'))
        else:
            flash('Erreur: cet email est déjà utilisé.', 'danger')
        return redirect(url_for('inscription'))

    return render_template('inscription.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mot_de_passe')

        utilisateur = recherche_utilisateur(nom, mdp)

        if utilisateur is not None:
            session['nom_utilisateur'] = utilisateur['nom']
            session['id_utilisateur'] = utilisateur['id']
            return redirect(url_for('traitement'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
            return redirect(request.url)
    else:
        if 'nom_utilisateur' in session:
            return redirect(url_for('traitement'))
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('nom_utilisateur', None)
    session.pop('id_utilisateur', None)
    return redirect(url_for('login'))

@app.route("/traitement", methods=["POST", "GET"])
def traitement():
    if 'nom_utilisateur' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        heure = int(request.form['heure'])
        minutes = int(request.form['minutes'])
        heure_combinee = heure * 100 + minutes
        date = request.form['date']
        id_utilisateur = session['id_utilisateur']

        if ajouter_heure_type(heure_combinee, date, id_utilisateur):
            flash('Heure de réveil ajoutée avec succès!', 'success')
        else:
            flash('Erreur: une heure de réveil avec cette date existe déjà.', 'danger')
        
        return redirect(url_for('traitement'))
    else:
        id_utilisateur = session['id_utilisateur']
        heures = obtenir_heures_type(id_utilisateur)
        return render_template("traitement.html", heures=heures)

@app.route("/modifier/<int:heure>/<date>", methods=["GET", "POST"])
def modifier_heure(heure, date):
    if 'nom_utilisateur' not in session:
        return redirect(url_for('login'))

    id_utilisateur = session['id_utilisateur']

    if request.method == "POST":
        nouvelle_heure = int(request.form['heure'])
        nouvelle_minutes = int(request.form['minutes'])
        nouvelle_heure_combinee = nouvelle_heure * 100 + nouvelle_minutes
        nouvelle_date = request.form['date']

        if modifier_heure_type(heure, date, nouvelle_heure_combinee, nouvelle_date, id_utilisateur):
            flash('Heure de réveil modifiée avec succès!', 'success')
        else:
            flash('Erreur: une heure de réveil avec cette date existe déjà.', 'danger')
        
        return redirect(url_for('traitement'))
    else:
        heure_type = obtenir_heure_type(heure, date, id_utilisateur)
        if heure_type:
            return render_template("modifier.html", heure=heure_type[0], date=heure_type[1])
        else:
            flash('Heure de réveil non trouvée.', 'danger')
            return redirect(url_for('traitement'))

@app.route("/supprimer/<int:heure>/<date>")
def supprimer_heure(heure, date):
    if 'nom_utilisateur' not in session:
        return redirect(url_for('login'))

    id_utilisateur = session['id_utilisateur']

    if supprimer_heure_type(heure, date, id_utilisateur):
        flash('Heure de réveil supprimée avec succès!', 'success')
    else:
        flash('Erreur lors de la suppression de l\'heure de réveil.', 'danger')
    
    return redirect(url_for('traitement'))

if __name__ == '__main__':
    app.run(debug=True)

