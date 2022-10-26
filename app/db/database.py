from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(BASE_DIR, "secrets.json")
secrets = json.loads(open(SECRET_FILE).read())
DB = secrets["DB"]

# DB_URL = f"mysql+asyncmy://{DB['user']}:{DB['password']}@host.docker.internal:{DB['port']}/{DB['database']}?charset=utf8" # 도커용
DB_URL = f"mysql+asyncmy://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset=utf8" # <-- 네이티브용
engine = create_async_engine(DB_URL, encoding="utf-8")

async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session

def init():
    Base.metadata.create_all(bind=engine)
