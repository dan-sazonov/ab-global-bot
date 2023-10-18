import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Bot:
    bot_token: str
    admin_id: int


def _get_settings():
    load_dotenv()
    return Bot(bot_token=os.getenv("BOT_TOKEN"),
               admin_id=int(os.getenv("ADMIN_ID")))


settings = _get_settings()
