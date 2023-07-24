from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin, Super
from . import db
from . import views
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


admin_auth = Blueprint('admin_auth', __name__)


@admin_auth.route('/admin_login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        admin = Admin.query.filter_by(email = email).first()
        if admin:
            if check_password_hash(admin.password, password):
                flash('Logged in successfully!', category = 'success')
                login_user(admin, remember = True)
                return redirect(url_for('views.theaters'))
            else:
                flash('Incorrect password.', category = 'error')
        else:
            flash('Email does not exists.', category = 'error')
    return render_template('admin_login.html', admin = current_user)


@admin_auth.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('views.admin_login'))


@admin_auth.route('/admin_registration', methods=['GET', 'POST'])
def sign_up():
    admin = Admin.query.filter_by().first()
    super = Super.query.filter_by().first()
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if admin:
            flash('Email already exists.', category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category = 'error')
        elif len(first_name)<2:
            flash('First name must be greater than 2 characters.', category = 'error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category = 'error')
        elif len(password1) < 7:
            flash('Passeword must be at least 7 characters.', category = 'error')
        else: 
            new_admin = Admin(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method = 'sha256'))
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin, remember = True)
            flash('Account created.', category = 'success')
            return redirect(url_for('views'))

    return render_template('register_admin.html', admin = current_user, super_value=super)