from flask import Blueprint, request, jsonify, make_response, app, Blueprint
from pymongo import MongoClient
from bson import ObjectId
import jwt
from functools import wraps


office_episodes = Blueprint("office_episodes", __name__)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.theOffice
officeEpisodes = db.officeEpisodes
favouriteEpisodes = db.favouriteEpisodes


@office_episodes.route("/", methods=["GET"])
def show_all_episodes():
        page_num, page_size = 1, 9
        if request.args.get("pn"):
            page_num = int(request.args.get('pn'))
        if request.args.get("ps"):
            page_size = int(request.args.get('ps'))
        page_start = (page_size * (page_num - 1))

        data_to_return = []
        for office_episode in officeEpisodes.find().skip(page_start).limit(page_size):
            office_episode["_id"] = str(office_episode["_id"])
            for review in office_episode["review"]:
                review["_id"] = str(review["_id"])
            data_to_return.append(office_episode)

        return make_response (jsonify( data_to_return), 200)

@office_episodes.route("/<string:id>/", methods=["GET"])
def show_one_episode(id):
    office_episode = officeEpisodes.find_one( { "_id" : ObjectId(id) })

    if ObjectId(id) == office_episode["_id"]:
        office_episode["_id"] = str(office_episode["_id"])
        for review in office_episode["review"]:
            review["_id"] = str(review["_id"])
        return make_response(jsonify(office_episode, 200))
    else:
        return make_response(jsonify({"Error" : "Invalid Episode ID"}), 404)


@office_episodes.route("/<string:id>/reviews", methods=["GET"])
def show_episode_review(id):
    data_to_return = []
    office_episode = officeEpisodes.find_one({"_id": ObjectId(id)},
                                             {"_id": 0, "review.$": 1, })

    for review in office_episode["review"]:
        print(review)
        review["_id"] = str(review["_id"])
        data_to_return.append(review)


    return make_response(jsonify(data_to_return), 201)


@office_episodes.route("/season/", methods=["GET"])
def show_season():

    season = {}
    page_num, page_size = 1, 30
    if request.args.get("s"):
        season = {"season": int(request.args.get("s"))}
    season_start = (1)

    data_to_return = []
    for office_episode in officeEpisodes.find(season).skip(season_start).limit(page_size):
        office_episode["_id"] = str(office_episode["_id"])
        for review in office_episode["review"]:
            review["_id"] = str(review["_id"])
        data_to_return.append(office_episode)

    return make_response(jsonify(data_to_return), 200)









