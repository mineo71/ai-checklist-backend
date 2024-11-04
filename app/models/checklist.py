from app.extensions import mongo

class Checklist:
    @staticmethod
    def create_checklist(name, user_id, style=None):
        return mongo.db.checklists.insert_one({
            "name": name,
            "user_id": user_id,
            "style": style,
        })

class ChecklistItem:
    @staticmethod
    def create_item(name, parent_id, priority="low", status=False, style=None):
        return mongo.db.checklist_items.insert_one({
            "name": name,
            "parent_id": parent_id,
            "status": status,
            "priority": priority,
            "style": style,
        })
