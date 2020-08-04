import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from feedback_bot.command_replies import Replies

load_dotenv(find_dotenv())

TG_TOKEN = os.environ["TG_BOT_TOKEN"]
PROXY = os.environ.get("RT_HTTPS_PROXY")
CHAT_ID = int(os.environ["TG_CHAT_ID"])
REPLIES: Replies = Replies.load_from_dir(Path(os.environ["COMMAND_REPLIES_PATH"]))
BOT_TIMEOUT = os.environ.get("BOT_TIMEOUT", 30)
BOT_RETRIES = os.environ.get("BOT_RETRIES", 3)
