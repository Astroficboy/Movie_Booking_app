from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Super
from . import db
from . import views
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

super_auth = Blueprint('super_auth', __name__)

@super_auth.route('/super_login', methods=['GET', 'POST'])
def login():
    super = Super.query.filter_by()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        super = Super.query.filter_by(email = email).first()
        if super:
            if password == super.password:
                flash('Logged in successfully!', category = 'success')
                login_user(super, remember = True)
                return redirect(url_for('admin_auth.sign_up', super_value=super))
            else:
                flash('Incorrect password.', category = 'error')
        else:
            flash('Email does not exists.', category = 'error')
    return render_template('super_login.html', super_value=super)


@super_auth.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('views.home'))