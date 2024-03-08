from flask import Flask, request

app = Flask(__name__)

#stores = []

stores = [
     {
        "name":"My Store",
        "items":
        [
            {
                "name":"iphone 13",
                "price": 1200
            },
            {
                "name":"iphone 14",
                "price": 1400
            }
        ]
    }
   
]


@app.get("/store")  #flask root  http://127.0.0.1:5000/store  returns JSON data
def get_stores():
    return {"stores":stores}

@app.post("/store")
def create_store():
    request_data = request.get_json()  # will convert JSON string darta into a Python Dictionary
    new_store = {"name":request_data["name"], "items":[]}
    stores.append(new_store)
    return new_store, 201  #status code

@app.post("/store/<string:name>/item")  #data inside a URL segment
def create_item(name): # <--  name is from URL
    request_data = request.get_json()  
    #find a matching name in our list
    for store in stores:
        if store["name"] == name: # <-- name from url
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store Not Foud"}, 404 # if return before not runs, we run this
           
@app.get("/store/<string:name>")  #data inside a URL segment
def get_store(name): # <--  name is from URL
    #find a matching name in our list
    for store in stores:
        if store["name"] == name: # <-- name from url
            return store
    return {"message": "Store Not Foud"}, 404 # if return before not runs, we run this

@app.get("/store/<string:name>/item")  #data inside a URL segment
def get_item_in_store(name): # <--  name is from URL
    #find a matching name in our list
    for store in stores:
        if store["name"] == name: # <-- name from url
            return {"items":store["items"]}
    return {"message": "Store Not Foud"}, 404 # if return before not runs, we run this
