from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, Response
from .models import Admin, Theaters, showListing, User, Bookings
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import base64
import weasyprint


admin_auth = Blueprint('admin_auth', __name__)

def admin_get_role():
   try: 
        if current_user:
            if current_user.role == 'admin':
                return 'admin'
        else:
            return redirect(url_for('admin_auth.login'))
   except AttributeError:
       return redirect(url_for('admin_auth.login'))
        
        
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
                return redirect(url_for('admin_auth.admin_dashboard', admin_id=admin.id))
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
    admin_id = request.args.get("admin_id")
    admin = Admin.query.filter_by(id=admin_id).first()
    admin_theater = Theaters.query.filter_by(admin_id=admin_id).all()
    movies = []
    total_business=[]
    for theater in admin_theater:
        movies.append(showListing.query.filter_by(theater_name=theater.name).first())
        total_business.append(theater.total_business)
    bookings = []
    for movie in movies:
        bookings.append(Bookings.query.filter_by(show_listing_id=movie.id).first())
    theater_image = Theaters.query.all()
    for theater in admin_theater:
        theater_image = base64.b64encode(theater.image).decode('utf-8')
    return render_template('admin_dashboard.html', admin=admin, admin_theater=admin_theater, theater_image=theater_image, 
                           admin_id=admin_id, movies=movies, bookings=bookings, total_business=total_business)


@admin_auth.route('/theater_management', methods=['GET','POST'])
def theater_management():
    admin = Admin.query.filter_by().first()
    admin_id = request.args.get('admin_id')
    # if current_user:
    #     if admin_get_role() == 'admin':
    #         return redirect(url_for('admin_auth.theater_management'))
    #     else:
    #         return redirect(url_for('admin_auth.login'))
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
            return redirect(url_for('admin_auth.admin_dashboard', admin_id=admin_id))
    theater = Theaters.query.filter_by().first()
    return render_template('theater_management.html', admin=admin, theater=theater, admin_id=admin_id)


@admin_auth.route('/delete_theater', methods=['POST', 'GET'])
def delete_theater():
    admin = Admin.query.filter_by(id=current_user.id).first()
    admin_id = request.args.get('admin_id')
    theater_name = request.args.get("theater_name")
    theater = Theaters.query.filter_by(name=theater_name).first()
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
            return redirect(url_for('admin_auth.admin_dashboard', admin_id=admin.id))
        flash('Theater not found', category='error')
        return redirect(url_for('admin_auth.admin_dashboard', admin_id=admin.id))
    return render_template('delete_theater.html', admin=admin, theater=theater, admin_id=admin_id)


@admin_auth.route('admin_movies', methods=['GET', 'POST'])
def admin_movies():
    user=User.query.first()
    admin_id = request.args.get('admin_id')
    theater_name = request.args.get('theater_name')
    admin=Admin.query.filter_by(id=admin_id).first()
    theater = Theaters.query.filter_by(admin_id=admin_id).first()
    movies = showListing.query.filter_by(theater_name=theater.name).all()
    return render_template('admin_movies.html', admin=admin, movies=movies, theater=theater, theater_name=theater_name)


@admin_auth.route('/add_movies', methods=['GET', 'POST'])
def add_movies():
    admin = Admin.query.filter_by(id = current_user.id).first()
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
            total_seats = request.form.get('total_seats')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            theater = Theaters.query.filter_by(name=theater_name).first()
            if theater:
                image = request.files['image']
                image = image.read()
                new_movie = showListing(show_name=show_name.capitalize(), tags=tags, director=director.capitalize(), theater_name=theater_name.capitalize(),
                                        image=image, price=price, screen_no=screen_no, total_seats=total_seats, start_date=start_date, end_date=end_date)
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


@admin_auth.route('/edit_movie', methods=['POST', 'GET'])
def edit_movie():
    # admin = Admin.query.filter_by(id=current_user.id).first()
    movie_id = request.args.get('movie_id')
    movie = showListing.query.filter_by(id=movie_id).first()
    admin = Admin.query.filter_by(email=current_user.email).first()
    # theater_id = request.args.get("theater_id")
    # theater = Theaters.query.get(theater_id)
    # movie = showListing.query.filter_by(theater_name=theater.name).first()
    movie_name = request.form.get('movie_name')
    tags = request.form.get('tags')
    director = (request.form.get('director'))
    price = (request.form.get('screens'))
    theater_name = (request.form.get('theater_name'))
    screen_no = (request.form.get('screen_no'))
    if request.method=='POST':
        if movie:
            if movie_name:
                movie.show_name = movie_name
            if tags:
                movie.tags=tags
            if director:
                movie.director=director
            if price:
                movie.price=price
            if theater_name:
                movie.theater_name = theater_name
            if screen_no:
                movie.screen_no=screen_no
        
        
            db.session.commit()
            return redirect(url_for('views.home'))
        flash('Movie not found', category='error')
        return redirect(url_for('admin_auth.admin_dashboard'))
    return render_template('edit_movie.html', admin=admin, movie=movie)


@admin_auth.route('/delete_movie', methods=['POST', 'GET'])
def delete_movie():
    admin = Admin.query.filter_by(id=current_user.id).first()
    movie_id = request.args.get('movie_id')
    movie = showListing.query.filter_by(id=movie_id).first()
    if request.method=='POST':
    # Get the theater from the database
        if movie:
            db.session.delete(movie)
            db.session.commit()
        # Redirect to a page after deletion (e.g., the admin dashboard)
            return redirect(url_for('views.home'))
        flash('Movie not found', category='error')
        return redirect(url_for('admin_auth.admin_dashboard'))
    return render_template('delete_movie.html', admin=admin, movie=movie)


@admin_auth.route('/summary', methods=['GET'])
def summary():
    admin_id = request.args.get('admin_id')
    admin = Admin.query.filter_by(id=admin_id).first()
    theaters = Theaters.query.filter_by(admin_id=admin_id).all()
    
    movies = []
    for theater in theaters:
        movies.append(showListing.query.filter_by(theater_name=theater.name).first())
        
    business_from_each_movie = {}
    for movie in movies:
        business = movie.price * movie.number_of_bookings
        business_from_each_movie[movie.show_name] = business_from_each_movie.get(movie.show_name, 0) + business
    print(business_from_each_movie)
    
    highest_sale = 0
    movie_name = ''
    for movie_name, sale in business_from_each_movie.items():
        if sale > highest_sale:
            highest_sale = sale
            movie_name = movie_name
    
    if admin.is_authenticated:
        admin = Admin.query.filter_by(id=admin.id).first()
    else:
        return redirect(url_for('admin_auth.admin_login'))
    return render_template('summary.html', admin_id=admin_id, admin=admin, theaters=theaters, movies=movies,
                           business_from_each_movie=business_from_each_movie, highest_sale=highest_sale, movie_name=movie_name)
    
    
@admin_auth.route('/report', methods=['GET', 'POST'])
def report():
    admin_id = request.args.get('admin_id')
    admin = Admin.query.filter_by(id=admin_id).first()
    theaters = Theaters.query.filter_by(admin_id=admin_id).all()
    movies = []
    for theater in theaters:
        movies.append(showListing.query.filter_by(theater_name=theater.name).first())
        
    html_content = render_template('report.html', admin=admin, admin_id=admin_id, theaters=theaters, movies=movies)
    # html_template_url = "F:\Pranav project\from scratch\Website\templates\report.html"

    report_html = weasyprint.HTML(string=html_content)

    # Generate the PDF in memory
    pdf_bytes = report_html.write_pdf(target=None)

    # Specify the filename for the PDF (if needed)
    pdf_filename = 'report.pdf'

    # Return the PDF as a response with appropriate headers for PDF content
    response = Response(pdf_bytes, content_type='application/pdf')
    response.headers['Content-Disposition'] = f'inline; filename="{pdf_filename}"'
    return response

        


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
