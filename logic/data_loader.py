import json
import os

def load_json_data(filename):
    # Ścieżka od głównego folderu death_clock_web
    path = os.path.join('DeathClockEngine', 'data', filename)
    with open(path, 'r', encoding="utf-8") as f:
        return json.load(f)