from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin, Theaters
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db


admin_auth = Blueprint('admin_auth', __name__)

def get_role():
    admin = Admin.query.filter_by().first()
    for admin in admin:
        if current_user.name == admin.name:
            return 'admin'
        
        
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
                return redirect(url_for('admin_auth.admin_dashboard'))
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

@admin_auth.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    admin = Admin.query.filter_by(id=current_user.id).first()
    admin_theater = Theaters.query.filter_by(admin_id=admin.id).first()
    return render_template('admin_dashboard.html', admin=admin)

@admin_auth.route('/theater_management', methods=['GET','POST'])
def theater_management():
    admin = Admin.query.filter_by().first()
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        capacity = request.form.get('capacity')
        screens = request.form.get('screens')
        image = request.files['image']
        if Theaters.query.filter_by(name=name).first():
            flash('Theater already exists', category='error')
        else:
            image = image.read()
            new_theater = Theaters(name=name, address=address, capacity=capacity, screens=screens, image=image)
            db.session.add(new_theater)
            db.session.commit()
            flash('Theater added', category='success')
            return(redirect(url_for('admin_auth.admin_dashboard')))
    
    return render_template('theater_management.html', admin=admin, admin_id=admin.id)


@admin_auth.route('/summary', methods=['GET'])
def summary():
    admin = Admin.query.filter_by().first()
    #user = User.query.filter_by().first()
    return render_template('summary.html', admin=admin)