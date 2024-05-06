from typing import Any
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, WareHouseItems, WareHouseAddItems, WareHousePublic, WareHouseItemsPublic, WareHouseItemsUpdate

router = APIRouter()


@router.get("/", response_model=WareHouseItemsPublic)
def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """
    count_statement = select(func.count()).select_from(WareHouseItems)
    count = session.exec(count_statement).one()

    statement = select(WareHouseItems).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return WareHouseItemsPublic(data=users, count=count)



@router.post("/{item_id}", response_model=WareHousePublic)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: WareHouseAddItems, item_id: int) -> Any:
    """
    Create new item.
    """
    item = WareHouseItems.model_validate(item_in, update = { "item_id": item_id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.put("/", response_model=WareHouseItemsPublic)
def update_item(
    *, session: SessionDep, current_user: CurrentUser, wh_id: int, item_in: WareHouseItemsUpdate
) -> Any:
    """
    Update an item.
    """
    wh_item = session.get(WareHouseItems, wh_id)
    #wh_item = session.exec(WareHouseItems).filter_by(item_id=id).first()
    print("-------Up-----", wh_item)
    if not wh_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (wh_item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = item_in.model_dump(exclude_unset=True)
    wh_item.sqlmodel_update(update_dict)
    session.add(wh_item)
    session.commit()
    session.refresh(wh_item)
    return wh_item