from __future__ import annotations

import asyncio
from typing import Protocol

from obspec import DeleteAsync, ListWithDelimiterAsync


class DeletePrefixAsyncInput(ListWithDelimiterAsync, DeleteAsync, Protocol): ...


async def delete_prefix(client: DeletePrefixAsyncInput, prefix: str | None = None):
    items = await client.list_with_delimiter_async(prefix)
    paths = [x["path"] for x in items["objects"]]
    futures = [client.delete_async(path) for path in paths]
    await asyncio.gather(*futures)
