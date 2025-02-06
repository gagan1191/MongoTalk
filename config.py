import os
import json


# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("MONGO_DATABASE", "test_db")

# Load Knowledge Base from JSON file
KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")

def load_knowledge_base():
    """Loads knowledge base from JSON file."""
    with open(KNOWLEDGE_BASE_PATH, "r") as file:
        return json.load(file)

KNOWLEDGE_BASE = load_knowledge_base()
