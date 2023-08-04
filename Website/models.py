from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Enum, BLOB
import enum
import json

class BytesJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('latin-1')  # Decode using 'latin-1'
        return super().default(obj)

class Super(db.Model, UserMixin):
    __tablename__ = 'super'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    role = db.Column(db.String(150))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    role = db.Column(db.String(150))

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    role = db.Column(db.String(150))

class Bookings(db.Model):
    __tablename__='bookings'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    show_listing_id = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    number_of_seats = db.Column(db.Integer)
    total_amount = db.Column(db.Integer)

# class T(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey(User.id))
#     task_list_id = db.Column(db.Integer, db.ForeignKey(Task_list.id))
#     title = db.Column(db.String(200))
#     description = db.Column(db.String(1000))
#     status = db.Column(db.Enum(Task_status))
#     start_date = db.Column(db.DateTime(timezone=True), default=func.now())
#     end_date = db.Column(db.DateTime(timezone=True), default=func.now())
#     completed_on_date = db.Column(db.DateTime(timezone=True), default=func.now())

class Theaters(db.Model):
    __tablename__='theaters'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(500))
    capacity = db.Column(db.Integer)
    screens = db.Column(db.Integer)
    image = db.Column(db.BLOB)
    admin_id = db.Column(db.Integer, db.ForeignKey(Admin.id))
    total_business = db.Column(db.Integer)
    
class showListing(db.Model):
    __tablenane__='showlistings'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    show_name = db.Column(db.String(200))
    tags = db.Column(db.String(100))
    director = db.Column(db.String(100))
    price = db.Column(db.Integer)
    theater_name = db.Column(db.String)
    screen_no = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    number_of_bookings = db.Column(db.Integer)
    number_of_theaters = db.Column(db.Integer)
    image = db.Column(db.BLOB)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    no_seats = db.Column(db.Integer)
    def to_dict(self):
        data = {
            'id': self.id,
            'show_name': self.show_name,
            'tags':self.tags,
            'director': self.director,
            'rating': self.rating,
            'price': self.price,
            'theater_name': self.theater_name,
            'screen_no': self.screen_no,
            'number_of_bookings':self.number_of_bookings,
            'number_of_theaters':self.number_of_theaters,
            'image':self.image,
            'start_date':self.start_date,
            'end_date':self.end_date,
            'no_seats':self.no_seats
            
            # Add other fields as needed
        }
        return data



    

    
