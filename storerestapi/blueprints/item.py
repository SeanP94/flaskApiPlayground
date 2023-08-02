from flask.views import MethodView
from flask_smorest import Blueprint, abort
from storerestapi.schemas import ItemSchema, ItemUpdateSchema

from sqlalchemy.exc import SQLAlchemyError

from models import db, ItemModel
blp = Blueprint("items", __name__, description="Operations for items")

# Gets list or adds an item
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # Create new item
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occured inserting the item into the database.')

        return item

# Operates directly on a specified item
@blp.route("/item/<string:item_id>")
class ItemGeneral(MethodView):
    blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        store = ItemModel.query.get_or_404(item_id)
        db.session.delete(store)
        db.session.commit()
        return {"message" : "item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data['name']
            item.price = item_data['price']
        else: # If product doesnt exist, create a new product.
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item

