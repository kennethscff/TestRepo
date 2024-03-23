# matches.py
from flask import Blueprint, jsonify, request, render_template
from extensions import db
from sqlalchemy import text


matches = Blueprint('matches', __name__)

@matches.route('/about', methods=['GET'])
def about():
    return render_template('aboutus.html')

@matches.route('/search', methods=['GET'])
def search():
    print(request.args)
    return render_template('facets.html')

@matches.route('/direct_swap', methods=['GET'])
def get_direct_swap():
    tenant_id = request.args.get('id')
    if not tenant_id:
        return jsonify({'message': 'Tenant ID is required'}), 400

    sql = """
    SELECT 
      TenantA.name AS TenantA_Name,
      TenantB.name AS TenantB_Name,
      locationA.LocationName AS CurrentLocation_A,
      locationA_desired.LocationName AS DesiredLocation_A,
      locationB_current.LocationName AS CurrentLocation_B,
      locationB_desired.LocationName AS DesiredLocation_B
    FROM 
      tenant AS TenantA 
    INNER JOIN desiredLocation AS desiredLocationA ON TenantA.TenantID = desiredLocationA.TenantID
    INNER JOIN location AS locationA ON TenantA.TenantLocation = locationA.LocationID
    INNER JOIN location AS locationA_desired ON desiredLocationA.DesiredLocationID = locationA_desired.LocationID
    INNER JOIN tenant AS TenantB ON desiredLocationA.DesiredLocationID = TenantB.TenantLocation
    INNER JOIN location AS locationB_current ON TenantB.TenantLocation = locationB_current.LocationID
    INNER JOIN desiredLocation AS desiredLocationB ON TenantB.TenantID = desiredLocationB.TenantID
    INNER JOIN location AS locationB_desired ON desiredLocationB.DesiredLocationID = locationB_desired.LocationID
    WHERE 
      TenantA.TenantID = :tenant_id
      AND desiredLocationA.DesiredLocationID = TenantB.TenantLocation
      AND desiredLocationB.DesiredLocationID = TenantA.TenantLocation;
    """
    
    try:
        result = db.session.execute(text(sql), {'tenant_id': tenant_id})
        matches = [
            {
                "TenantB_Name": row['TenantB_Name'], 
                "DesiredLocation_B": row['DesiredLocation_B']
            } for row in result.mappings()
        ]
        return jsonify(matches), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@matches.route('/multipoint_swap', methods=['GET'])
def get_multipoint_swap():
    tenant_id = request.args.get('id')
    if not tenant_id:
        return jsonify({'message': 'Tenant ID is required'}), 400

    sql = """
    SELECT
  TenantA.name AS 'TenantA_Name',
  locationA.LocationName AS 'CurrentLocation_A',
  locationA_desired.LocationName AS 'DesiredLocation_A',
  
  TenantB.name AS 'TenantB_Name',
  locationB_current.LocationName AS 'CurrentLocation_B',
  locationB_desired.LocationName AS 'DesiredLocation_B',
  
  TenantC.name AS 'TenantC_Name',
  locationC_current.LocationName AS 'CurrentLocation_C',
  locationC_desired.LocationName AS 'DesiredLocation_C'
FROM
  tenant AS TenantA
INNER JOIN desiredLocation AS desiredLocationA ON TenantA.TenantID = desiredLocationA.TenantID
INNER JOIN location AS locationA ON TenantA.TenantLocation = locationA.LocationID
INNER JOIN location AS locationA_desired ON desiredLocationA.DesiredLocationID = locationA_desired.LocationID
  
INNER JOIN tenant AS TenantB ON desiredLocationA.DesiredLocationID = TenantB.TenantLocation
INNER JOIN location AS locationB_current ON TenantB.TenantLocation = locationB_current.LocationID
INNER JOIN desiredLocation AS desiredLocationB ON TenantB.TenantID = desiredLocationB.TenantID
INNER JOIN location AS locationB_desired ON desiredLocationB.DesiredLocationID = locationB_desired.LocationID
  
INNER JOIN tenant AS TenantC ON desiredLocationB.DesiredLocationID = TenantC.TenantLocation
INNER JOIN location AS locationC_current ON TenantC.TenantLocation = locationC_current.LocationID
INNER JOIN desiredLocation AS desiredLocationC ON TenantC.TenantID = desiredLocationC.TenantID
INNER JOIN location AS locationC_desired ON desiredLocationC.DesiredLocationID = locationC_desired.LocationID
WHERE
  desiredLocationA.DesiredLocationID = TenantB.TenantLocation
  AND desiredLocationB.DesiredLocationID = TenantC.TenantLocation
  AND desiredLocationC.DesiredLocationID = TenantA.TenantLocation;
    """
    
    try:
        result = db.session.execute(text(sql), {'tenant_id': tenant_id})
        matches = [
            {
                "TenantB_Name": row['TenantB_Name'], 
                "DesiredLocation_B": row['DesiredLocation_B']
            } for row in result.mappings()
        ]
        return jsonify(matches), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500