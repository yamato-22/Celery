import os
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("BROKER")
BACKEND = os.getenv("BACKEND")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
PROCESS_FOLDER= os.getenv("PROCESS_FOLDER")
