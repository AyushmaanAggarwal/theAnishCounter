from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        full_name = request.form.get('fullName')
        username = request.form.get('username')
        email = request.form.get('email')
        email_auth = random.uniform(100000, 999999)
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif (password1 != password2):
            flash('Passwords don\'t match.', category='error')
        else:
            new_user = User(fullName=full_name, username = username, email=email, emailauth=email_auth,
            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            #TODO: Redirect to email verificication (automate sending email to user with code and prompt user for code before activation)
            #Make
            return redirect(url_for('auth.verify_email'))
    return render_template("sign_up.html", )

@auth.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    if request.method == 'POST':
        email_auth = request.form.get('emailcode')

        user = User.query.filter_by(email=current_user.email).first()
        #123456 is a temporary bypass while debugging(will disable for final version
        if (user.emailauth != email_auth or email_auth == 123456):
            flash('Incorrect Verification Code.', category='error')
        else:
            setattr(user, emailauth, 0)
            db.session.commit()
            flash('Account verified!', category='success')
            #TODO: Redirect to email verificication (automate sending email to user with code and prompt user for code before activation)
            #Make
            return redirect(url_for('views.home'))
    return render_template("verify_email.html", )