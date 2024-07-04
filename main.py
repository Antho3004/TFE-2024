from flask import Flask, render_template, request, redirect, url_for, session, flash
from inscription import ajouter_utilisateur, bcrypt
from connexion import recherche_utilisateur

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
            flash('Utilisateur ajouté avec succès! Connectez-vous maintenant.', 'success')
            return redirect(url_for('index'))  # Redirection vers la page d'accueil après inscription
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

        if not nom or not mdp:
            flash('Nom d\'utilisateur et mot de passe sont requis', 'danger')
            return redirect(request.url)

        utilisateur = recherche_utilisateur(nom, mdp)

        if utilisateur is not None:
            session['nom_utilisateur'] = utilisateur['nom']
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
            return redirect(request.url)
    else:
        if 'nom_utilisateur' in session:
            return redirect(url_for('index'))
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('nom_utilisateur', None)
    return redirect(url_for('login'))

@app.route("/traitement", methods=["POST", "GET"])
def traitement():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')
        if nom == 'admin' and mdp == '1234':
            return render_template("traitement.html", nom_utilisateur=nom)
        else:
            return render_template("traitement.html")
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
