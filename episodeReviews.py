from flask import Flask, request, jsonify, make_response, Blueprint
from pkg_resources import require
from pymongo import MongoClient
from bson import ObjectId

from office_episodes import office_episodes

episode_reviews = Blueprint("episode_reviews", __name__)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.theOffice
officeEpisodes = db.officeEpisodes
url = 'http://localhost:'
port = '5000'


@episode_reviews.route("/", methods=["GET"])
def show_all_reviews():
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get('pn'))
    if request.args.get("ps"):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    data_to_return = []
    for review in officeEpisodes.find().skip(page_start).limit(page_size):
        review["_id"] = str(review["_id"])
        data_to_return.append(review)

    return make_response(jsonify(data_to_return), 200)


@episode_reviews.route("/<string:id>/", methods=["GET"])
def show_episode_reviews(id):
    data_to_return = []

    if ObjectId.is_valid(id):
        officeEpisode = officeEpisodes.find_one({'_id': ObjectId(id)},
        {"review": 1, "_id": 0})

    else:
        return make_response(jsonify({"Error": "Invalid Episode"}), 401)

    for reviews in officeEpisode['review']:
        print(reviews)
        reviews["_id"] = str(reviews["_id"])
        data_to_return.append(reviews)

    return make_response(jsonify(data_to_return), 200)

@episode_reviews.route("/<string:id>/", methods=["POST"])
def add_review(id):

    if "username" in request.form and "rating" in request.form and "review" in request.form:
        review = {
            "_id": ObjectId(),
            "username": request.form["username"],
            "rating": request.form["rating"],
            "review": request.form["review"],
        }

        officeEpisodes.update_one(
            {"_id": ObjectId(id)},
            {"$push": {"review": review}}
        )

        review_id = str(review["_id"])
        review_link = f"http://localhost:5000/v1.0/episode_reviews/{review_id}"
        return make_response(jsonify({"New Review URL": review_link}), 201)
    else:
        return make_response(jsonify({"Error": "Missing Form Data"}), 404)


@episode_reviews.route("/<string:review_id>", methods=["PUT"])
def edit_review(review_id):
    if "rating" in request.form and "review" in request.form:
        edited_review = {
                "review.$.username": request.form["username"],
                "review.$.rating": request.form["rating"],
                "review.$.review": request.form["review"]
                }
    else:
        return make_response(jsonify({"Error": "Missing Form Data"}), 404)

    if ObjectId.is_valid(review_id):
        officeEpisodes.update_one(
            {"review._id": ObjectId(review_id)},
            {"$set": edited_review})


        edited_review_link = "http://localhost:5000/v1.0/episode_reviews/" + review_id
        return make_response(jsonify({"Edited Review URL": edited_review_link}), 200)
    else:
        return make_response(jsonify({"Error": "Invalid Review ID"}), 404)


@episode_reviews.route("/<string:review_id>/", methods=["DELETE"])
def delete_review(review_id):
    if ObjectId.is_valid(review_id):

        officeEpisodes.update_one({"review._id": ObjectId(review_id)},
                              {"$pull": {"review":{"_id": ObjectId(review_id)}}})

        return make_response(jsonify({"Message":"Review Deleted"}), 200)
    else:
        return make_response(jsonify({"Error":"Invalid Review ID"}), 404)