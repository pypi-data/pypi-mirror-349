from typing import Protocol

from obspec import GetRangeAsync, GetRangesAsync


class AsyncCloudOptimizedGeoTiffReader(GetRangeAsync, GetRangesAsync, Protocol):
    """Necessary methods to asynchronously read a Cloud-Optimized GeoTIFF file."""


async def read_cog_header(backend: AsyncCloudOptimizedGeoTiffReader, path: str):
    # Make request for first 32KB of file
    header_bytes = await backend.get_range_async(path, start=0, end=32 * 1024)

    # TODO: parse information from header
    raise NotImplementedError


async def read_cog_image(backend: AsyncCloudOptimizedGeoTiffReader, path: str):
    header = await read_cog_header(backend, path)

    # TODO: read image data from file.
