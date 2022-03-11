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

blacklist = db.blacklist

@usersAuth.route("/login", methods=["GET"])
def login():
    auth = request.authorization
    print(auth)
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
            "access" : "User",
        }

        UsersDB.insert_one(newUser)
        return make_response( jsonify( { "New User Registered" : "Success"} ), 201)
    else:
        print(request.form)
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


