from datetime import timedelta
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, mail
from app.forms import RegistrationForm, LoginForm, ResetPasswordForm, RequestResetForm, LoginAdmin
from app.models import User
from flask_login import login_user, current_user, logout_user
from flask_mail import Message


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return render_template('server.html')
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        vorname = form.vorname.data
        firmaname = form.firmaname.data
        email = form.email.data.upper()
        password = form.confirm_password.data
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Diese E-Mail existiert in unserer Datenbank, bitte geben Sie eine andere ein!', 'warning')
            return render_template('register.html',title='Register', form=form)
        else:

            hashed_password = bcrypt.generate_password_hash(password)
            user = User(name=name, vorname=vorname, firmaname=firmaname, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Ihr Konto wurde erstellt! Sie können sich jetzt einloggen', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return render_template('server.html')
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.upper()
        password = form.password.data
        remember = form.remember.data
        print(remember)
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember,duration=timedelta(minutes=15))
            flash('Sie sind eingeloggt!', 'success')
            return render_template('server.html')

        else:
            flash('Anmeldung nicht erfolgreich. Bitte E-Mail und Passwort prüfen', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@app.route('/server', methods=['POST', 'GET'])
def logout():
    if request.form.get("submit_logout") == 'submit_logout':
        logout_user()
        return redirect(url_for('home'))
    logout_user()
    return redirect(url_for('home'))
    # return render_template('server.html')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Anfrage zum Zurücksetzen des Passworts',
                  sender='keine.Antwort@bst.einbruchschutz.com',
                  recipients=[user.email])
    msg.body = f'''Um Ihr Passwort zurückzusetzen, besuchen Sie den folgenden Link:
    
{url_for('reset_token', token=token, _external=True)}
(( DIESER LINK IST NUR 30 MINUTEN GÜlTIG ))

Wenn Sie diese Anfrage nicht gestellt haben, 
ignorieren Sie diese E-Mail einfach und es werden keine Änderungen vorgenommen.

Zentrum für Einbruchschutz
BST Sicherheitstechnik AG
Lagerhausweg 10, 3018 Bern
Tel: 031 997 55 55
E-Mail: info@einbruchschutz.ch
'''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return render_template('server.html')
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.upper()).first()
        if user is None:
            #'Diese E-Mail existiert nicht in unserer Datenbank!, '
             #     'Bitte wenden Sie sich an den Administrator der Firma BST '
            flash('Es wurde eine E-Mail mit Anweisungen zum Zurücksetzen Ihres Passworts gesendet.', 'warning')
            return redirect(url_for('reset_request'))

        send_reset_email(user)
        flash('Es wurde eine E-Mail mit Anweisungen zum Zurücksetzen Ihres Passworts gesendet.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Passwort zurücksetzen', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return render_template('server.html')
    user = User.verify_reset_token(token)
    if user is None:
        flash('Das ist ein ungültiges oder abgelaufenes Token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.confirm_password.data
        hashed_password = bcrypt.generate_password_hash(password)
        user.password = hashed_password
        db.session.commit()
        flash('Ihr Passwort wurde aktualisiert! Sie können sich jetzt einloggen', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Password zurücksetzen', form=form)


@app.route('/bst-admin', methods=['POST', 'GET'])
def Adminlogin():
    form = LoginAdmin()
    if form.validate_on_submit():
        email = form.email.data.upper()
        password = form.password.data
        admin = User.query.get(1)
        print(admin.email)
        if email == admin.email and bcrypt.check_password_hash(admin.password, password):
            login_user(admin)
            flash('Sie sind eingeloggt!', 'success')
            return render_template('server.html')
        else:
            flash('Anmeldung nicht erfolgreich. Bitte E-Mail und Passwort prüfen', 'danger')

    return render_template('bst-admin.html', title='Admin Login', form=form)

