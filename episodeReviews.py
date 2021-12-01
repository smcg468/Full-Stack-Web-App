from flask import Flask, request, jsonify, make_response, Blueprint
from pkg_resources import require
from pymongo import MongoClient
from bson import ObjectId

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
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get('pn'))
    if request.args.get("ps"):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    data_to_return = []

    for reviews in officeEpisodes.find({"office_episode" : id}).skip(page_start).limit(page_size):
        reviews["_id"] = str(reviews["_id"])
        data_to_return.append(reviews)

    return make_response(jsonify(data_to_return), 200)

@episode_reviews.route("/", methods=["POST"])
def add_review():

    if "username" in request.form and "id" in request.form and "review" in request.form:
        review = {
            "username": request.form["username"],
            "id": int(request.form["id"]),
            "rating": request.form["rating"],
            "review": request.form["review"],
        }

        review_id = officeEpisodes.insert_one(review)
        review_link = f"http://localhost:5000/v1.0/episode_reviews/{str(review_id.inserted_id)}"
        return make_response(jsonify({"New Review URL": review_link}), 201)
    else:
        return make_response(jsonify({"Error": "Missing Form Data"}), 404)


@episode_reviews.route("/<string:id>", methods=["PATCH"])
def edit_review(id):
    if "username" in request.form and "rating" in request.form and "review" in request.form:
        result = officeEpisodes.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "username": request.form["username"],
                "rating": request.form["rating"],
                "review": request.form["review"]
            }
            }
        )

        if result.matched_count == 1:
            edited_review_link = "http://localhost:5000/v1.0/episode_reviews/" + id
            return make_response(jsonify({"Updated Review URL": edited_review_link}), 200)
        else:
            return make_response(jsonify({"Error": "Invalid Review ID"}), 404)
    else:
        return make_response(jsonify({"Error": "Missing Form Data"}), 404)


@episode_reviews.route("/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    if ObjectId.is_valid(review_id):

        officeEpisodes.update_one({"review._id": ObjectId(review_id)},
                              {"$pull": {"review":{"_id": ObjectId(review_id)}}})

        return make_response(jsonify({"Review Successfully Deleted"}), 200)
    else:
        return make_response(jsonify({"Invalid Review ID"}), 404)