from marshmallow import Schema, fields

'''

Schema is used to set the logical data from the API calls.
This will save us a lot of if/then logic and will verify that the data comes in matching the schema.

'''

# Schema for Items:

class ItemSchema(Schema):
    id = fields.Str(dump_only=True) # Used only in the API call itself.
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoresSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)