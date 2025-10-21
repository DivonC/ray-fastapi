from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Path, Header, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])

class ItemIn(BaseModel):
    name: str
    price: float
    tags: List[str] = []

class ItemOut(ItemIn):
    id: int

DB: dict[int, ItemOut] = {}
_next_id = 1

@router.post("", response_model=ItemOut, status_code=201)
def create_item(item: ItemIn):
    global _next_id
    new = ItemOut(id=_next_id, **item.model_dump())
    DB[_next_id] = new
    _next_id += 1
    return new

@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int = Path(..., ge=1)):
    if item_id not in DB:
        raise HTTPException(404, "Not found")
    return DB[item_id]

@router.get("", response_model=list[ItemOut])
def list_items(tag: Optional[str] = Query(None, min_length=1)):
    items = list(DB.values())
    return [i for i in items if not tag or tag in i.tags]

def require_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != "secret":
        raise HTTPException(401, "Unauthorized")

# This will be /items/secure because of the router prefix
@router.get("/secure", dependencies=[Depends(require_api_key)])
def secure():
    return {"message": "ok"}


