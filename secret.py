from dotenv import load_dotenv

load_dotenv()

import os

API_KEY = os.getenv("API_KEY")
API_HOST_URL = os.getenv("API_HOST_URL")