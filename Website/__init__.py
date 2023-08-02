from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv
from flask_login import LoginManager, login_user
from werkzeug.security import generate_password_hash
from Website import workers


db = SQLAlchemy()
DB_NAME = "database.db"

celery=None

def create_default_user():
    from .models import Super
    super_user = Super.query.filter_by(name='super').first()
    if not super_user:
        super_user = Super(name='super', email='super@movies.com', password=generate_password_hash('super123', method='sha256'), role='super')
        db.session.add(super_user)
        db.session.commit()
        

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'iitm'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin_auth import admin_auth
    from .super_auth import super_auth


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin_auth, url_prefix='/')
    app.register_blueprint(super_auth, url_prefix='/')


    from .models import User, Theaters, Bookings, showListing, Admin, Super

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id) or Super.query.get(id) or Admin.query.get(id)
    return app, celery

    

def create_database(app):
    if not path.exists('website/instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
    else:
        print('Database already exists.')
        





