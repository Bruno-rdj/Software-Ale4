import os

INSTANCE_ID = os.getenv("INSTANCE_ID", "backend-unknown")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
