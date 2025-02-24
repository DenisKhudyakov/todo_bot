import asyncio
import json
import random
import aiofiles

async def read_json(file='jokes/anekdoty.json'):
    async with aiofiles.open(file) as f:
        data = await f.read()
        return json.loads(data)
        
        

async def chose_joke():
    """
    Функция случайного выбора анекдота 
    """
    jokes = await read_json()
    joke = random.choice(jokes) if jokes else 'Анекдотов нет'
    return joke
    