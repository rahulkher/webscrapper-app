from flask import render_template, redirect, url_for, request, flash, session
from app import app, db  # Ensure this import is correct
from .models import User  # Ensure relative imports for intra-package references


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)  # Securely hash and store the password
        db.session.add(new_user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('You have successfully logged in.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/prompt', methods=['GET', 'POST'])
def prompt():
    # Prompt logic here...
    return

@app.route('/logout')
def logout():
    # Logout logic here...
    return
