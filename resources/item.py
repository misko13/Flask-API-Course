#import uuid
#from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt  # x User autentication 
from sqlalchemy.exc import SQLAlchemyError  # Exceptions used with SQLAlchemy.

from db import db
from models import ItemModel # __init__.py id important
from schemas import ItemSchema, ItemUpdateSchema
#from db import items

#----------------------------------------------------------------------------------------------

"""Blueprint Devides flask api in segments"""
blp = Blueprint("Items", __name__,  description="Operations on items")


#----------------------------------------------------------------------------------------------

@blp.route("/item/<int:item_id>")  #connect flask smorest with class Store bellow, so API runs the dinctions inside
class Item(MethodView): #class Store inherits from a methodView   
    """ITEM READ from db record --> db.session.add(item)""" 
    
    @jwt_required() # requests a token in header' Authetication -> Bearer'  with a token inside
    @blp.response(200, ItemSchema) # response deffinition  (includes dump_only and required from schema too into a response)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)   # Query.get but aborts with a 404 Not Found error instead of returning None. !! The primary key to query !!
        return item
    
    """ITEM DELETE from db record --> """  
    @jwt_required() # requests a token in header' Authetication -> Bearer'  with a token inside
    def delete(self, item_id):
        
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message=" Admin role is requested.")


        item = ItemModel.query.get_or_404(item_id) 
        db.session.delete(item)
        db.session.commit()
        #raise NotImplementedError("Delete not implemented")
        return {"message": "Item deleted"}

    """ITEM UPDATE in db record --> """  
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)  #respomse decorator must be AFTER arguments decorator
    def put(self, item_data , item_id ): # arguments decorator must be first after root (self)
        item = ItemModel.query.get(item_id) 
        if item:  # true if Item Exists we need to update only price and name
            item.price = item_data["price"]
            item.name = item_data["name"]
        else: #New item , also store Id mist be pass
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item

                
#----------------------------------------------------------------------------------------------

@blp.route("/item")  
class ItemList(MethodView): #class Store inherits from a methodView    
    """ITEM LIST ALL in db record --> """ 
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))  # after validation gives us a list sutible for return in function
    def get(self):
        #return("Hello word!")

        #return {"items": list(items.values())}  #for JSON we need to convert Dict to List , this is OBJECT {} of items
        return ItemModel.query.all()

    """ITEM CREATE record --> db.session.add(item)"""
    """@jwt_required(Fresh=True)  #A decorator to protect a Flask endpoint with JSON Web Tokens. Any route decorated with this will require a valid JWT """
    @jwt_required()
    @blp.arguments(ItemSchema)   #here we DECORATED the metod with ItemSchema defined in schemas.py  for data valadation
    @blp.response(201, ItemSchema)
    def post(self, item_data): #++ item_data  ++  will be passsed after validation from ItemSchema
        # OLD before database.. item_data = request.get_json()  # recived json converted in dictionary
        #    then item = { **item_data, "id": item_id  } will pass  coinstruct params for a new dict insert
      
        item = ItemModel(**item_data) #**store_data unpaks item_data Dictionary and saves into new dict .. passing to ItemModel
                                    
        try:
            db.session.add(item)
            db.session.commit() #writte to db occures
        except  SQLAlchemyError:
            abort(500, message="Error: Item not inserted!")


        return item  #status code