API_KEY = None
API_SECRET = None
API_PATH = '/api/v3/brokerage'

def set_api_credentials(api_key, api_secret):
    global API_KEY
    global API_SECRET

    API_KEY = api_key
    API_SECRET = api_secret
