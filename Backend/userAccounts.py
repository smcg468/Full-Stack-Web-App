from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://127.0.0.1:2717")
db = client.theOffice
UsersDB = db.Users

url = "http://localhost:"
port = "5000"

accounts = [
          { "name" : "Eddie McGarry",
            "username" : "EddieUser",
            "password" : b"UserPassword",
            "email" : "EddieMcG@user.net",
            "admin" : False
          },
          { "name" : "Sean McGarry",
            "username" : "SeanAdmin",
            "password" : b"AdminPassword",
            "email" : "SeanMcG@admin.net",
            "admin" : True
          },
          { "name" : "Catherine McGarry",
            "username" : "CatherineUser",
            "password" : b"UserPassword1",
            "email" : "CatherineMcG@user.net",
            "admin" : False
          }
       ]

for newUser in accounts:
      newUser["password"] = bcrypt.hashpw(newUser["password"], bcrypt.gensalt())
      UsersDB.insert_one(newUser)
