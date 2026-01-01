import os
import json
from datetime import datetime

DATA_DIR = "data"

def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def add_performance(user_id: int, raw_text: str, formatted_text: str, performance_slot: str):
    _ensure_data_dir()
    performance_filename = f"{DATA_DIR}/{user_id}_{performance_slot}.json"
    performance_data = {
        "user_id": user_id,
        "raw_text": raw_text,
        "formatted_text": formatted_text,
        "timestamp": str(datetime.now())
    }
    with open(performance_filename, "w") as f:
        json.dump(performance_data, f)

def get_user_performances(user_id: int):
    _ensure_data_dir()
    performance_files = [f for f in os.listdir(DATA_DIR) if f.startswith(str(user_id))]
    performances = []
    for performance_file in performance_files:
        with open(f"{DATA_DIR}/{performance_file}", "r") as f:
            performances.append(json.load(f))
    return performances
