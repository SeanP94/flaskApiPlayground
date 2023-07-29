import uuid 
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from storerestapi.models import items

blp = Blueprint("items", __name__, description="Operations for items")

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        #return {"items" : list(items.values())}
        return items
    
    def post(self):
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


@blp.route("/item/<string:item_id>")
class ItemBasic(MethodView):
    def get(self, item_id):
        try:
            return items[item_id], 201
        except KeyError:
            abort(404, message="Could not find item.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message" : "Item deleted."}, 201
        except KeyError:
            abort(404, message=f"Item id {item_id} not found.")

    def put(self, item_id):
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

