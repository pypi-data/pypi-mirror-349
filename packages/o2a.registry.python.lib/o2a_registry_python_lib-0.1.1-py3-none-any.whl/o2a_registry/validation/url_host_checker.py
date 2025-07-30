from typing import Annotated

from pydantic import HttpUrl, AfterValidator


class UrlHostChecker:
    def __init__(self, host: str) -> None:
        self._host = host

    def __call__(self, url: HttpUrl) -> HttpUrl:
        if url.host != self._host:
            raise ValueError(f"URL must be for host {self._host}")

        return url


ORCID_URL = Annotated[HttpUrl, AfterValidator(UrlHostChecker("orcid.org"))]
ROR_URL = Annotated[HttpUrl, AfterValidator(UrlHostChecker("ror.org"))]
