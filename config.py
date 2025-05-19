import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

API_ID = int(environ.get("API_ID", "23621595"))
API_HASH = environ.get("API_HASH", "de904be2b4cd4efe2ea728ded17ca77d")
BOT_TOKEN = environ.get("BOT_TOKEN", "7355277731:AAENoMRTMYMd4ja8OrVv5VrZWR2l_Oe8p4s")

LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1002648688388"))

# Database Channel For Text Or Caption Store 
FILE_CHANNEL = int(environ.get("FILE_CHANNEL", "-1002600199074"))

ADMINS = int(environ.get("ADMINS", "1249672673"))

# Mongodb Database 
DB_URI = environ.get("DB_URI", "mongodb+srv://dbmongo702:xtb9PzLmv5dstZYG@cluster0.2dxbh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = environ.get("DB_NAME", "chatvjbot")

# True Or False
REQUEST_TO_JOIN_MODE = bool(environ.get("REQUEST_TO_JOIN_MODE", True))
FORWARD = bool(environ.get("FORWARD", False))

# Force subscribe channel 
auth_channel = environ.get('AUTH_CHANNEL', '') # give your force subscribe channel id here else leave it blank
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

second_auth_channel = environ.get('SECOND_AUTH_CHANNEL', '') # give your force subscribe channel id here else leave it blank
SECOND_AUTH_CHANNEL = int(second_auth_channel) if second_auth_channel and id_pattern.search(second_auth_channel) else None
