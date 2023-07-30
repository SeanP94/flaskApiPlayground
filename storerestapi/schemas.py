from marshmallow import Schema, fields

'''

Schema is used to set the logical data from the API calls.
This will save us a lot of if/then logic and will verify that the data comes in matching the schema.

'''

# Schema for Items:

class BasicItemSchema(Schema):
    id = fields.Str(dump_only=True) # Used only in the API call itself.
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    

class BasicStoresSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class ItemSchema(BasicItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(BasicStoresSchema(), dump_only=True)

class StoresSchema(BasicStoresSchema):
    items = fields.List(fields.Nested(BasicItemSchema()), dump_only=True)
