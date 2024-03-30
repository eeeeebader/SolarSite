import os

MONGO_DB_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_DB_HOST = os.environ.get("MONGO_URL", "192.168.178.225")
MONGO_DB_USER = "admin"
MONGO_DB_PASS = "admin"