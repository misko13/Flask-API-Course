from db import db  #ORM model


class ItemModel(db.Model): # maps row in table with python class
    __tablename__ = "items"  # table name

    id = db.Column(db.Integer, primary_key=True)  #autoincrementa
    name = db.Column(db.String(80), unique=True, nullable = False )
    description=db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable = False )
    store_id = db.Column(
         db.Integer, db.ForeignKey("stores.id"), unique=False, nullable = False
    )#  !! 1:n relationship by foreign key, cheks relations in integrity
    store = db.relationship("StoreModel", back_populates = "items" ) #SQLAlchemy knows how to populate the key
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
    


