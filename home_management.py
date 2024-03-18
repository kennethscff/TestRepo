# home_management.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Tenant, Location, DesiredLocation  # Adjust this line based on your actual model locations

home_management = Blueprint('home_management', __name__)

@home_management.route('/tenant', methods=['POST'])
def create_tenant():
    # Extract data from request
    data = request.get_json()

    # Data validation
    if not data or 'name' not in data or 'TenantLocation' not in data or 'DesiredLocations' not in data:
        return jsonify({'message': 'Missing data for tenant creation'}), 400
    if not isinstance(data['DesiredLocations'], list) or len(data['DesiredLocations']) == 0:
        return jsonify({'message': 'DesiredLocations must be a non-empty list'}), 400

    # Create a new Tenant object
    new_tenant = Tenant(name=data['name'], TenantLocation=data['TenantLocation'])
    db.session.add(new_tenant)

    # Attempt to create DesiredLocation objects for each ID in the list
    for loc_id in data['DesiredLocations']:
        desired_location = DesiredLocation(TenantID=new_tenant.TenantID, DesiredLocationID=loc_id)
        db.session.add(desired_location)

    try:
        # Commit session to save Tenant and their DesiredLocations
        db.session.commit()
        return jsonify({'message': 'Tenant and desired locations created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create tenant and desired locations', 'error': str(e)}), 500
