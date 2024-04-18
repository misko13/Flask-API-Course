import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate



from db import db
from blocklist import BLOCKLIST
import models  #uses __init__.py, SQL Alchemy uses Models to know abaut tables to create

""" To organize code , we move all views from app.py into the corresponding Flask Blueprint."""
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.users import blp as UserBlueprint

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
    migrate = Migrate(app, db) #muste be after db 

    api = Api(app)

    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     # TODO: Read from a config file instead of hard-coding
    #     if identity == 1:
    #         return {"is_admin": True}
    #     return {"is_admin": False}

    app.config["JWT_SECRET_KEY"] = "168382049668195797030675850518160702137" #should be stored in environment var!! Not in code.
    #secrets.SystemRandom().getrandbits(128) -> Generates an int with k random bits -> this key will sign and check user JWT to prevent tampering
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Better will be to look in a database and seew if user is Admin
        if identity == 2:
            return {"is_admin": True}
        return {"is_admin": False}
    

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader  # for non fresh token
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # JWT configuration ends






    #@app.before_first_request
    """Since we will be using Flask-Migrate to create our database, we no longer need to tell Flask-SQLAlchemy to do it when we create the app."""
    # with app.app_context():
    #    db.create_all()  #creates all tables in database using defionition inside a models!

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    return app
