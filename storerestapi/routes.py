from flask import request
from flask_smorest import abort
from storerestapi import app
from storerestapi.models import stores, items
import uuid


# GETs

@app.get('/store')
def get_stores():
    return {"stores" : list(stores.values())}

@app.get('/item')
def get_all_items():
    return {"items" : list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 201
    except KeyError:
        abort(404, message="Could not find item.")
    
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 201
    except KeyError:
        abort(404, message="Could not find store.")

## POSTs

@app.post('/store')
def create_store():
    store_data = request.get_json()
    
    # return if JSON is incomplete
    if "name" not in store_data:
        abort(400, message="Bad request. name is not in JSON payload.")
    # Return if store exsits.
    for store in stores.values():
        if store_data['name'] == store['name']:
            abort(400, message="Bad request, Store already exists")
    # Creates new store.
    store_id = uuid.uuid4().hex # Creates a UUID unique key, will be done by Postgres later.
    new_store = {**store_data, "id" : store_id}
    stores[store_id] = new_store
    return new_store, 201

@app.post("/store/item")
def create_item():
    item_data = request.get_json()
    # Return now if data is incomplete.
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(400, message="Bad request, make sure you include price, store_id and name in JSON payload.")
    # return if item exists
    for item in items.values():
        if item_data["name"] == item["name"] and item_data["store_id"] == item['store_id']:
            abort(400, message="Bad request, Item already exists.")

    # Create new item
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id" : item_id}
    items[item_id] = new_item
    return new_item, 201


# UPDATES

@app.put('/item/<string:item_id>')
def update_item(item_id):
    item_data = request.get_json()
    
    # Make sure name and price are the only 2 keys.
    if 'name' not in item_data or 'price' not in item_data and len(item_data) == 2:
        abort(400, "Bad request, name and price are not in the item data.")
    try:
        item = items[item_id] # Get the item object
        item |= item_data # Combine the name and price into the item_id.
        return item, 201
    except:
        abort(404, message=f"Item id {item_id} not found.")

# DELETES
@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message" : "Item deleted."}, 201
    except KeyError:
        abort(404, message=f"Item id {item_id} not found.")


@app.delete('/item/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message" : "Store deleted."}, 201
    except KeyError:
        abort(404, message=f"Item id {store_id} not found.")