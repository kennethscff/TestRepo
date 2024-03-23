from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from swaggertools import resolve

from extensions import db
from home_management import home_management
from matches import matches
from user import users
from utils import utils
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.secret_key = os.urandom(24)

    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:kbcbhbjb@socialx.cubywqkqujxb.eu-west-2.rds.amazonaws.com/socialx'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'kqwowksckpoa-opvlspokvmas-qwokpfaskzpk-cakopqwppak' 

    jwt = JWTManager(app)
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
    app.register_blueprint(utils)

    @app.route('/')
    def hello_world():
        return render_template('index.html')
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.route('/api-docs') 
    def get_swagger_spec():
        with open('static/swagger/swagger.json') as file_handler:
            app = resolve(file_handler)
        return jsonify(app.to_dict())

    return app
