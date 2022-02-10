"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, json, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from FamilyStructures import Family
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = Family("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    result = jackson_family.get_all_members()
    return jsonify(result=result)


@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    result = jackson_family.get_member(id)
    return jsonify(member=result[0]), result[1]


@app.route('/member', methods=['POST'])
def create_member():
    member = request.get_json()
    result = jackson_family.add_member(member)
    return jsonify(result=result[0]), result[1]


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    result = jackson_family.delete_member(id)
    return jsonify(result=result[0]), result[1]


@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    member = request.get_json()
    result = jackson_family.update_member(id, member)
    return jsonify(member=result[0]), result[1]

    


    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
