from marshmallow import Schema, fields

#here we do some validation settings for a fields in api interchange
class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True) #used only for returning data , NEVER in request
    name = fields.Str(required=True) # used in request, so not dump_only !, Required = True , mandatory, must be present
    price = fields.Float(required=True)
    #store_id = fields.Str(required=True)  #database will connect to stores

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True) #used only when we are sending data back
    name = fields.Str(required=True) # we need name for store

class ItemUpdateSchema(Schema):
    name = fields.Str() # it is not mandatory for upade, can be sent from user only one
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):  # inherits - extends PlainItemSchema
    store_id = fields.Int(required=True, load_only=True) # we pass store_id when RTECEIVING data from the client
    store = fields.Nested(PlainStoreSchema(), dump_only=True) #nested other schema inside - only for RETURNING data to the client

class StoreSchema(PlainStoreSchema): # inherits - extends PlainStoreSchema
        items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)  # StoreShena is after ItemSchema as it nesting this

# When we use the Nesting  we can incluse only a part of the fields and not this nested fields