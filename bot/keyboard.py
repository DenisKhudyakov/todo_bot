from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_calendar import SimpleCalendar

from database.views import get_tasks


async def generate_keyboard_kalendar():
    kalendar = await SimpleCalendar(locale="ru_RU.UTF-8").start_calendar()
    return kalendar


questions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Календарь", callback_data="kalendar")],
    [InlineKeyboardButton(text="Поставить задачу", callback_data="add_task")],
    [InlineKeyboardButton(text="Список задач", callback_data="list_tasks")],
])

cancel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отмена")],
], resize_keyboard=True)


async def tasks_keyboard():
    keyboard = InlineKeyboardBuilder()
    result = await get_tasks()
    for task in result:
        if not task.is_done:
            keyboard.add(InlineKeyboardButton(text=f"{task.id}-{task.description}", callback_data=f"task_{task.id}"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    
    return keyboard.adjust(1).as_markup()
    
choise_task = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Да", callback_data="YES"), InlineKeyboardButton(text="Нет", callback_data="NO")]]
)

update_task_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="UPDATE_YES"), InlineKeyboardButton(text="Нет", callback_data="NO")]
])