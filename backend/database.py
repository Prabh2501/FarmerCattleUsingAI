import pandas as pd
import os
from datetime import datetime

DB_FILE = "records.csv"

COLUMNS = [
    "animal_id",      # internal only
    "animal_type",    # Cow, Goat, etc
    "display_name",   # Farmer editable
    "attendance",     # integer
    "health_status",  # Healthy / Needs Vet Support
    "last_seen"       # timestamp
]

def init_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DB_FILE, index=False)

def load_db():
    init_db()
    return pd.read_csv(DB_FILE)

def save_db(df):
    df.to_csv(DB_FILE, index=False)

def upsert_animal(animal_id, animal_type, health_status):
    df = load_db()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if animal_id in df["animal_id"].values:
        # Animal already exists → update last seen only
        idx = df[df["animal_id"] == animal_id].index[0]
        df.at[idx, "last_seen"] = now
        df.at[idx, "health_status"] = health_status
    else:
        # New animal → add row
        new_row = {
            "animal_id": animal_id,
            "animal_type": animal_type,
            "display_name": animal_type,
            "attendance": 1,
            "health_status": health_status,
            "last_seen": now
        }
        df.loc[len(df)] = new_row

    save_db(df)

def get_all_animals():
    return load_db()

def delete_animal(animal_id):
    df = load_db()
    df = df[df["animal_id"] != animal_id]
    save_db(df)

def update_display_name(animal_id, new_name):
    df = load_db()
    df.loc[df["animal_id"] == animal_id, "display_name"] = new_name
    save_db(df)
