from db import db  #ORM model



class StoreModel(db.Model): # maps row in table with python class
    __tablename__ = "stores"  # table name

    id = db.Column(db.Integer, primary_key=True)  #autoincrements --> this is foreign Key mapping items
    name = db.Column(db.String(80), unique=True, nullable = False )

    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")

    # lazy="dynamic" = no prefetch, cascade will delete all depending data