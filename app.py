from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from swaggertools import resolve

from extensions import db
from home_management import home_management
from matches import matches
from user import users
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:faceb00k?@localhost/homes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger/swagger.json'
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={ 
            'app_name': "Social Swap" 
        }
    )

    
    db.init_app(app)   

    app.register_blueprint(home_management)
    app.register_blueprint(matches)
    app.register_blueprint(users)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    @app.route('/api-docs') 
    def get_swagger_spec():
        with open('static/swagger/swagger.json') as file_handler:
            app = resolve(file_handler)
        return jsonify(app.to_dict())

    return app
