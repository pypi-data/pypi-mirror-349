from collections.abc import Callable
from http.cookies import SimpleCookie
from typing import Dict, Any, Optional, TypeVar, Union, Sequence

from aiohttp import ClientSession, CookieJar
from aiohttp.client import _BaseRequestContextManager
from pydantic import BaseModel, TypeAdapter

from o2a_registry.rate_limiter import RateLimiter


class RestAdapter:
    def __init__(self, hostname: str, ssl: bool) -> None:
        prefix = "https" if ssl else "http"
        self._url = f"{prefix}://{hostname}/rest/v2/"
        self._ssl = ssl
        self._rate_limiter = RateLimiter(100)
        self._cookie: Optional[SimpleCookie] = None

        self._session: Optional[ClientSession] = None

    async def _get_session(self) -> ClientSession:
        """
        Returns a valid client session. This is necessary, since in the init, it is not guaranteed, that the event loop exists yet. Therefore, the session is created dynamically in the calls themselves.
        :return: A valid client session
        """
        if self._session is None:
            self._session = self._create_session()

        return self._session

    def _create_session(self) -> ClientSession:
        cookie_jar: Optional[CookieJar] = None
        if not self._ssl:
            cookie_jar = CookieJar(treat_as_secure_origin=self._url)

        return ClientSession(json_serialize=_json_serialize, cookie_jar=cookie_jar)

    async def login(self, endpoint: str, username: str, password: str) -> None:
        request_path = self._url + endpoint

        await self._rate_limiter(
            self._session_login(
                request_path, {"username": username, "password": password}
            )
        )

    async def _session_login(self, url: str, data: Dict[str, str]) -> None:
        session = await self._get_session()
        async with session.post(url, ssl=self._ssl, data=data) as response:
            response.raise_for_status()
            self._cookie = response.cookies

    async def get(
        self, endpoint: str, ep_params: Optional[Dict[str, Any]] = None
    ) -> str:
        session = await self._get_session()
        return await self._rate_limiter(
            self._execute(session.get, endpoint, {"params": ep_params})
        )

    async def post(
        self,
        endpoint: str,
        data: Optional[
            Union[BaseModel, Sequence[BaseModel | int | str | float | bool]]
        ] = None,
    ) -> str:
        session = await self._get_session()
        return await self._rate_limiter(
            self._execute(session.post, endpoint, {"json": data})
        )

    async def put(
        self,
        endpoint: str,
        data: Optional[
            Union[BaseModel, Sequence[BaseModel | int | str | float | bool]]
        ] = None,
    ) -> str:
        session = await self._get_session()
        return await self._rate_limiter(
            self._execute(session.put, endpoint, {"json": data})
        )

    async def delete(self, endpoint: str) -> str:
        session = await self._get_session()
        return await self._rate_limiter(self._execute(session.delete, endpoint, {}))

    async def _execute(
        self,
        session_command: Callable[..., _BaseRequestContextManager],
        endpoint: str,
        kwargs: Dict[str, Any],
    ) -> str:
        request_path = self._url + endpoint
        async with session_command(
            request_path, ssl=self._ssl, cookies=self._cookie, **kwargs
        ) as response:
            response.raise_for_status()
            return await response.text()

    async def close(self):
        if self._session is not None:
            await self._session.close()


T = TypeVar("T")


def _json_serialize(
    item: Union[BaseModel, Sequence[BaseModel | int | str | float | bool], None],
) -> str:
    if item is None:
        return ""

    if isinstance(item, BaseModel):
        return item.model_dump_json(by_alias=True)

    type_adapter = TypeAdapter(type(item))
    return type_adapter.dump_json(item, by_alias=True).decode("utf-8")
