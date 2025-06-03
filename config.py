import json
import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    personal_info = {
        "name": os.getenv("NAME"),
        "email": os.getenv("EMAIL"),
        "resume_path": os.getenv("RESUME_PATH"),
        "phone": os.getenv("PHONE"),
        "portfolio": os.getenv("PORTFOLIO")
    }
    for key, value in personal_info.items():
        if key in ["name", "email", "resume_path"] and not value:
            raise ValueError(f"Missing required .env variable: {key}")

    with open("config.json", "r") as f:
        config = json.load(f)

    config["personal_info"] = personal_info
    return config