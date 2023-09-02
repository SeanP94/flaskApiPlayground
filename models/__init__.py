from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import for easier access.
from models.item import ItemModel
from models.store import StoreModel
from models.tag import TagModel

# Will be deleted on next iteration
items = {}
stores = {}