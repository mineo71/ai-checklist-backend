from flask import Blueprint, request, jsonify
from app.extensions import mongo
from bson import ObjectId

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/profile/<user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.get_json()
    update_fields = {k: v for k, v in data.items() if k in ['name', 'email']}
    mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
    return jsonify({"message": "Profile updated"})


@settings_bp.route('/settings/<user_id>', methods=['PUT'])
def update_settings(user_id):
    data = request.get_json()
    mongo.db.settings.update_one(
        {"user_id": ObjectId(user_id)},
        {"$set": data},
        upsert=True
    )
    return jsonify({"message": "Settings saved"})


@settings_bp.route('/settings/<user_id>', methods=['GET'])
def get_settings(user_id):
    settings = mongo.db.settings.find_one({"user_id": ObjectId(user_id)})
    if settings:
        settings['_id'] = str(settings['_id'])
        settings['user_id'] = str(settings['user_id'])
    return jsonify(settings or {})
