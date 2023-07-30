import uuid 
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from storerestapi.schemas import ItemSchema, ItemUpdateSchema

from models import items

blp = Blueprint("items", __name__, description="Operations for items")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        #return {"items" : list(items.values())}
        return items.values()
    
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # return if item exists
        for item in items.values():
            if item_data["name"] == item["name"] and item_data["store_id"] == item['store_id']:
                abort(400, message="Bad request, Item already exists.")

        # Create new item
        item_id = uuid.uuid4().hex
        new_item = {**item_data, "id" : item_id}
        items[item_id] = new_item
        return new_item


@blp.route("/item/<string:item_id>")
class ItemBasic(MethodView):
    blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Could not find item.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message" : "Item deleted."}, 201
        except KeyError:
            abort(404, message=f"Item id {item_id} not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id] # Get the item object
            item |= item_data # Combine the name and price into the item_id.
            return item
        except:
            abort(404, message=f"Item id {item_id} not found.")

