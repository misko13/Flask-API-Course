import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError  # Exceptions used with SQLAlchemy.

from db import db
from models import StoreModel # __init__.py id important
from schemas import StoreSchema

#from db import stores

#----------------------------------------------------------------------------------------------

"""Blueprint Devides flask api in segments"""
blp = Blueprint("stores", __name__ , description="Operations on stores")


@blp.route("/store/<int:store_id>")  #connect flask smorest with class Store bellow, so API runs the dinctions inside
class Store(MethodView): #class Store inherits from a methodView
    
    """STORE READ from db record --> """   
    @blp.response(200, StoreSchema) #we serialize using store schema
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)   # Query.get but aborts with a 404 Not Found error instead of returning None. !! The primary key to query !!
        return store #returns object
   
    
    """STORE DELETE from db record --> """   
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit
        #raise NotImplementedError("Delete not implemented")
        return {"messasge": "strore deleted"}
    

#----------------------------------------------------------------------------------------------
            
@blp.route("/store")  #connect flask smorest with class Store bellow, so API runs the dinctions inside
class StoreList(MethodView): #class Store inherits from a methodView
    """STORE LIST ALL in db record --> """ 
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    

    """STORE CREATE record --> db.session.add(store)  """
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):  #store_data insert that is passed from Store_schema validator

        store = StoreModel(**store_data) #**store_data unpaks store_data Dictionary and saves into new dict .. passing to StoreModel
                                    
        try:
            db.session.add(store)
            db.session.commit() #writte to db occures
        except  IntegrityError: #rised if srore already exists
            abort(
                400,
                message="Error: Store esistente!"

            )
        except  SQLAlchemyError:
            abort(500, message="Error: Store not inserted!")
        
        return store  #status code
    
   