from flask import Blueprint, request, jsonify
from app.models.hive import Hive, Honeycomb
from bson import ObjectId

hive_bp = Blueprint('hives', __name__)


@hive_bp.route('/hives', methods=['POST'])
def create_hive():
    data = request.get_json()
    result = Hive.create_hive(data['name'], ObjectId(data['user_id']))
    return jsonify({"hive_id": str(result.inserted_id)}), 201


@hive_bp.route('/hives/<user_id>', methods=['GET'])
def get_hives(user_id):
    hives = Hive.get_user_hives(ObjectId(user_id))
    for h in hives:
        h['_id'] = str(h['_id'])
        h['user_id'] = str(h['user_id'])
    return jsonify(hives)


@hive_bp.route('/hives/<hive_id>', methods=['PUT'])
def rename_hive(hive_id):
    data = request.get_json()
    Hive.rename_hive(ObjectId(hive_id), data['name'])
    return jsonify({"message": "Hive renamed successfully"})


@hive_bp.route('/hives/<hive_id>', methods=['DELETE'])
def delete_hive(hive_id):
    Hive.delete_hive(ObjectId(hive_id))
    return jsonify({"message": "Hive and its honeycombs deleted"})


@hive_bp.route('/honeycombs', methods=['POST'])
def create_honeycomb():
    data = request.get_json()
    result = Honeycomb.create_honeycomb(
        ObjectId(data['hive_id']),
        data['title'],
        data.get('description'),
        data.get('icon'),
        data.get('color'),
        data.get('priority', 'low'),
        data.get('deadline')
    )
    return jsonify({"honeycomb_id": str(result.inserted_id)}), 201


@hive_bp.route('/honeycombs/<honeycomb_id>', methods=['PUT'])
def update_honeycomb(honeycomb_id):
    data = request.get_json()
    Honeycomb.update_honeycomb(ObjectId(honeycomb_id), data)
    return jsonify({"message": "Honeycomb updated"})


@hive_bp.route('/honeycombs/<honeycomb_id>/complete', methods=['PUT'])
def complete_honeycomb(honeycomb_id):
    Honeycomb.mark_completed(ObjectId(honeycomb_id))
    return jsonify({"message": "Honeycomb marked as complete"})


@hive_bp.route('/honeycombs/<honeycomb_id>', methods=['DELETE'])
def delete_honeycomb(honeycomb_id):
    Honeycomb.delete_honeycomb(ObjectId(honeycomb_id))
    return jsonify({"message": "Honeycomb deleted"})
