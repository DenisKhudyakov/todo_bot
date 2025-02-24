import locale
from datetime import datetime
from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboard import generate_keyboard_kalendar, questions, cancel, choise_task, tasks_keyboard, update_task_kb
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from database.config import BOT_COMMANDS
from database.db_utils import Tasks
from database.views import add_task, get_task_on_id, get_tasks, update_task
from jokes.read import chose_joke

router = Router()

class FormTask(StatesGroup):
    description = State()
    dead_line = State()
    is_done = State()


class UpdateTask(StatesGroup):
    id = State()


@router.message(CommandStart())
async def start(message: Message) -> None:
    # markup = await generate_keyboard_kalendar()
    await message.answer("Привет Богам снабжения! Я бот-планировщик задачь, ещё Я умею расскзывать анекдоты", reply_markup=questions)

@router.callback_query(F.data == "kalendar")
async def get_calendar(callback_query: CallbackQuery) -> None:
    """
    Обработка колбэка от кнопки "Календарь"
    """
    markup = await generate_keyboard_kalendar()
    await callback_query.message.answer("Выберите дату", reply_markup=markup)


@router.callback_query(F.data == "add_task")
async def set_description_task(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FormTask.description)
    await callback_query.message.answer(
        text="Введите описание задачи",
        reply_markup=cancel
    )

@router.message(FormTask.description)
async def set_dead_line(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(FormTask.dead_line)
    markup = await generate_keyboard_kalendar()
    await message.answer("Выберит срок выполнения задачи", reply_markup=markup)

@router.callback_query(SimpleCalendarCallback.filter(), StateFilter(FormTask.dead_line))
async def gen_and_set_task(callback_query: CallbackQuery, state: FSMContext, callback_data: SimpleCalendarCallback) -> None:
    
    try:
        # Устанавливаем локаль для календаря
        calendar = SimpleCalendar(locale="ru_RU.UTF-8")
        selected, date = await calendar.process_selection(callback_query, callback_data)

        if selected:
            dead_line = date.strftime('%Y-%m-%d')
            dead_line_date = datetime.strptime(dead_line, '%Y-%m-%d').date()
            task_data = await state.get_data()
            description = task_data.get("description", "")
            task = Tasks(description=description, dead_line=dead_line_date)
            await add_task(task)
            await state.clear()
            await callback_query.message.answer(f"Задача добавлена")

    except locale.Error:
        # Обработка ошибки локали
        await callback_query.message.answer("Ошибка: Локаль не поддерживается на сервере!")



@router.callback_query(SimpleCalendarCallback.filter())
async def process_calendar_callback(callback_query: CallbackQuery, callback_data: SimpleCalendarCallback) -> None:
    """
    Обработка колбэков от SimpleCalendar с русской локалью.
    При выводе даты, выводить задачи по указанной дате
    """
    try:
        # Устанавливаем локаль для календаря
        calendar = SimpleCalendar(locale="ru_RU.UTF-8")
        selected, date = await calendar.process_selection(callback_query, callback_data)

        if selected:
            # Если пользователь выбрал дату
            await callback_query.message.answer(f"Вы выбрали дату: {date.strftime('%Y-%m-%d')}")

    except locale.Error:
        # Обработка ошибки локали
        await callback_query.message.answer("Ошибка: Локаль не поддерживается на сервере!")


@router.callback_query(F.data == "list_tasks")
async def list_tasks(callback_query: CallbackQuery) -> None:
    """
    Обработка колбэка от кнопки "Список задач"
    """
    result = await get_tasks()
    if not result:
        await callback_query.message.answer("Список задач пуст")
        return
        
    text = "\n".join(
        [f"№{task.id} Описание {task.description}, дата выполнения {task.dead_line.strftime("%d.%m.%Y")}\nСтатус: 'Не выполнено\n" for task in result if not task.is_done]
    )
    await callback_query.message.answer(f"Список не выполненных задач:\n{text}")
    await callback_query.message.answer("Желаете выбрать задачу?", reply_markup=choise_task)

@router.callback_query(F.data == 'YES')
async def button_list_tasks(callback_query: CallbackQuery) -> None:
    """
    Обработка колбэка от кнопки "Да"
    """
    await callback_query.message.answer("Выберите задачу", reply_markup=await tasks_keyboard())


@router.callback_query(F.data.in_(['NO', 'cancel']))
async def button_list_tasks(callback_query: CallbackQuery) -> None:
    """
    Обработка колбэка от кнопки "Нет"
    """
    await callback_query.message.answer("Хорошего дня")
    
@router.callback_query(F.data.startswith("task_"))
async def get_task(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка колбэка от кнопки "Задача"
    """
    try:
        task_id = int(callback.data.split("_")[1])
    except (IndexError, ValueError):
        await callback.message.answer("Ошибка: неверный формат задачи.")
        return

    await state.update_data(id=task_id)
    await state.set_state(UpdateTask.id)
    result = await get_task_on_id(task_id)
    if not result:
        await callback.message.answer("Задача не найдена")
        return
    await callback.message.answer(f"Задача №{result.id} Описание {result.description}, дата выполнения {result.dead_line.strftime('%d.%m.%Y')}")
    await callback.message.answer("Выполнить задачу?", reply_markup=update_task_kb)
    

@router.callback_query(F.data == "UPDATE_YES", StateFilter(UpdateTask.id))
async def update_task_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка колбэка от кнопки "Да" Для перевода задачи в статус "Выполнено"
    """
    task_id = (await state.get_data()).get('id', None)
    if not task_id:
        await callback.message.answer("Ошибка: неверный формат задачи.")
        return
        
    await update_task(task_id)
    await callback.message.answer("Задача выполнена")
    await callback.message.answer("Желаете выбрать задачу?", reply_markup=choise_task)
    await state.clear()


@router.message(Command('joke'))
async def get_joke(message: Message) -> None:
    await message.answer(f'{await chose_joke()}')


@router.message(Command('help'))
async def help(message: Message) -> None:
    commands = '\n'.join(f'{command[0]} - {command[1]}' for command in BOT_COMMANDS)
    await message.answer(f'Список команд:\n{commands}')