from dotenv import load_dotenv, find_dotenv
import os


if not find_dotenv():
    exit('No .env file found')
else:
    load_dotenv()
    
BOT_TOCKEN = os.getenv('BOT_TOCKEN')

DATA_BASE_URL = os.getenv('DATA_BASE_URL')
BOT_COMMANDS = (
    ('/start', 'Запуск бота'),
    ('/joke', 'Вывести случайный анекдот')
)