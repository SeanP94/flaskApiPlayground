from flask import request
from storerestapi import app
from storerestapi.models import stores


# Will be deleted later I think
@app.get('/store')
def get_stores():
    return stores

@app.post('/store')
def post_store():
    request_data = request.get_json()
    new_store = {"name" : request_data["name"], "items" : []}
    stores.append(new_store)
    return new_store, 201

@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {'name' : request_data['name'] , 'price' : request_data['price']}
            store['items'].append(new_item)
            return new_item, 201
    return {"message" : f"Could not find store {name}"}, 404

@app.get("/store/<string:name>/item")
def get_store_items(name):
    for store in stores:
         if store['name'] == name:
            return store['items'], 201
    return {"message" : f"Could not find store {name}"}, 404
         