from __future__ import annotations

from typing import Generic, Literal, Self, Sequence, TypeVar, overload

from arro3.core import RecordBatch, Table

from obspec import ObjectMeta

from ._test_list_protocol import List


def test_list_arrow_compatible():
    ListChunkType_co = TypeVar("ListChunkType_co", covariant=True)

    class ListIter(Generic[ListChunkType_co]):
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

    class ListIterImpl(ListIter[Sequence[ObjectMeta]]):
        def __iter__(self) -> Self:
            """Return `Self` as an async iterator."""
            ...

        def collect(self) -> Sequence[ObjectMeta]:
            """Collect all remaining ObjectMeta objects in the stream.

            This ignores the `chunk_size` parameter from the `list` call and collects all
            remaining data into a single chunk.
            """
            ...

        def __next__(self) -> Sequence[ObjectMeta]:
            """Return the next chunk of ObjectMeta in the stream."""
            ...

    class ObstoreList:
        @overload
        def list(
            self,
            prefix: str | None = None,
            *,
            offset: str | None = None,
            chunk_size: int = 50,
        ) -> ListIter[Sequence[ObjectMeta]]: ...
        @overload
        def list(
            self,
            prefix: str | None = None,
            *,
            offset: str | None = None,
            chunk_size: int = 50,
            return_arrow: Literal[True],
        ) -> ListIter[RecordBatch]: ...
        @overload
        def list(
            self,
            prefix: str | None = None,
            *,
            offset: str | None = None,
            chunk_size: int = 50,
            return_arrow: Literal[False],
        ) -> ListIter[Sequence[ObjectMeta]]: ...
        @overload
        def list(
            self,
            prefix: str | None = None,
            *,
            offset: str | None = None,
            chunk_size: int = 50,
            return_arrow: bool,
        ) -> ListIter[RecordBatch] | ListIter[Sequence[ObjectMeta]]: ...

        def list(
            self,
            prefix: str | None = None,
            *,
            offset: str | None = None,
            chunk_size: int = 50,
            return_arrow: bool = False,
        ) -> ListIter[RecordBatch] | ListIter[Sequence[ObjectMeta]]:
            return ListIterImpl()

    def accepts_obspec_list(provider: List):
        pass

    accepts_obspec_list(ObstoreList())
