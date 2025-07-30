from typing import Optional, List


def resolve_query_parameters(
    where: Optional[str] = None,
    sorts: Optional[List[str]] = None,
    offset: Optional[int] = None,
    hits: Optional[int] = None,
) -> str:
    parameters = []
    if where is not None:
        parameters.append(_resolve_where(where))

    if sorts is not None:
        parameters += [_resolve_sorts(sort) for sort in sorts]

    if offset is not None:
        parameters.append(_resolve_offset(offset))

    if hits is not None:
        parameters.append(_resolve_hits(hits))

    return "?" + "&".join(parameters)


def _resolve_where(where: str) -> str:
    cleaned_where = where.replace("=", "%3D").replace("!", "%21")
    return f"where={cleaned_where}"


def _resolve_sorts(sorts: str) -> str:
    return f"sorts={sorts}"


def _resolve_offset(offset: int) -> str:
    return f"offset={offset}"


def _resolve_hits(hits: int) -> str:
    return f"hits={hits}"
