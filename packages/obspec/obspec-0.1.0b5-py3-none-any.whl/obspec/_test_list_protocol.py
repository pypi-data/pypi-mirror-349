from __future__ import annotations

from collections.abc import Sequence
from typing import Generic, Protocol, Self, TypedDict, TypeVar

from ._meta import ObjectMeta


ListChunkType_co = TypeVar(
    "ListChunkType_co",
    covariant=True,
)
"""The data structure used for holding list results.

By default, listing APIs return a `list` of [`ObjectMeta`][obspec.ObjectMeta]. However
for improved performance when listing large buckets, you can pass `return_arrow=True`.
Then an Arrow `RecordBatch` will be returned instead.
"""


class ListResult(TypedDict, Generic[ListChunkType_co]):
    """Result of a `list_with_delimiter` call.

    Includes objects, prefixes (directories) and a token for the next set of results.
    Individual result sets may be limited to 1,000 objects based on the underlying
    object storage's limitations.
    """

    common_prefixes: Sequence[str]
    """Prefixes that are common (like directories)"""

    objects: ListChunkType_co
    """Object metadata for the listing"""


class ListIterator(Protocol[ListChunkType_co]):
    """A stream of [ObjectMeta][obspec.ObjectMeta] that can be polled synchronously."""

    def __iter__(self) -> Self:
        """Return `Self` as an async iterator."""
        ...

    def collect(self) -> ListChunkType_co:
        """Collect all remaining ObjectMeta objects in the stream.

        This ignores the `chunk_size` parameter from the `list` call and collects all
        remaining data into a single chunk.
        """
        ...

    def __next__(self) -> ListChunkType_co:
        """Return the next chunk of ObjectMeta in the stream."""
        ...


class ListStream(Protocol[ListChunkType_co]):
    """A stream of [ObjectMeta][obspec.ObjectMeta] that can be polled asynchronously."""

    def __aiter__(self) -> Self:
        """Return `Self` as an async iterator."""
        ...

    async def collect_async(self) -> ListChunkType_co:
        """Collect all remaining ObjectMeta objects in the stream.

        This ignores the `chunk_size` parameter from the `list` call and collects all
        remaining data into a single chunk.
        """
        ...

    async def __anext__(self) -> ListChunkType_co:
        """Return the next chunk of ObjectMeta in the stream."""
        ...


class List(Protocol):
    def list(
        self,
        prefix: str | None = None,
        *,
        offset: str | None = None,
        chunk_size: int = 50,
    ) -> ListIterator[Sequence[ObjectMeta]]: ...


class ListAsync(Protocol):
    def list_async(
        self,
        prefix: str | None = None,
        *,
        offset: str | None = None,
        chunk_size: int = 50,
    ) -> ListStream[Sequence[ObjectMeta]]: ...


class ListWithDelimiter(Protocol):
    def list_with_delimiter(
        self,
        prefix: str | None = None,
    ) -> ListResult[Sequence[ObjectMeta]]: ...


class ListWithDelimiterAsync(Protocol):
    async def list_with_delimiter_async(
        self,
        prefix: str | None = None,
    ) -> ListResult[Sequence[ObjectMeta]]:
        """Call `list_with_delimiter` asynchronously.

        Refer to the documentation for
        [ListWithDelimiter][obspec.ListWithDelimiter].
        """
        ...
