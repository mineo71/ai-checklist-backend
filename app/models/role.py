from app.extensions import mongo

class Role:
    @staticmethod
    def create_role(role_name):
        return mongo.db.roles.insert_one({"role_name": role_name})

    @staticmethod
    def get_role_by_id(role_id):
        return mongo.db.roles.find_one({"_id": role_id})
