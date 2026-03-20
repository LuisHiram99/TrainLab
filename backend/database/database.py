from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine
from config import Settings

settings = Settings()
DATABASE_URL = settings.DATABASE_URL.get_secret_value()

engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        try: 
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:            
            await session.close()