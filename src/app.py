"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favourites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_all_characters():
    raw_list = Characters.query.all()

    serialed_list = [ character.serialize() for character in raw_list]

    return jsonify(serialed_list), 200

@app.route('/people/<int:id>', methods=["GET"])
def get_single_character_by_id(id):

    raw_character = Characters.query.get_or_404(id)
    serialized_character = raw_character.serialize()

    return jsonify(serialized_character), 200

@app.route('/planets', methods =["GET"])
def get_all_planets():

    raw_list = Planets.query.all()
    serialized_list = [ planet.serialize() for planet in raw_list]

    return jsonify(serialized_list),200

@app.route('/planets/<int:id>', methods =["GET"])
def get_single_planet_by_id(id):

    raw_planet = Planets.query.get_or_404(id)
    serialized_planet = raw_planet.serialize()

    return jsonify(serialized_planet),200


@app.route('/users', methods=["GET"])
def get_all_users():

    raw_list = User.query.all()
    serialized_list = [ user.serialize() for user in raw_list]

    return jsonify(serialized_list),200

@app.route("/users/favourites/", methods=["GET"])
def get_single_user_favourites():

    favourites_list = Favourites.query.filter_by(user_id=1)
    favourite_list_serialized = [ favourite.serialize() for favourite in favourites_list]
    
    return jsonify(favourite_list_serialized),200


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_planet_to_user_favourites(planet_id):
    
    target_planet = Planets.query.get_or_404(planet_id)
    new_fav = Favourites(
        user_id = 1,
        external_type = "planet",
        external_id = target_planet.id
    )

    db.session.add(new_fav)
    db.session.commit()

    response = {
        "msg" : "Favourite planet added"
    }

    return jsonify(response),200


@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_character_to_user_favourites(people_id):
    
    target_character = Characters.query.get_or_404(people_id)
    new_fav = Favourites(
        user_id = 1,
        external_type = "people",
        external_id = target_character.id
    )

    db.session.add(new_fav)
    db.session.commit()

    response = {
        "msg" : "Favourite character added"
    }

    return jsonify(response),200


@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def remove_planet_from_user_favourites(planet_id):
    
    target_fav = Favourites.query.filter_by(external_type="planet").filter_by(external_id=planet_id).first()

    db.session.delete(target_fav)
    db.session.commit()

    response = {
        "msg" : "Favourite planet successfully removed"
    }

    return jsonify(response),200


@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def remove_character_from_user_favourites(people_id):
    
    target_fav = Favourites.query.filter_by(external_type="people").filter_by(external_id=people_id).first()

    db.session.delete(target_fav)
    db.session.commit()

    response = {
        "msg" : "Favourite planet successfully removed"
    }

    return jsonify(response),200






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
