from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import db
from .models import User, Dkey, Message
import random
from werkzeug.security import generate_password_hash, check_password_hash
from .views import home
from flask_login import login_user, logout_user, login_required, current_user
global numlogin
auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
           flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Passwords don\'t match.', category='error') 
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
        
    return render_template('sign_up.html') 

NUMLOGIN = 0

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):   
                flash('logged in, succesfully!', category ='success')
                login_user(user, remember=True)
                existing_note = Dkey.query.filter_by(user_id=current_user.id).first()
                session['user_id'] = user.id

                if existing_note:
                    print(existing_note.dkey)
                    print("hey")
                    login_user(user, remember=True)                    
                else:
                    print("hello")
                    login_user(user, remember=True)
                    dkey = random.randint(10000, 99999)
                    print(dkey)
                    new_user = Dkey(dkey=dkey, user_id=current_user.id)
                    db.session.add(new_user)
                    db.session.commit()                    
                return redirect(url_for('views.home'))
            else: 
                flash('Incorrect password, try again', category='error')
    
    return render_template('login.html', user=current_user)

@auth.route('/dkey', methods=['GET', 'POST'])
def dkey():
    if request.method == 'POST':
        dkey_input = request.form.get('dkey')

        dkey = Dkey.query.filter_by(dkey=dkey_input).first()
        if dkey:
            user = User.query.get(dkey.user_id)  # Get the associated User
            if user:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                print(dkey_input)
                return redirect(url_for('views.index2'))
            else:
                flash('User not found for this dkey.', category='error')
        else:
            flash('Invalid dkey. Please try again.', category='error')
    
    return render_template('dkey.html', user=current_user)
