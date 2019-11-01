import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(ROOT_DIR, ".data")
APP_DATA_FILE = os.path.join(DATA_DIR, "app.json")
ICONS_DIR = os.path.join(ROOT_DIR, "Assets", "Icons")
