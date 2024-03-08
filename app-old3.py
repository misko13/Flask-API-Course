import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items,stores

"""The value of that new variable, Flask(__name__) , is a new object that inherits from the class Flask — 
meaning it gets all the attributes and methods built into that class, 
which we have imported. __name__ is a built-in variable in Python.
We create  Flask application instances by passing __name__ as the first argument to the Flask class."""
app = Flask(__name__)

"""----GET	Retrieve an existing resource.----"""

"""1)Get all stores"""
@app.get("/store")  #flask root  http://127.0.0.1:5000/store  returns JSON data ... this is a full url, /store is ending shorten name
def get_stores():
    return {"stores":list(stores.values())}         # store,values is json so we need to convert to a list
                                                    # the values() method of dict. returns a view object.  es: dict_values(['My store', 'Store 1', ..])
                                                    # The view object contains the values of the dictionary, as a list. List() converts to list!
                                                    #possible returnin value :
                                                    # {
                                                    #@   "stores": [
                                                    #        {
                                                    #            "id": "1aa913fd1d884acf8500fe8fdbc7060b",
                                                    #            "name": "My store 3"
                                                    #        }
                                                    #    ]
                                                    # }
    

""" ---- POST	Create a new resource. ----"""

"""2)insert a new store"""
@app.post("/store")   #  http://127.0.0.1:5000/store  and JSON we send is {"name":"My store 3"}
def create_store():
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

"""3) insert item in a store"""
@app.post("/item")  #data inside a URL segment
def create_item(): # 
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

"""4) get all items"""
@app.get("/item")  
def get_items():
    #return("Hello word!")
    return {"items": list(items.values())}  #for JSON we need to convert Dict to List


"""5) get a specific store by id"""         # http://127.0.0.1:5000/store/1aa913fd1d884acf8500fe8fdbc7060b
@app.get("/store/<string:store_id>")  #data inside a URL segment
def get_store(store_id): # <--  name is from URL
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found!") # we use Abort function from flask_smorest ..if return before not runs, we run this

"""6) get item from a store by id"""
@app.get("/item/<string:item_id>")  #data inside a URL segment !!
def get_item(item_id): # <--  name is from URL
    try:
        return items[item_id]
    except KeyError:
         abort(404, message="Item not found!") # we use Abort function from flask_smorest ..i

"""7) delete item from a store by id"""
@app.delete("/item/<string:item_id>")  #data inside a URL segment !!
def delete_item(item_id): # <--  name is from URL
    try:
        del items[item_id]
        return{ "message":"Item deleted!"}
    except KeyError:
         abort(404, message="Item not found!") # we use Abort function from flask_smorest ..

"""8) Updatate Item"""
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if (  "price" not in item_data or "name" not in item_data ):
        abort(  400,  message="Bad request. Ensure 'price'  and 'name' are included inside a JSON payload. "  )
    try:
        item = items[item_id]   # item here is a dictionary
        #   | operaror permos merge (replace corresponding data) on two distionaries
        item |= item_data
        return item
    except KeyError:
           abort(404, message="Item not found!")

"""9) delete store  by id"""
@app.delete("/store/<string:store_id>")  #data inside a URL segment !!
def delete_store(store_id): # <--  name is from URL
    try:
        del stores[store_id]
        return{ "message":"Store deleted!"}
    except KeyError:
         abort(404, message="Store not found!") # we use Abort function from flask_smorest ..


