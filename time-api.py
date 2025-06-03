#setting up s simple server


from fastapi import FastAPI # type: ignore
from fastapi import FastAPI # type: ignore
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession # type: ignore
from sqlalchemy.orm import sessionmaker, declarative_base # type: ignore
from sqlalchemy import Column, Integer, DateTime # type: ignore
from datetime import datetime, timezone
import time
import os
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL")

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
    return {"Message": "Hello world, FastAPI with Docker compose and PostgreSQL"}

@app.get("/visits")
async def get_visits():
    async with SessionLocal() as session:
        result = await session.execute(Visit.__table__.select().order_by(Visit.accessed_at.desc()))
        visits = result.fetchall()
        return [{"id": row.id, "accessed_at": row.accessed_at.isoformat()} for row in visits]

@app.get("/time")
def read_time():
    time_in_seconds = time.time()
    current_time = time.ctime(time_in_seconds)
    return {"current date and time": current_time}
