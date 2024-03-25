# models.py
from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    os_id = db.Column(db.String(50))
    name1 = db.Column(db.String(50))
    name1_lang = db.Column(db.String(10))
    name2 = db.Column(db.String(50))
    name2_lang = db.Column(db.String(10))
    lat = db.Column(db.Numeric(10, 7))
    lon = db.Column(db.Numeric(10, 7))
    label = db.Column(db.String(50))
    local_type_id = db.Column(db.Integer)
    county_unitary_id = db.Column(db.Integer)
    region_id = db.Column(db.Integer)
    country_id = db.Column(db.Integer)
    slug = db.Column(db.String(50))
    redirect_slug = db.Column(db.String(50))
    
class Tenant(db.Model):
    __tablename__ = 'tenant'
    TenantID = db.Column(db.Integer, primary_key=True)
    TenantLocation = db.Column(db.Integer, db.ForeignKey('location.LocationID'), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    # Relationship for desired locations
    desired_locations = db.relationship('DesiredLocation', backref='tenant', lazy=True)
class DesiredLocation(db.Model):
    __tablename__ = 'desiredLocation'
    id = db.Column(db.Integer, primary_key=True)
    TenantID = db.Column(db.Integer, db.ForeignKey('tenant.TenantID'), nullable=False)
    DesiredLocationID = db.Column(db.Integer, db.ForeignKey('location.LocationID'), nullable=False)

class Resident(db.Model):
    __tablename__ = 'resident'
    resident_id = db.Column(db.Integer, primary_key=True)
    resident_location_id = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    address_id = db.Column(db.Integer, nullable=True, default=0)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
