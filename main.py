from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from inscription import ajouter_utilisateur, bcrypt
from connexion import recherche_utilisateur, User
from heure_type import ajouter_heure_type, obtenir_heures_type, obtenir_heure_type, modifier_heure_type, supprimer_heure_type

app = Flask(__name__)
app.secret_key = "2fb48ed61fe5f62c7ea52bd58128ca1179fdd8b162ac4cacc3da03e83a0b053f"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        if ajouter_utilisateur(nom, prenom, email, mot_de_passe):
            utilisateur = recherche_utilisateur(nom, mot_de_passe)
            login_user(utilisateur)
            flash('Inscription réussie et connecté!', 'success')
            return redirect(url_for('traitement'))
        else:
            flash('Erreur: cet email est déjà utilisé.', 'danger')
        return redirect(url_for('inscription'))

    return render_template('inscription.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nom = request.form['nom']
        mot_de_passe = request.form['mot_de_passe']
        utilisateur = recherche_utilisateur(nom, mot_de_passe)
        
        if utilisateur:
            login_user(utilisateur)
            return redirect(url_for('traitement'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/traitement', methods=['GET', 'POST'])
@login_required
def traitement():
    if request.method == 'POST':
        heure = int(request.form['heure'])
        minutes = int(request.form['minutes'])
        heure_combinee = heure * 100 + minutes
        date = request.form['date']
        id_utilisateur = current_user.id

        if ajouter_heure_type(heure_combinee, date, id_utilisateur):
            flash('Heure de réveil ajoutée avec succès!', 'success')
        else:
            flash('Erreur: une heure de réveil avec cette date existe déjà.', 'danger')
        
        return redirect(url_for('traitement'))
    else:
        id_utilisateur = current_user.id
        heures = obtenir_heures_type(id_utilisateur)
        return render_template("traitement.html", heures=heures)

@app.route('/modifier/<int:heure>/<date>', methods=['GET', 'POST'])
@login_required
def modifier_heure_route(heure, date):
    id_utilisateur = current_user.id

    if request.method == 'POST':
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

@app.route('/supprimer/<int:heure>/<date>')
@login_required
def supprimer_heure_route(heure, date):
    id_utilisateur = current_user.id

    if supprimer_heure_type(heure, date, id_utilisateur):
        flash('Heure de réveil supprimée avec succès!', 'success')
    else:
        flash('Erreur lors de la suppression de l\'heure de réveil.', 'danger')
    
    return redirect(url_for('traitement'))

@app.route('/get_heures')
@login_required
def get_heures():
    id_utilisateur = current_user.id
    heures = obtenir_heures_type(id_utilisateur)

    events = []
    for heure in heures:
        events.append({
            'title': str(heure[0]),
            'start': heure[1],
            'heure': heure[0]
        })
    
    return jsonify(events)

@app.route('/add_heure', methods=['POST'])
@login_required
def add_heure():
    data = request.get_json()
    heure = int(data['heure'])
    date = data['date']
    id_utilisateur = current_user.id

    ajouter_heure_type(heure, date, id_utilisateur)
    return '', 204

@app.route('/delete_heure', methods=['POST'])
@login_required
def delete_heure():
    heure = int(request.form['heure'])
    date = request.form['date']
    id_utilisateur = current_user.id

    supprimer_heure_type(heure, date, id_utilisateur)
    return '', 204

@app.route('/modify_heure', methods=['POST'])
@login_required
def modify_heure():
    old_heure = int(request.form['old_heure'])
    new_heure = int(request.form['new_heure'])
    date = request.form['date']
    id_utilisateur = current_user.id

    if modifier_heure_type(old_heure, date, new_heure, date, id_utilisateur):
        return '', 204
    else:
        return jsonify({'error': 'Modification échouée'}), 400

if __name__ == '__main__':
    app.run(debug=True)
