import uuid
from flask import Flask, request
from db import items,stores

"""The value of that new variable, Flask(__name__) , is a new object that inherits from the class Flask — 
meaning it gets all the attributes and methods built into that class, 
which we have imported. __name__ is a built-in variable in Python.
We create  Flask application instances by passing __name__ as the first argument to the Flask class."""
app = Flask(__name__)

"""----GET	Retrieve an existing resource.----"""

"""Get all stores"""
@app.get("/store")  #flask root  http://127.0.0.1:5000/store  returns JSON data ... this is a full url, /store is ending shorten name
def get_stores():
    return {"stores":list(stores.values())}         # store,values is json so we need to convert to a list
                                                    # the values() method of dict. returns a view object.  es: dict_values(['My store', 'Store 1', ..])
                                                    # The view object contains the values of the dictionary, as a list. List() converts to list!

""" ---- POST	Create a new resource. ----"""

"""insert a new store"""
@app.post("/store")
def create_store():
    store_data = request.get_json()  # will convert JSON string data into a Python Dictionary
    store_id = uuid.uuid4().hex # generated string
    store = { **store_data, "id": store_id  } #**store_data unpaks stora data dict. and includ it inside a new dictionary
    stores[store_id] = store #insert a store (dictionary) inside a stores Dict in store_id 

    return store, 201  #status code

"""insert item in a store"""
@app.post("/item")  #data inside a URL segment
def create_item(): # <--  name is from URL
    item_data = request.get_json()  # recived json converted in dictionary then item = { **item_data, "id": item_id  } will pass  coinstruct params for a new dict ionsert
    if item_data["store_id"] not in stores:
        return {"message":  "Store not found"}, 404
   
    item_id = uuid.uuid4().hex # generated string
    item = { **item_data, "id": item_id  } #**store_data unpaks item_data Dictionary and saves into new dict. 
    return item, 201  #status code

"""get all items"""
@app.get("/item")  
def get_all_items():
    return {"items": list(items.values())}  #for JSON we need to convert Dict to List

"""get a specific store by id"""           
@app.get("/store/<string:store_id>")  #data inside a URL segment
def get_store(store_id): # <--  name is from URL
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store Not Foud"}, 404 # if return before not runs, we run this

"""get item from a store by id"""
@app.get("/item/<string:item_id>")  #data inside a URL segment !!
def get_item(item_id): # <--  name is from URL
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item Not Foud"}, 404 # if return before not runs, we run this
