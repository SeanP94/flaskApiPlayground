import uuid 
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from storerestapi.models import stores
from storerestapi.schemas import StoresSchema

blp = Blueprint("stores", __name__, description="Operations for stores")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoresSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoresSchema)
    @blp.response(200, StoresSchema)
    def post(self, store_data):
        # Return if store exsits.
        for store in stores.values():
            if store_data['name'] == store['name']:
                abort(400, message="Bad request, Store already exists")
        # Creates new store.
        store_id = uuid.uuid4().hex # Creates a UUID unique key, will be done by Postgres later.
        new_store = {**store_data, "id" : store_id}
        stores[store_id] = new_store
        return new_store

@blp.route("/store/<string:store_id>")
class StoreGeneral(MethodView):
    @blp.response(200, StoresSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Could not find store.")


    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message" : "Store deleted."}, 201
        except KeyError:
            abort(404, message=f"Item id {store_id} not found.")
