from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")

#-----------------------TAG IN STORE-----------------------------------------------------
@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    
    """GET ALL TAGS"""
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()  # lazy="dynamic" means 'tags' is a query

    """CREATE TAGS"""
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return tag

#-----------------------TAG id TO ITEM id-----------------------------------------------------
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    """ LINK ITEM TO A TAG"""
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        #FIND ITEM AND TAG SO WE KNOW THEY EXIST
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag) #TAGS is a list

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag
    
    """ DELETE LINK ITEM FROM A TAG / UNLINK"""
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}

#-----------------------TAG OPERATIONS-----------------------------------------------------
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):

    """GET SPECIFIC TAG"""
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    """DELETE A  SPECIFIC TAG"""
    #Definition of main response
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )

    #Definition of alternative  response 1
    @blp.alt_response(404, description="Tag not found.")
    
    #Definition of alternative  response 2
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id) #find a tag

        if not tag.items:  #delete only  if no itensa are connected (we need to chech they are the same store too)
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",  # noqa: E501
        )
