from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel
from fastapi import Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from app.routers import items, itemsDb

from sqlmodel import SQLModel, Field, select
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from app.models.item import Item


DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables, stash factories on app.state, etc.
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    app.state.engine = engine
    app.state.SessionLocal = SessionLocal
    try:
        yield
    finally:
        # Shutdown: close engine connections
        await engine.dispose()

app = FastAPI(title="Items API", version="0.1.0", lifespan=lifespan)

app.include_router(items.router)
app.include_router(itemsDb.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")  # optional root route for quick check
def root():
    return {"ok": True}

@app.get("/health")
def health():
    return {"ok": True}

def require_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != "secret":
        raise HTTPException(401, "Unauthorized")

@app.get("/secure", dependencies=[Depends(require_api_key)])
def secure():
    return {"message": "ok"}



