import os
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("BROKER")
BACKEND = os.getenv("BACKEND")
INPUT_FOLDER = os.getenv("INPUT_FOLDER")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
MODEL_PATH = os.getenv("MODEL_PATH")
