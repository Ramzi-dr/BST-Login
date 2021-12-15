
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    '''if form.validate_on_submit():
        name = form.username.data
        vorname = form.uservorname.data
        firmaname = form.firmaname.data
        email = form.email.data
        password = form.confirm_password.data

       # email existing control:
        email_found = BST_records.find_one({"Email": email})
        if email_found:
            message = 'Diese E-email existiert bereits in der Datenbank'
            flash(message, 'danger')
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_input = {
                'Name': name,
                'Vorname': vorname,
                'Firma': firmaname,
                'Email': email,
                'Passwort': hashed_password
            }
            try:
                BST_records.insert_one(user_input)
                result = BST_records.insert_one(user_input)
                flash('Ihr Konto wurde erstellt! Sie können sich jetzt einloggen', 'success')
                return redirect(url_for('login'))
            except pymongo.errors.DuplicateKeyError:
                flash('Ihr Konto wurde erstellt! Sie können sich jetzt einloggen', 'success')
                return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)'''


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        '''email = form.email.data
        password = form.password.data
        email_found = BST_records.find_one({"Email": email})
        print(email_found)
        if email_found:
            passwordCheck = email_found['Passwort']
            if bcrypt.checkpw(password.encode('utf-8'), passwordCheck):
                flash('Sie sind eingeloggt!', 'success')
                return redirect(url_for('home'))

            else:
                flash('Anmeldung nicht erfolgreich. Bitte E-Mail und Passwort prüfen', 'danger')
        else:
            flash('Anmeldung nicht erfolgreich. Bitte E-Mail und Passwort prüfen', 'danger')'''
    return render_template('/login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

