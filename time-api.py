from fastapi import FastAPI  # type: ignore
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # type: ignore
from sqlalchemy.orm import sessionmaker, declarative_base  # type: ignore
from sqlalchemy import Column, Integer, DateTime, select  # type: ignore
from datetime import datetime, timezone
import time
import os
from contextlib import asynccontextmanager
from urllib.parse import quote_plus

# Build DATABASE_URL from separate env vars
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_port = os.getenv("POSTGRES_PORT", "5432")


if not all([db_user, db_password, db_name]):
    raise ValueError("Missing one or more required environment variables for DB connection.")

DATABASE_URL = (
    f"postgresql+asyncpg://{quote_plus(db_user)}:{quote_plus(db_password)}"
    f"@{db_host}:{db_port}/{db_name}"
)


# Create async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Define a simple Visit model
class Visit(Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True, index=True)
    accessed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: nothing needed here for now

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def index():
    async with SessionLocal() as session:
        new_visit = Visit()
        session.add(new_visit)
        await session.commit()
    return {"Message": "Hello world, FastAPI with Kubernetes"}

@app.get("/visits")
async def get_visits():
    async with SessionLocal() as session:
        result = await session.execute(select(Visit).order_by(Visit.accessed_at.desc()))
        visits = result.scalars().all()
        return [{"id": v.id, "accessed_at": v.accessed_at.isoformat()} for v in visits]

@app.get("/time")
def read_time():
    time_in_seconds = time.time()
    current_time = time.ctime(time_in_seconds)
    return {"current date and time": current_time}
