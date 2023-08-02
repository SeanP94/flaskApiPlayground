from flask.views import MethodView
from flask_smorest import Blueprint, abort
from storerestapi.schemas import StoresSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import db, StoreModel


blp = Blueprint("stores", __name__, description="Operations for stores")

# Gets all stores or creates one
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoresSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoresSchema)
    @blp.response(200, StoresSchema)
    def post(self, store_data):
        # Return if store exsits.
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message='A store with that name already exists.')
        except SQLAlchemyError:
            abort(500, message='An error occured inserting the store into the database.')

        return store

# Operates directly on a store.
@blp.route("/store/<string:store_id>")
class StoreGeneral(MethodView):
    @blp.response(200, StoresSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store, 200

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message" : "store deleted."}
