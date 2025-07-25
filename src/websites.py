from abc import ABC
from collections.abc import Iterable
import logging
from typing import Protocol

import httpx

from exceptions import HTTPServerError
from parsers import ScrapyParser, ScrapySelector
from shared import Offer, ProgrammingLanguage

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.128 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


class IPostingWebsite(Protocol):
    async def list_offers_for(
        self, language: ProgrammingLanguage, criteria: Iterable[str] = []
    ) -> Iterable: ...

    async def get_offer(self) -> Offer: ...


class PostingWebsite(IPostingWebsite, ABC):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.host = ""
        self.headers = {}

        with httpx.Client(headers=BROWSER_HEADERS) as client:
            try:
                website_metadata = client.head(self.base_url)
                website_metadata.raise_for_status()
                self.headers = website_metadata.headers
                self.website_host = website_metadata.url.host
            except httpx.HTTPStatusError as ex:
                raise HTTPServerError(
                    "Unable to fetch metadata. Website unavailable?"
                ) from ex

    async def list_offers_for(
        self, language: ProgrammingLanguage, criteria: Iterable[str] = []
    ) -> Iterable:
        raise NotImplementedError("Function not implemented in abstract class")

    async def get_offer(self) -> Offer:
        raise NotImplementedError("Function not implemented in abstract class")


class GenericPostingWebsite(PostingWebsite):
    def __init__(self, base_url: str) -> None:
        super().__init__(base_url)

    async def list_offers_for(
        self, language: ProgrammingLanguage, criteria: Iterable[str] = []
    ) -> Iterable:
        raise NotImplementedError("Unable to list offers for generic Posting Website")


class BulldogJob(PostingWebsite):
    def __init__(self) -> None:
        base_url = "https://bulldogjob.pl"
        super().__init__(base_url)

    async def list_offers_for(
        self, language: ProgrammingLanguage, criteria: Iterable[str] = []
    ) -> Iterable[str]:
        posting_page_url = f"{self.base_url}/companies/jobs/s/skills,{language}"
        async with httpx.AsyncClient(
            headers=BROWSER_HEADERS, follow_redirects=True
        ) as client:
            response = await client.get(posting_page_url)
            parser = ScrapyParser(response.text)
            selector = ScrapySelector("//h3/text()")
            return parser.get_multiple_entries(selector)
