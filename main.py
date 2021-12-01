from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from episodeReviews import episode_reviews
from office_episodes import office_episodes, officeEpisodes
from userAuthentication import usersAuth
from flask_cors import CORS

main = Flask(__name__)
CORS(main)
url = "http://localhost:"
port = "5000"


main.config["SECRET_KEY"] = "SECRET_KEY"
main.register_blueprint(office_episodes, url_prefix = "/v1.0/office_episodes/")
main.register_blueprint(episode_reviews, url_prefix = "/v1.0/episode_reviews/")
main.register_blueprint(usersAuth, url_prefix = "/v1.0/users/")

@main.route("/")
def app():
    return make_response(jsonify("MongoDB and Python API"))

if __name__ == "__main__":
    main.run(debug=True)