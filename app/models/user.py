from app.extensions import mongo
from werkzeug.security import generate_password_hash

class User:
    @staticmethod
    def create_user(name, email, password, role_id):
        hashed_password = generate_password_hash(password)
        return mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "role_id": role_id
        })
