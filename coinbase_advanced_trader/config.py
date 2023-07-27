import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API_KEY and API_SECRET using environment variables
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
TELEGRAM = os.environ.get('TELEGRAM')

# Check if the environment variables are set
if not API_KEY or not API_SECRET or not TELEGRAM:
    raise ValueError("Please set the API_KEY and API_SECRET and the TELEGRAM environment variables.")

API_PATH = '/api/v3/brokerage'
