# configs/settings.py
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATA_PATH = "data/"
OUTPUT_PATH = "outputs/"

def load_pipeline_config() -> dict:
    with open("configs/pipeline_config.yaml", "r") as file:
        return yaml.safe_load(file)
