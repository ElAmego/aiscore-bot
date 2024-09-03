import telebot
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bot import activate_tg_bot

# Bot
bot = telebot.TeleBot("BOT API")

# Database
db_url = ("DB_URL")
client = MongoClient(db_url, server_api=ServerApi('1'))
db = client.test_db
collection_users = db.users
collection_config = db.config

url = 'https://www.aiscore.com/ru'


def main():
    activate_tg_bot(bot, collection_users, collection_config, url)


if __name__ == '__main__':
    main()

