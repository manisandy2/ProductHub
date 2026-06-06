from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path.cwd()

BASE_URL = os.getenv("BaseUrl")
AUTH_URL = os.getenv("AuthUrl")
PRODUCT_URL = os.getenv("href")

OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)