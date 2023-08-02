from marshmallow import Schema, fields

'''
Schema is used to set the logical data from the API calls.
This will save us a lot of if/then logic and will verify that the data comes in matching the schema.
'''

class BasicItemSchema(Schema):
    id = fields.Int(dump_only=True) # Used only in the API call itself.
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    

class BasicStoresSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

# Helps get all
class ItemSchema(BasicItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(BasicStoresSchema(), dump_only=True)


# Notice how these just include all, but dont force you to use them
# So we can use this to either update or create new with put.
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

# Helps get all
class StoresSchema(BasicStoresSchema):
    items = fields.List(fields.Nested(BasicItemSchema()), dump_only=True)
