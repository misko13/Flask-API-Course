import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items, stores

#----------------------------------------------------------------------------------------------

"""Blueprint Devides flask api in segments"""
blp = Blueprint("Items", __name__,  description="Operations on items")


#----------------------------------------------------------------------------------------------

@blp.route("/item/<string:item_id>")  #connect flask smorest with class Store bellow, so API runs the dinctions inside
class Item(MethodView): #class Store inherits from a methodView    
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found!") # we use Abort function from flask_smorest ..i

   
    def delete(self, item_id):
        try:
            del items[item_id]
            return{ "message":"Item deleted!"}
        except KeyError:
            abort(404, message="Item not found!") # we use Abort function from flask_smorest ..

    def put(self, item_id):
        item_data = request.get_json()
        if(  "price" not in item_data or "name" not in item_data ):
            abort(  400,  message="Bad request. Ensure 'price'  and 'name' are included inside a JSON payload. "  )
        try:
            item = items[item_id]   # item here is a dictionary
            #   | operaror permos merge (replace corresponding data) on two distionaries
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found!")

                
#----------------------------------------------------------------------------------------------

@blp.route("/item")  
class ItemList(MethodView): #class Store inherits from a methodView    
    def get(self):
        #return("Hello word!")
        return {"items": list(items.values())}  #for JSON we need to convert Dict to List

        
    def post(self):
        item_data = request.get_json()  # recived json converted in dictionary then item = { **item_data, "id": item_id  } will pass  coinstruct params for a new dict ionsert
        # we need to validate if data exist and if the data is of right type
        if (
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data 
        ):
            abort(
                400,  
                message="Bad request. Ensure 'price' , 'store' and 'name' are included inside a JSON payload. "
            )
        
        #check if item is already present in same store
        for item in items.values():
            if(
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort( 400, message="Item already exists "  )

        #check if sore is present
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found!") # we use Abort function from flask_smorest ..i
    
        item_id = uuid.uuid4().hex # generated string
        item = { **item_data, "id": item_id  } #**store_data unpaks item_data Dictionary and saves into new dict. 
        items[item_id] = item #insert a item (dictionary) inside a items Dict having  store_id 
        return item, 201  #status code