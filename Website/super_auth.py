from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Super, Admin
from . import db
from flask_login import login_user, login_required, logout_user, current_user, fresh_login_required
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

super_auth = Blueprint('super_auth', __name__)




@super_auth.route('/super_login', methods=['GET', 'POST'])
def super_login():
    super_obj = Super.query.filter_by().first()
    admin_obj = Admin.query.first()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        email=email.strip()
        super_user = Super.query.filter(func.lower(Super.email) == email.lower()).first()
        if super_user:
            if check_password_hash(super_user.password, password):
                flash('Logged in successfully!', category = 'success')
                login_user(super_user)
                return redirect(url_for('super_auth.admin_registration'))
            flash('Incorrect password.', category = 'error')
        else:
            flash('Email does not exists.', category = 'error')
    return render_template('super_login.html', super_value=super_obj)


@super_auth.route('/super_logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('views.home'))


def super_get_role():
   try: 
        if current_user:
            if current_user.role == 'super':
                return 'super'
        else:
            return redirect(url_for('super_auth.super_login'))
   except AttributeError:
       return redirect(url_for('super_auth.super_login'))
    

@super_auth.route('/admin_registration', methods=['GET', 'POST'])
# @super_required
def admin_registration():
    admin = Admin.query.first()
    super_value = Super.query.first()
    role = super_get_role()
    if role == 'super':
        if request.method == 'POST':
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            email_check = Admin.query.filter(func.lower(Admin.email) == email.lower()).first()
            if email_check:
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
                new_admin = Admin(email=email.lower(), first_name=first_name.capitalize(), last_name=last_name.capitalize(), password=generate_password_hash(password1, method = 'sha256'), role='admin')
                db.session.add(new_admin)
                db.session.commit()
                login_user(new_admin)
                flash('Account created.', category = 'success')
                
                # return redirect(url_for('admin_auth.admin_dashboard'))
    else:
        return redirect(url_for('super_auth.super_login'))
    return render_template('register_admin.html', admin = current_user, super_value=super_value)