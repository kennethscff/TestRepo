from flask import Blueprint, request, jsonify, session, render_template, abort
from flask_bcrypt import Bcrypt
from math import ceil

from models import Location

utils = Blueprint('utils', __name__)
bcrypt = Bcrypt()  

@utils.route('/typeahead', methods=["GET"])
def typeahead():
    search_term = request.args.get('term', '')  # "term" is the query parameter we expect to hold the search keyword
    if search_term:
        # Using the `ilike` function to perform a case-insensitive partial match
        # and limiting the results to 5
        typeahead_results = Location.query.filter(Location.label.ilike(f"{search_term}%")).limit(5).all()
        # Formatting results as a list of dictionaries to return as JSON
        results = [{'id': location.id, 'name': location.name1} for location in typeahead_results]
        return jsonify(results)
    return jsonify([])  # Return an empty list if no search term is provided

@utils.route('/facets', methods=['GET'])
def facets():
    facet_data = {
        'location': request.args.get('location', ''),
        'current_location': request.args.get('currentLocation', ''),
        'parking': request.args.get('parking', ''),
        'garden': request.args.get('garden', ''),
        'accessible': request.args.get('accessible', ''),
        'min_bedroom': request.args.get('min_bedroom', ''),
        'max_price': request.args.get('max_price', ''),
        'category': request.args.get('category', '')
    }
    return render_template('facets.html', facet_data = facet_data)

@utils.route('/search', methods=['GET'])
def search():
    facet_data = {
        'location': request.args.get('location', ''),
        'current_location': request.args.get('currentLocation', ''),
        'parking': request.args.get('parking', ''),
        'garden': request.args.get('garden', ''),
        'accessible': request.args.get('accessible', ''),
        'min_bedroom': request.args.get('min_bedroom', ''),
        'max_price': request.args.get('max_price', ''),
        'category': request.args.get('category', '')
    }

    # Dummy data for results
    results = [
        {
            'id': 1,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'id': 2,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'id': 3,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'id': 4,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'id': 5,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'id': 6,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'id': 7,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'id': 8,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'id': 9,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'id': 10,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'id': 11,
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
    ]

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page
    total_results = len(results)  # Total number of results available
    total_pages = ceil(total_results / per_page)  # Calculate total number of pages

    # Calculate start and end indices for the current page
    start = (page - 1) * per_page
    end = start + per_page

    # Slice the results array to get only the items for the current page
    page_results = results[start:end]

    # Maintain original query parameters for pagination links
    query_params = request.args.to_dict()
    query_params.pop('page', None)  # Remove the page parameter if present

    # Render the template, passing the necessary data
    return render_template('search_results.html', facet_data=facet_data, results=page_results, current_page=page, total_pages=total_pages, query_params=query_params)

@utils.route('/property/<property_id>', methods=['GET'])
def get_property(property_id):
    if not property_id:
        abort(404, 'Page not found')

    #dummy data
    data = {
            'id': 11,
            'location': '123 Main St, Anytown, AT 12345',
            'bedrooms': 2,
            'bathrooms': 2,
            'match': 4,
            'image_url': '../static/images/property/1.jpg',
            'landlord': 'Gorbals Housing Association',
            'last_active': '16',
            'parking': 'Yes',
            'garden': 'Shared',
            'price': '450',
            'description': "This spacious tenement flat in Glasgow's vibrant West End boasts classic charm and modern convenience. High ceilings and original features create an airy feel, while the updated kitchen and bathroom offer a touch of contemporary style.<br><br>Two generously sized bedrooms provide comfortable living space, ideal for sharing or a small family. The added bonus of a designated parking space takes the stress out of city living - a true rarity within Glasgow's bustling streets.<br><br>Imagine strolling to nearby cafes and independent shops on Byres Road, or enjoying a picnic in Kelvingrove Park. This tenement offers the best of both worlds:  city living with the ease of parking and access to green spaces."
        }
    return render_template('property.html', data=data)

@utils.route('/swap', methods=['GET'])
def swap_property():
    return render_template('swap_your_home.html')