from collections.abc import Callable
from typing import List, TypeVar, AsyncGenerator, Any, Awaitable

T = TypeVar("T")


async def paginated_get_all(
    request: Callable[[str, List[str], int, int], Awaitable[List[T]]],
    *args: Any,
    hits=100,
    **kwargs: Any,
) -> List[T]:
    """
    Returns all entries of a paginated endpoint.

    :param request: Paginated endpoint request
    :param where: RSQL QUERY (e.g. "id==90").
    :param sorts: List of field names to sort by.
    :param offset: Number of records to skip before returning data.
    :param hits: Number of records to return.
    :return: List of entries of the endpoint.
    :raises aiohttp.ClientResponseError: If the request fails.
    """
    output: List[T] = []
    while result := await request(*args, **kwargs, hits=hits, offset=len(output)):  # type: ignore
        output += result

    return output


async def paginated_iter(
    request: Callable[[str, List[str], int, int], Awaitable[List[T]]],
    *args: Any,
    hits=100,
    **kwargs: Any,
) -> AsyncGenerator[T, None]:
    """
    Returns a generator over all entries of a paginated endpoint. Generator only loads the next page if the previous page was processed.

    :param request: Paginated endpoint request
    :param where: RSQL QUERY (e.g. "id==90").
    :param sorts: List of field names to sort by.
    :param offset: Number of records to skip before returning data.
    :param hits: Number of records to return.
    :return: Generator over all entries of a paginated endpoint.
    :raises aiohttp.ClientResponseError: If the request fails.
    """
    offset = 0
    while result := await request(*args, **kwargs, hits=hits, offset=offset):  # type: ignore
        offset += len(result)
        for x in result:
            yield x
