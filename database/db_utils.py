from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Date, Integer, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import false
from database.config import DATA_BASE_URL


engine = create_async_engine(DATA_BASE_URL, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    dead_line = Column(Date)
    is_done = Column(Boolean, default=False, server_default=false())
    

def connections(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper
    
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        

if __name__ == '__main__':
    task = Tasks(description='test', dead_line='2021-01-01')




