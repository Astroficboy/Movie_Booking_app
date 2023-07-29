from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import Admin, Theaters, showListing
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import base64


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
        admin = Admin.query.filter_by(email = email.lower()).first()
        if admin:
            if check_password_hash(admin.password, password):
                flash('Logged in successfully!', category = 'success')
                login_user(admin)
                return redirect(url_for('admin_auth.admin_dashboard'))
            else:
                flash('Incorrect password.', category = 'error')
        else:
            flash('Email does not exists.', category = 'error')
    return render_template('admin_login.html', admin = current_user)


@admin_auth.route('/admin_logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('admin_auth.login'))

@admin_auth.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    admin = Admin.query.first()
    admin_theater = Theaters.query.filter_by(admin_id=admin.id).all()
    theater_image = Theaters.query.all()
    for theater in admin_theater:
        theater_image = base64.b64encode(theater.image).decode('utf-8')
    return render_template('admin_dashboard.html', admin=admin, admin_theater=admin_theater, theater_image=theater_image)


@admin_auth.route('/theater_management', methods=['GET','POST'])
def theater_management():
    print(current_user.email)
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
            new_theater = Theaters(name=name.capitalize(), address=address.capitalize(), capacity=capacity, screens=screens, image=image, admin_id=current_user.id)
            db.session.add(new_theater)
            db.session.commit()
            db.session.close()
            flash('Theater added', category='success')
            return(redirect(url_for('admin_auth.admin_dashboard')))
    theater = Theaters.query.filter_by().first()
    return render_template('theater_management.html', admin=admin, theater=theater)


@admin_auth.route('/delete_theater', methods=['POST', 'GET'])
def delete_theater():
    admin = Admin.query.filter_by(id=current_user.id).first()
    theater_name = request.args.get("theater_name")
    print(theater_name)
    theater = Theaters.query.filter_by(name=theater_name).first()
    print(theater)
    if request.method=='POST':
    # Get the theater from the database
        if theater:
            movies = showListing.query.filter_by(theater_name=theater_name).all()
            if movies:
                for movie in movies:
                    db.session.delete(movie)

        # Delete the theater
            db.session.delete(theater)
            db.session.commit()

        # Redirect to a page after deletion (e.g., the admin dashboard)
            return redirect(url_for('admin_auth.admin_dashboard'))
        flash('Theater not found', category='error')
        return redirect(url_for('admin_auth.admin_dashboard'))
    return render_template('delete_theater.html', admin=admin, theater=theater)

    # Delete the associated movies (if any)
   



@admin_auth.route('/add_movies', methods=['GET', 'POST'])
def add_movies():
    print(current_user.email)
    admin = Admin.query.filter_by().first()
    theater_obj = Theaters.query.filter_by(admin_id=admin.id)
    if admin.is_authenticated:
        admin = Admin.query.filter_by(id=admin.id).first()
        if request.method == 'POST':
            show_name = request.form.get('show_name')
            tags = request.form.get('tags')
            director = request.form.get('director')
            price = request.form.get('price')
            screen_no = request.form.get('screen_no')
            theater_name = request.form.get('theater_name').capitalize()
            theater = Theaters.query.filter_by(name=theater_name).first()
            if theater:
                image = request.files['image']
                image = image.read()
                new_movie = showListing(show_name=show_name.capitalize(), tags=tags, director=director.capitalize(), theater_name=theater_name.capitalize(),
                                        image=image, price=price, screen_no=screen_no)
                db.session.add(new_movie)
                flash('Movie added.', category='success')
                db.session.commit()
                db.session.close()
                return render_template('add_movies.html', admin=admin)
            flash('Theater does not exist.', category='error')
            return redirect(url_for('admin_auth.theater_management'))
    else:
        return redirect(url_for('admin_auth.admin_login'))
    return render_template('add_movies.html', admin=admin, theater=theater_obj)

@admin_auth.route('/summary', methods=['GET'])
def summary():
    admin = Admin.query.filter_by(email=current_user.email).first()
    theater_obj = Theaters.query.filter_by(admin_id=admin.id)
    if admin.is_authenticated:
        admin = Admin.query.filter_by(id=admin.id).first()
    else:
        return redirect(url_for('admin_auth.admin_login'))
    return render_template('summary.html', admin=admin)


# Route to return the edit form HTML for a specific theater
@admin_auth.route('/get_edit_form', methods=['GET', 'POST'])
def get_edit_form():
    admin = Admin.query.filter_by(email=current_user.email).first()
    theater_id = request.args.get("theater_id")
    theater = Theaters.query.get(theater_id)
    name = request.form.get('name')
    address = request.form.get('address')
    capacity = (request.form.get('capacity'))
    screens = (request.form.get('screens'))
    if theater:
        if name:
            theater.name = name
        if address:
            theater.address = address
        if capacity:
            theater.capacity = capacity
        if screens:
            theater.screens = screens
        db.session.commit()
        flash("Theater updated", category='success')
        return render_template('edit_form.html', theater=theater, admin=admin)
    
    return flash('Theater not found',category='error')
#    return render_template('edit_form.html', theater=theater, admin=admin)

# @admin_auth.route('/update_theater/<theater_id>', methods=['POST'])
# def update_theater(theater_id):
#     admin = Admin.query.filter_by(email=current_user.email).first()
#     theater = Theaters.query.get(theater_id)
#     if theater:
#         # Update theater details based on the form data submitted
#         name = request.form.get('name')
#         address = request.form.get('address')
#         capacity = int(request.form.get('capacity'))
#         screens = int(request.form.get('screens'))
#         update_theater = theater(name=name, address=address, capacity=capacity, screens=screens)
#         db.session.commit(update_theater)

#         # Return a success message or handle the update success
#         return jsonify({'message': 'Theater details updated successfully'})
#     else:
#         # Return an error message or handle the case when the theater is not found
#         return jsonify({'error': 'Theater not found'}, admin=admin)