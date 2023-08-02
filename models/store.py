from models import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    # Deletes items when store is deleted*
    items = db.relationship("ItemModel", back_populates="store", cascade="all, delete", lazy="dynamic")
