from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from storerestapi.blueprints.item import blp as itemBlueprint
from storerestapi.blueprints.store import blp as storeBlueprint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"


# Help find errors
app.config["PROPAGATE_EXCEPTIONS"] = True

# Setup documentation for API
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

db = SQLAlchemy(app)
api = Api(app)

api.register_blueprint(storeBlueprint)
api.register_blueprint(itemBlueprint)