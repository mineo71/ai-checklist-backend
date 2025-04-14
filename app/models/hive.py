from app.extensions import mongo
from datetime import datetime


class Hive:
    @staticmethod
    def create_hive(name, user_id):
        return mongo.db.hives.insert_one({
            "name": name,
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })

    @staticmethod
    def get_user_hives(user_id):
        return list(mongo.db.hives.find({"user_id": user_id}))

    @staticmethod
    def rename_hive(hive_id, new_name):
        return mongo.db.hives.update_one(
            {"_id": hive_id},
            {"$set": {"name": new_name, "updated_at": datetime.utcnow()}}
        )

    @staticmethod
    def delete_hive(hive_id):
        mongo.db.honeycombs.delete_many({"hive_id": hive_id})
        return mongo.db.hives.delete_one({"_id": hive_id})


class Honeycomb:
    @staticmethod
    def create_honeycomb(hive_id, title, description=None, icon=None, color=None,
                         priority="low", deadline=None):
        return mongo.db.honeycombs.insert_one({
            "hive_id": hive_id,
            "title": title,
            "description": description,
            "icon": icon,
            "color": color,
            "priority": priority,
            "deadline": deadline,
            "status": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })

    @staticmethod
    def update_honeycomb(honeycomb_id, data):
        return mongo.db.honeycombs.update_one(
            {"_id": honeycomb_id},
            {"$set": {**data, "updated_at": datetime.utcnow()}}
        )

    @staticmethod
    def mark_completed(honeycomb_id):
        return mongo.db.honeycombs.update_one(
            {"_id": honeycomb_id},
            {"$set": {"status": True, "updated_at": datetime.utcnow()}}
        )

    @staticmethod
    def delete_honeycomb(honeycomb_id):
        return mongo.db.honeycombs.delete_one({"_id": honeycomb_id})
