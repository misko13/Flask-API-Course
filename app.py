import os

from flask import Flask
from flask_smorest import Api

from db import db
import models  #uses __init__.py, SQL Alchemy uses Models to know abaut tables to create

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

# it is bettere to deffine a function to crtate, setup, configure the flask app
def create_app(db_url=None): #argument is db we want to connect
    app = Flask(__name__)


    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASRE_URL", "sqlite:///data.db") # we use environment varioable to gai flexibility , secrets are NOT in code but in os
    #CONNECTION STRING FOIR A DB ,Postres will be the production db, Sqlite is development  db
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    

    api = Api(app)

    with app.app_context():
        db.create_all()  #creates all tables in database using defionition inside a models!

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    return app
