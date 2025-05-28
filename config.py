import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

API_ID = int(environ.get("API_ID", "23621595"))
API_HASH = environ.get("API_HASH", "de904be2b4cd4efe2ea728ded17ca77d")
BOT_TOKEN = environ.get("BOT_TOKEN", "7526133561:AAHqNGA98ezLcw3NMfyqQ9vgR5GiBNzsDHc")

LOG_CHANNEL = int(environ.get("LOG_CHANNEL", '-1002499774859'))

# Database Channel For Text Or Caption Store 
FILE_CHANNEL = int(environ.get("FILE_CHANNEL", "-1002499774859"))

ADMINS = int(environ.get("ADMINS", "1562935405"))

# Mongodb Database 
DB_URI = environ.get("DB_URI", "mongodb+srv://Botmaster:Botmaster@cluster08283746473883.mfjsvds.mongodb.net/?retryWrites=true&w=majority&appName=Cluster08283746473883")
DB_NAME = environ.get("DB_NAME", "achatvjbot")

# True Or False
REQUEST_TO_JOIN_MODE = bool(environ.get("REQUEST_TO_JOIN_MODE", True))
FORWARD = bool(environ.get("FORWARD", False))

# Force subscribe channel 
auth_channel = environ.get('AUTH_CHANNEL', '-1002371763393') # give your force subscribe channel id here else leave it blank
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

second_auth_channel = environ.get('SECOND_AUTH_CHANNEL', '-1002552561130') # give your force subscribe channel id here else leave it blank
SECOND_AUTH_CHANNEL = int(second_auth_channel) if second_auth_channel and id_pattern.search(second_auth_channel) else None
