import os
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager 
from models import db

from storerestapi.blueprints.item import blp as itemBlueprint
from storerestapi.blueprints.store import blp as storeBlueprint
from storerestapi.blueprints.tag import blp as tagBlueprint


def create_app(db_url=None):
    '''Initial Builder application'''
    app = Flask(__name__)
    # Help find errors
    app.config["PROPAGATE_EXCEPTIONS"] = True

    # Setup documentation for API
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['JWT_SECTET_KEY'] = '18552217901512987768132793601622742024' # Change later. # Used to work with signing the data before its sent
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    with app.app_context():
        db.create_all()

    api.register_blueprint(storeBlueprint)
    api.register_blueprint(itemBlueprint)
    api.register_blueprint(tagBlueprint)
    return app