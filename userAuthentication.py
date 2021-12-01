import bcrypt
from flask import Blueprint, request, jsonify, make_response
from pymongo import MongoClient
from bson import ObjectId
import jwt
import datetime
from functools import wraps

usersAuth = Blueprint('usersAuth', __name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.theOffice
UsersDB = db.Users
url = "http://localhost:"
port = "5000"

blacklist = db.blacklist

@usersAuth.route("/login", methods=["GET"])
def login():
    auth = request.authorization
    if auth:
        user = UsersDB.find_one({"username": auth["username"]})
        if user is not None:
            if bcrypt.checkpw(bytes(auth["password"], 'UTF-8'), user["password"]):
                token = jwt.encode({
                    'user': auth["username"],
                    "exp" : datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)
                }, 'SECRET_KEY')
                return make_response(jsonify( {'token': token}
                ), 201)
            else:
                return make_response(jsonify({"Error" : "Incorrect Password"}), 401)
        return make_response(jsonify({"Error":  "Incorrect Username"}), 402)
    return make_response(jsonify({"Error": "Authentication is required"}), 403)



@usersAuth.route("/register", methods=["POST"])
def register():
    if "email" in request.form and "username" in request.form and "password" in request.form:
        password = request.form["password"]
        newUser = {
            "email": request.form["email"],
            "username" : request.form["username"],
            "password" : bcrypt.hashpw(bytes(password, 'UTF-8'),bcrypt.gensalt()),
            "access" : ["User"]
        }

        UsersDB.insert_one(newUser)
        return make_response( jsonify( { "New User Registered" : "Success"} ), 201)
    else:
        return make_response( jsonify( {"Error" : "Missing Form Data"}), 404)


@usersAuth.route("/<string:id>", methods=["GET"])
def show_user(id):
    if ObjectId.is_valid(id):
        user = UsersDB.find_one({"_id": ObjectId(id)})
        user["_id"] = str(user["_id"])
        del user ['password']
        return make_response(jsonify(user), 200)
    else:
        return make_response(jsonify({"Error": "Invalid User ID"}), 400)



@usersAuth.route("/logout", methods=["GET"])
def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one = ({'token': token})
    return make_response(jsonify({"Message":"Logout Successful"}), 200)

def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({'Token Error Message': 'Token is Missing'}), 401
        try:
            data = jwt.decode(token, "PRIVATE_KEY")
        except:
            return jsonify({'Token Error Message': 'Token is Invalid'}), 401
        bl_token = blacklist.find_one({"token" : token})
        if bl_token is not None:
            return make_response(jsonify({"Token Has been Cancelled"}), 401)

        return func(*args, **kwargs)
    return jwt_required_wrapper

def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = request.headers["x-access-token"]
        data = jwt.decode(token, "PRIVATE_KEY")
        if data["admin"]:
            return func(*args, **kwargs)
        else:
            return make_response(jsonify({'Admin Error Message': 'Admin Access Required'}), 401)

    return admin_required_wrapper


