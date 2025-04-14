import io
import json
from datetime import datetime

from flask import Blueprint, jsonify, send_file
from app.extensions import mongo
from bson import ObjectId

data_bp = Blueprint('data', __name__)


@data_bp.route('/export/<user_id>', methods=['GET'])
def export_data(user_id):
    user_id = ObjectId(user_id)
    hives = list(mongo.db.hives.find({"user_id": user_id}))
    honeycombs = list(mongo.db.honeycombs.find({"hive_id": {"$in": [h["_id"] for h in hives]}}))

    # Convert ObjectIds
    for h in hives:
        h['_id'] = str(h['_id'])
        h['user_id'] = str(h['user_id'])

    for c in honeycombs:
        c['_id'] = str(c['_id'])
        c['hive_id'] = str(c['hive_id'])

    return jsonify({
        "hives": hives,
        "honeycombs": honeycombs
    })

@data_bp.route('/export-download/<user_id>', methods=['GET'])
def export_download(user_id):
    user_id = ObjectId(user_id)
    hives = list(mongo.db.hives.find({"user_id": user_id}))
    honeycombs = list(mongo.db.honeycombs.find({"hive_id": {"$in": [h["_id"] for h in hives]}}))

    for h in hives:
        h['_id'] = str(h['_id'])
        h['user_id'] = str(h['user_id'])
        h['created_at'] = h['created_at'].isoformat()
        h['updated_at'] = h['updated_at'].isoformat()

    for c in honeycombs:
        c['_id'] = str(c['_id'])
        c['hive_id'] = str(c['hive_id'])
        c['created_at'] = c['created_at'].isoformat()
        c['updated_at'] = c['updated_at'].isoformat()
        if 'deadline' in c and isinstance(c['deadline'], datetime):
            c['deadline'] = c['deadline'].isoformat()

    export_data = {
        "hives": hives,
        "honeycombs": honeycombs
    }

    json_data = json.dumps(export_data, indent=2)
    buffer = io.BytesIO(json_data.encode('utf-8'))

    return send_file(
        buffer,
        mimetype='application/json',
        as_attachment=True,
        download_name='combly_export.json'
    )

@data_bp.route('/cleanup/<user_id>', methods=['DELETE'])
def delete_all_data(user_id):
    user_id = ObjectId(user_id)
    hive_ids = [h['_id'] for h in mongo.db.hives.find({"user_id": user_id})]
    mongo.db.honeycombs.delete_many({"hive_id": {"$in": hive_ids}})
    mongo.db.hives.delete_many({"user_id": user_id})
    return jsonify({"message": "All hives and honeycombs deleted"})
