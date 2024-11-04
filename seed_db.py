from app import create_app
from app.extensions import mongo

app = create_app()

with app.app_context():
    roles_collection = mongo.db.roles
    if roles_collection.count_documents({}) == 0:
        roles_collection.insert_many([
            {"role_name": "Admin"},
            {"role_name": "User"},
            {"role_name": "Guest"}
        ])
    print("Database seeded successfully.")
