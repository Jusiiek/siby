import os
import json

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

SERVER_ID = os.getenv('SERVER_ID')

# voice channels
MAIN_VC_CHANNEL_ID = os.getenv('MAIN_VC_CHANNEL_ID')

# text channels
WELCOME_CHANNEL_ID = os.getenv('WELCOME_CHANNEL_ID')

# users
ADMINS_IDS = json.loads(os.getenv('ADMINS_IDS'))
