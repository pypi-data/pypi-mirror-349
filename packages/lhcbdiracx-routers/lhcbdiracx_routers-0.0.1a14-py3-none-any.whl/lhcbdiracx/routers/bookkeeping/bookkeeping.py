from __future__ import annotations

from typing import Annotated

from diracx.routers.fastapi_classes import DiracxRouter
from fastapi import Depends

from lhcbdiracx.db.sql import BookkeepingDB as _BookkeepingDB
from lhcbdiracx.logic.bookkeeping.bookkeeping import hello_world as hello_world_bl

from .access_policy import ActionType, CheckBookkeepingPolicyCallable

router = DiracxRouter()

# Define the dependency at the top, so you don't have to
# be so verbose in your routes
BookkeepingDB = Annotated[_BookkeepingDB, Depends(_BookkeepingDB.transaction)]


@router.get("/")
async def hello_world(
    bookkeeping_db: BookkeepingDB,
    check_permission: CheckBookkeepingPolicyCallable,
):
    await check_permission(action=ActionType.HELLO)
    return await hello_world_bl(bookkeeping_db)
