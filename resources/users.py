from flask.views import MethodView
from flask_smorest import Blueprint, abort
#from .exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UsersSchema

blp = Blueprint("Users", "users", description="Operations on users")

# When you create a Flask application, you start by creating a Flask object that represents your application, and then you associate views to routes. 
# Flask takes care of dispatching incoming requests to the correct view based on the request URL and the routes you’ve defined.
# Flask Blueprints encapsulate functionality, such as views, templates, and other resources.

#----------------------- User Register -----------------------------------------------------
@blp.route("/register")   # register Endpoint
class UserRegister(MethodView): #Dispatches request methods to the corresponding instance methods. For example, if you implement a get method, it will be used to handle GET requests.
    @blp.arguments(UsersSchema)
    def post(self, user_data):
        #user_data is a dictionary with username and password (see json)
        #chek if username is unique, we can skip this and catch 'Integryty error' during insertion into database (better solution)
        if UserModel.query.filter(UserModel.username == user_data["username"]).first(): #database query
            abort(409, message = "A user with that username already exists.")

        #continue to create a user model
        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"]) #save hasehd pass
        )    
        #save in database
        db.session.add(user)
        db.session.commit()

        return {"messasge": "User Created successfully."}, 201


#----------------------- User Login Token -----------------------------------------------------   
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UsersSchema)
    def post(self, user_data):    

        #get a user from a db and chek 
        user =  UserModel.query.filter(UserModel.username == user_data["username"]).first() #database query om database - get user or NONE if not foud
        if user and pbkdf2_sha256.verify(user_data["password"], user.password): # chek the password
            access_token  = create_access_token(identity=user.id, fresh=True)      #jwt.io web toke is specific for the user and grant the access
            refresh_token = create_refresh_token(identity=user.id)  
            return {"access_token": access_token, "refresh_token": refresh_token}
        
        abort(401, message = "Invalid Crtedential")

#----------------------- User Refresh Token --------------------------------------------------
@blp.route("/refresh")     
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity = current_user, fresh=False)
        jti = get_jwt()["jti"] 
        BLOCKLIST.add(jti)
        return {"access_token": new_token}

#----------------------- User Logout ---------------------------------------------------------
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]  #same as  jti = get_jwt().get("jti")
        
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
        
               

#----------------------- User Get & Delete -----------------------------------------------------    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UsersSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user


    def delete(self, user_id):    
        user = UserModel.query.get_or_404(user_id)

        #delete from database
        db.session.delete(user)
        db.session.commit()

        return {"messasge": "User deleted successfully."}, 200
