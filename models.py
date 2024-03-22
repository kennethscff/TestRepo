# models.py
from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Typeahead(db.Model):
    __tablename__ = 'typeahead'
    id = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.String(50))
    lat = db.Column(db.Numeric(10, 7))
    lng = db.Column(db.Numeric(10, 7))
    label = db.Column(db.String(50))
    local_type_id = db.Column(db.Integer)
    county_unitary_id = db.Column(db.Integer)
    slug = db.Column(db.String(50))
    redirect_slug = db.Column(db.String(50))
    region = db.Column(db.Integer)
    country = db.Column(db.Integer)

class Tenant(db.Model):
    __tablename__ = 'tenant'
    TenantID = db.Column(db.Integer, primary_key=True)
    TenantLocation = db.Column(db.Integer, db.ForeignKey('location.LocationID'), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    # Relationship for desired locations
    desired_locations = db.relationship('DesiredLocation', backref='tenant', lazy=True)

class Location(db.Model):
    __tablename__ = 'location'
    LocationID = db.Column(db.Integer, primary_key=True)
    LocationName = db.Column(db.String(50), nullable=False)

    # Relationship (one Location to many Tenants)
    tenants = db.relationship('Tenant', backref='location', lazy=True)

class DesiredLocation(db.Model):
    __tablename__ = 'desiredLocation'
    id = db.Column(db.Integer, primary_key=True)
    TenantID = db.Column(db.Integer, db.ForeignKey('tenant.TenantID'), nullable=False)
    DesiredLocationID = db.Column(db.Integer, db.ForeignKey('location.LocationID'), nullable=False)

class Resident(db.Model):
    __tablename__ = 'resident'
    resident_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    # ... other fields you'd like to store

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
