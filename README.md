# 📝 Telegram Task Planner Bot

## 🚀 Описание
Этот бот помогает вам:
- 📅 **Планировать задачи** — добавлять, удалять и просматривать список дел.
- 🤣 **Рассказывать анекдоты** — немного юмора для поднятия настроения!

Запускается с помощью **Docker**, так что легко разворачивается в любом окружении. 🐳

---

## ⚙️ Запуск через Docker

1️⃣ **Собери Docker-образ:**
```sh
docker build -t task-planner-bot .
```

2️⃣ **Запусти контейнер:**
```sh
docker run -d --name task-planner-bot task-planner-bot
```

3️⃣ **(Опционально) Использование переменных окружения:**
Создай файл `.env` и добавь API токен Telegram:
```env
API_TOKEN=your-telegram-bot-token
DATA_BASE_URL=your data base url
```
Запусти контейнер с загрузкой `.env`:
```sh
docker run --rm --env-file .env task-planner-bot
```

---

## 🛠 Требования для локального запуска

Если не хочешь использовать Docker, установи вручную:
```sh
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows
pip install -r requirements.txt
python main.py
```

---

## 🎯 Функции
✅ **Добавление задач** — `Через Инлайн кнопки`
✅ **Просмотр списка задач** — `Через Инлайн кнопки`
✅ **Удаление задач** — `Через Инлайн кнопки`
✅ **Случайный анекдот** — `/joke`
✅ **Помощь** — `/help`
✅ **Календарь** — `Через Инлайн кнопки`


---

## 📌 Используемые технологии
- **Python 3.12** 🐍
- **Aiogram** 🤖 (для Telegram API)
- **Docker** 🐳 (для контейнеризации)
- **SQLite** 🗃 (возможность хранения задач)

---

## 🔗 Контакты
Разработчик: [DenisKhudyakov](https://github.com/DenisKhudyakov)

Если у тебя есть идеи или предложения — пиши, буду рад обратной связи! 🚀


