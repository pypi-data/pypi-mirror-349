from app.db.database_hub import DatabaseHub
from app.config import settings

db_hub = DatabaseHub(settings.model_dump())

def get_db_hub():
    return db_hub
