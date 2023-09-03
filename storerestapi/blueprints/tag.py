from flask.views import MethodView
from flask_smorest import Blueprint, abort
from storerestapi.schemas import TagSchema

from sqlalchemy.exc import SQLAlchemyError

from models import db, TagModel, StoreModel
blp = Blueprint("Tags", __name__, description="Operations for tags")


@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema)
    def get(self, store_id):
        stores = StoreModel.query.get_or_404(store_id)
        return stores.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(
                TagModel.store_id == store_id,
                TagModel.name == tag_data["name"]).first():
            abort(400, message="Tag with that name for this store already exists.")

        tag = TagModel(**tag_data)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag 
    
@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag