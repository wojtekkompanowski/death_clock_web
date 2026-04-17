import json
import os
import sys


def resource_path(relative_path):
    """ Pobiera ścieżkę do zasobów, obsługując tryb dev i spakowany .exe """
    try:
        # Ścieżka tymczasowa PyInstallera
        base_path = sys._MEIPASS
    except Exception:
        # Standardowa ścieżka podczas pisania kodu
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_json_data(filename):
    # 1. Budujemy ścieżkę do pliku wewnątrz folderu 'data'
    # 2. Przepuszczamy ją przez resource_path, żeby PyInstaller ją znalazł
    path = resource_path(os.path.join('data', filename))

    with open(path, 'r', encoding="utf-8") as f:
        return json.load(f)
