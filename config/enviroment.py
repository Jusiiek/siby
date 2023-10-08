import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

SERVER_ID = os.getenv('SERVER_ID')
MAIN_VC_CHANNEL_ID = os.getenv('MAIN_VC_CHANNEL_ID')
