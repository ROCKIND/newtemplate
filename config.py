import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

API_ID = int(environ.get("API_ID", ""))
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

LOG_CHANNEL = int(environ.get("LOG_CHANNEL", ""))

# Database Channel For Text Or Caption Store 
FILE_CHANNEL = int(environ.get("FILE_CHANNEL", ""))

ADMINS = int(environ.get("ADMINS", ""))

# Mongodb Database 
DB_URI = environ.get("DB_URI", "")
DB_NAME = environ.get("DB_NAME", "chatvjbot")

# True Or False
REQUEST_TO_JOIN_MODE = bool(environ.get("REQUEST_TO_JOIN_MODE", True))
FORWARD = bool(environ.get("FORWARD", False))

# Force subscribe channel 
auth_channel = environ.get('AUTH_CHANNEL', '') # give your force subscribe channel id here else leave it blank
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

second_auth_channel = environ.get('SECOND_AUTH_CHANNEL', '') # give your force subscribe channel id here else leave it blank
SECOND_AUTH_CHANNEL = int(second_auth_channel) if second_auth_channel and id_pattern.search(second_auth_channel) else None
