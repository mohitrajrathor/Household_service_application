'''
models.py

This module contain all the models required for application.
'''

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class Admins(db.Model):
    '''Admin table'''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self) -> str:
        return f"<Admin {self.username}>"
    

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    street_address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zipcode = db.Column(db.String(6), nullable=True)
    is_active = db.Column(db.Boolean, default=True)  
    date_created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    
    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='customer', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Customer {self.name}>'


class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.String(100), nullable=True)  
    
    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)
    
    def to_dict(self):
        '''convert service object to dict format'''
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "time_required": self.time_required
        }

    def __repr__(self):
        return f'<Service {self.name}>'

    

class Professional(db.Model):
    __tablename__ = 'professionals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    
    # Professional Details
    description = db.Column(db.Text, nullable=True)
    service_type_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False) 
    experience = db.Column(db.Integer, nullable=True) 
    doc_path = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, default=False) 
    
    # Status Fields
    is_active = db.Column(db.Boolean, default=True)  

    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='professional', lazy=True)
    service = db.relationship('Service', backref='professionals')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Professional {self.name}>'



class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    
    # Request Details
    title = db.Column(db.String(255), nullable=False)
    time_of_request = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    date_of_completion = db.Column(db.DateTime, nullable=False)
    service_status = db.Column(db.String(20), default='requested')  # other values should be 'in_progress', 'completed', 'cancelled' or 'paid' 
    remarks = db.Column(db.Text, nullable=True)
    location_pin_code = db.Column(db.String(10), nullable=False)

    review = db.relationship('Reviews', backref='service_request', lazy=True)

    
    def __repr__(self):
        return f'<ServiceRequest {self.id} - {self.service_status}>'


class Reviews(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    prof_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    service_req_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.String(255), nullable=True)

    professional = db.relationship('Professional', backref='reviews', lazy=True)
    customer = db.relationship('Customer', backref='reviews', lazy=True)

    def __repr__(self):
        return f'{self.rating}'
    
    def get_rating(self):
        '''return rating'''
        return self.rating
    
    