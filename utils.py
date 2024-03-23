from flask import Blueprint, request, jsonify, session, render_template
from flask_bcrypt import Bcrypt

from models import Typeahead

utils = Blueprint('utils', __name__)
bcrypt = Bcrypt()  

@utils.route('/typeahead', methods=["GET"])
def typeahead():
    search_term = request.args.get('term', '')  # "term" is the query parameter we expect to hold the search keyword
    if search_term:
        # Using the `ilike` function to perform a case-insensitive partial match
        # and limiting the results to 5
        typeahead_results = Typeahead.query.filter(Typeahead.label.ilike(f"{search_term}%")).limit(5).all()
        # Formatting results as a list of dictionaries to return as JSON
        results = [{'id': location.id, 'name': location.name1} for location in typeahead_results]
        return jsonify(results)
    return jsonify([])  # Return an empty list if no search term is provided

@utils.route('/facets', methods=['GET'])
def facets():
    requested_location = request.args['location']
    if not requested_location:
        requested_location = 'the UK'
    else:
        requested_location = requested_location.title()
    return render_template('facets.html', location = requested_location)

@utils.route('/search', methods=['GET'])
def search():
    return render_template('search_results.html')