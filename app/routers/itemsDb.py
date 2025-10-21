from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Path, Header, Depends
from pydantic import BaseModel



from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, List

from fastapi import FastAPI, Depends, HTTPException, Query, Path, Request
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, select
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.item import Item

# --- DB models ---------------------------------------------------------------

router = APIRouter(prefix="/itemsDb", tags=["itemsDb"])


# --- Dependency: get async session from app.state ----------------------------

async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = request.app.state.SessionLocal  # from lifespan
    async with SessionLocal() as session:
        yield session

# --- Schemas (optional, for strict input/output) -----------------------------

class ItemIn(BaseModel):
    name: str
    price: float
    tags: List[str] = []

class ItemOut(ItemIn):
    id: int

# --- Routes ------------------------------------------------------------------

@router.get("/health")
async def health():
    return {"ok": True}

@router.post("", response_model=ItemOut, status_code=201)
async def create_item(payload: ItemIn, session: AsyncSession = Depends(get_session)):
    item = Item(**payload.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item

@router.get("/{item_id}", response_model=ItemOut)
async def get_item(item_id: int = Path(..., ge=1), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Item).where(Item.id == item_id))
    item = res.scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Not found")
    return item

@router.get("", response_model=list[ItemOut])
async def list_items(tag: Optional[str] = Query(None, min_length=1), session: AsyncSession = Depends(get_session)):
    stmt = select(Item)
    if tag:
        # simple filter in Python after fetch; for large data, use JSON functions by DB
        res = await session.execute(stmt)
        items = list(res.scalars())
        return [i for i in items if tag in (i.tags or [])]
    res = await session.execute(stmt)
    return list(res.scalars())
