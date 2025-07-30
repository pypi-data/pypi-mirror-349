from __future__ import annotations

from lhcbdiracx.db.sql import BookkeepingDB


async def hello_world(
    bookkeeping_db: BookkeepingDB,
):
    return await bookkeeping_db.hello()
