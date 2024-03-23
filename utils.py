from flask import Blueprint, request, jsonify, session, render_template
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
    requested_location = request.args['location']
    if requested_location:
        requested_location = requested_location.title()
    return render_template('facets.html', location = requested_location)

@utils.route('/search', methods=['GET'])
def search():
    # Gather facet data from request
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
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
            'match': 4,
            'image_url': './static/images/property/1.jpg'
        },
        {
            'title': 'Modern Apartment Downtown',
            'location': '123 Main St, Anytown, AT 12345',
            'price': '1200',
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': '850sqft',
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
