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
    return render_template('facets.html')