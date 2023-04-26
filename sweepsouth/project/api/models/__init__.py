from project import  db
from itsdangerous import  TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from sqlalchemy import ForeignKeyConstraint,ForeignKey,UniqueConstraint
import json
from werkzeug.security import generate_password_hash, check_password_hash


class Client(db.Model):
    __tablename__ = 'Client'

    id = db.Column(db.Integer,primary_key=True)
    first_name  = db.Column(db.String)	
    second_name = db.Column(db.String)
    uuid = db.Column(db.String(60), nullable=False)
    gender=db.Column(db.String)
    Date_birth=db.Column(db.DateTime)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    email = db.Column(db.String,unique=True)#unique
    number = db.Column(db.String)
    idcard=db.Column(db.String)
    passport=db.Column(db.String)
    password = db.Column(db.String(60))
    visibility =db.Column(db.Boolean,default=True)
    
    
    def __repr__(self):
        return '<Client %r>' %self.id
    
    def passwordhash(self, password_taken):
        self.password = generate_password_hash(password_taken)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Services(db.Model):
    __tablename__ = 'Services'

    id = db.Column(db.Integer,primary_key=True)
    service  = db.Column(db.String)	
    N_bed = db.Column(db.String)
    N_bath=db.Column(db.String)
    location=db.Column(db.String)
    prices=db.Column(db.String)
    duration=db.Column(db.String)
    visibility =db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Services %r>' %self.id

class Worker(db.Model):
    __tablename__ = 'Worker'

    id = db.Column(db.Integer,primary_key=True)
    first_name  = db.Column(db.String)	
    second_name = db.Column(db.String)
    uuid = db.Column(db.String(60), nullable=False)
    gender=db.Column(db.String)
    Date_birth=db.Column(db.DateTime)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    email = db.Column(db.String,unique=True)#unique
    number = db.Column(db.String)
    idcard=db.Column(db.String)
    passport=db.Column(db.String)
    password = db.Column(db.String(60))
    visibility =db.Column(db.Boolean,default=True)
    
    
    def __repr__(self):
        return '<Worker %r>' %self.id


    def passwordhash(self, password_taken):
        self.password = generate_password_hash(password_taken)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class Extras(db.Model):
    __tablename__ = 'Extras'

    id = db.Column(db.Integer,primary_key=True)
    service_id=db.Column(db.Integer, ForeignKey('Services.id'))
    extra_name=db.Column(db.String)
    extra_name=db.Column(db.String)
    prices=db.Column(db.String)
    visibility =db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Extras %r>' %self.id

class Comment(db.Model):
   __tablename__ = 'Comment'

   id = db.Column(db.Integer,primary_key=True)
   client_id=db.Column(db.Integer, ForeignKey('Client.id'))
   worker_id=db.Column(db.Integer, ForeignKey('Worker.id'))
   comment=db.Column(db.String)
   date=db.Column(db.DateTime(),default=datetime.utcnow)
   visibility =db.Column(db.Boolean,default=True)
   

   def __repr__(self):
        return '<Comment %r>' %self.id


class Location(db.Model):
   __tablename__ = 'Location'

   id = db.Column(db.Integer,primary_key=True)
   location=db.Column(db.String)
   visibility =db.Column(db.Boolean,default=True)

   def __repr__(self):
        return '<Location %r>' %self.id


class W_location(db.Model):
   __tablename__ = 'W_location'

   id = db.Column(db.Integer,primary_key=True)
   location_id=db.Column(db.Integer, ForeignKey('Location.id'))
   worker_id=db.Column(db.Integer, ForeignKey('Worker.id'))
   visibility =db.Column(db.Boolean,default=True)

   def __repr__(self):
        return '<W_location %r>' %self.id


class p_location(db.Model):
   __tablename__ = 'p_location'

   id = db.Column(db.Integer,primary_key=True)
   client_id=db.Column(db.Integer, ForeignKey('Client.id'))
   location=db.Column(db.String)
   Type=db.Column(db.String)
   visibility =db.Column(db.Boolean,default=True)


   def __repr__(self):
        return '<p_location %r>' %self.id


class Booking(db.Model):
   __tablename__ = 'Booking'

   id = db.Column(db.Integer,primary_key=True)
   service_id=db.Column(db.Integer, ForeignKey('Services.id'))
   extras_id=db.Column(db.Integer, ForeignKey('Extras.id'))
   location_id=db.Column(db.Integer, ForeignKey('Location.id'))
   worker_id=db.Column(db.Integer, ForeignKey('Worker.id'))
   client_id=db.Column(db.Integer, ForeignKey('Client.id'))
   once=db.Column(db.Boolean,default=True)
   frequency=db.column(db.String)
   validate=db.column(db.String)
   discount=db.column(db.String)
   date_time=db.Column(db.DateTime(),default=datetime.utcnow)
   status=db.Column(db.Boolean,default=True)
   visibility =db.Column(db.Boolean,default=True)


   def __repr__(self):
        return '<Booking %r>' %self.id


class receipt(db.Model):
    __tablename__ = 'receipt'

    id = db.Column(db.Integer,primary_key=True)
    receipt_no_=db.column(db.String)
    Booking_id=db.Column(db.Integer, ForeignKey('Booking.id'))
    visibility =db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<receipt %r>' %self.id