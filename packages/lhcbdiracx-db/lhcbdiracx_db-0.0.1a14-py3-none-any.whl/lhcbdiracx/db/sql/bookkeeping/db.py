from __future__ import annotations

from typing import cast

from diracx.db.sql.utils import BaseSQLDB
from sqlalchemy import func, select

from .schema import Base as BookkeepingDBBase
from .schema import Configuration


class BookkeepingDB(BaseSQLDB):
    # This needs to be here for the BaseSQLDB to create the engine
    metadata = BookkeepingDBBase.metadata

    async def hello(self) -> int:

        query = select(func.count()).select_from(Configuration.__table__)
        result = await self.conn.execute(query)
        return cast(int, result.scalar())
