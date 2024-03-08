import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores

#----------------------------------------------------------------------------------------------

"""Blueprint Devides flask api in segments"""
blp = Blueprint("stores", __name__ , description="Operations on stores")

@blp.route("/store/<string:store_id>")  #connect flask smorest with class Store bellow, so API runs the dinctions inside
class Store(MethodView): #class Store inherits from a methodView
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found!") 
   
   
    def delete(self, store_id):
        try:
            del stores[store_id]
            return{ "message":"Store deleted!"}
        except KeyError:
            abort(404, message="Store not found!") # we use Abort function from flask_smorest ..



#----------------------------------------------------------------------------------------------
            
@blp.route("/store")  #connect flask smorest with class Store bellow, so API runs the dinctions inside
class StoreList(MethodView): #class Store inherits from a methodView
    def get(self):
        return {"stores":list(stores.values())} 
   
   
    def post(self):
        store_data = request.get_json()  # will convert JSON string data into a Python Dictionary
        # validate name is inside Json
        if "name" not in store_data:
            abort(
                400,  
                message="Bad request. Ensure  'name' is included inside a JSON payload. "
            )
        #validate store is not prsenet
        for store  in stores.values():
            if(
                store_data["name"] == store["name"]
                and store_data["store_id"] == store["store_id"]
            ):
                abort( 400, message=f"Item already exists "  )    

        store_id = uuid.uuid4().hex # generated string
        store = { **store_data, "id": store_id  } #**store_data unpaks stora data dict. and includ it inside a new dictionary
        stores[store_id] = store #insert a store (dictionary) inside a stores Dict in store_id 

        return store, 201  #status code
    
   