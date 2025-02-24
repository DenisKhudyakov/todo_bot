
from database.db_utils import Tasks, connections
from sqlalchemy import select


@connections
async def add_task(session, task):
    async with session.begin():
        session.add(task)


@connections      
async def get_task_on_id(session, task_id):
    result = (await session.execute(select(Tasks).filter(Tasks.id == task_id))).scalars().first()
    return result


@connections   
async def get_task(session, date):
    result = await session.execute(select(Tasks).where(Tasks.date == date)).scalars().all()
    return result


@connections
async def update_task(session, task_id):
    task = (await session.execute(select(Tasks).filter(Tasks.id == task_id))).scalars().first()
    print(task)
    if task:
        task.is_done = True
        await session.commit()
        return task
    return None

@connections
async def get_tasks(session):
    result = (await session.execute(select(Tasks))).scalars().all()
    return result
    