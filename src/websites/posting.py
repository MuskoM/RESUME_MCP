import logging
from abc import ABC
from collections.abc import Iterable
from typing import Protocol

import httpx

from exceptions import HTTPServerError
from parsers import ScrapyParser
from shared import Criteria, Offer, ProgrammingLanguage

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.128 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


class IPostingWebsite(Protocol):
    async def list_offers_for(
        self, language: ProgrammingLanguage, criteria: Criteria
    ) -> Iterable: ...

    async def get_offer(self) -> Offer: ...


class PostingWebsite(IPostingWebsite, ABC):
    def __init__(self, base_url: str) -> None:
        logging.info(f"Initializing PostingWebsite with base URL: {base_url}")
        self.base_url = base_url
        self.host = ""
        self.headers = {}

        with httpx.Client(headers=BROWSER_HEADERS) as client:
            try:
                website_metadata = client.head(self.base_url)
                website_metadata.raise_for_status()
                self.headers = website_metadata.headers
                self.website_host = website_metadata.url.host
                logging.info(f"Successfully fetched metadata for {self.base_url}")
            except httpx.HTTPStatusError as ex:
                logging.error(
                    f"Failed to fetch metadata for {self.base_url}", exc_info=ex
                )
                raise HTTPServerError(
                    "Unable to fetch metadata. Website unavailable?"
                ) from ex

    async def list_offers_for(
        self, language: ProgrammingLanguage, criteria: Criteria
    ) -> Iterable:
        raise NotImplementedError("Function not implemented in abstract class")

    async def get_offer(self) -> Offer:
        raise NotImplementedError("Function not implemented in abstract class")


class GenericPostingWebsite(PostingWebsite):
    def __init__(self, base_url: str) -> None:
        logging.info(f"Initializing GenericPostingWebsite with base URL: {base_url}")
        super().__init__(base_url)

    async def list_offers_for(
        self, language: ProgrammingLanguage, criteria: Criteria
    ) -> Iterable:
        logging.warning("list_offers_for is not implemented for GenericPostingWebsite")
        raise NotImplementedError("Unable to list offers for generic Posting Website")


class BulldogJob(PostingWebsite):
    def __init__(self) -> None:
        logging.info("Initializing BulldogJob")
        base_url = "https://bulldogjob.pl"
        super().__init__(base_url)

    async def list_offers_for(
        self, language: ProgrammingLanguage, criteria: Criteria
    ) -> Iterable[Offer]:
        logging.info(f"Fetching offers for language: {language}, criteria: {criteria}")
        posting_page_url = f"{self.base_url}/companies/jobs/s/skills,{language}"
        async with httpx.AsyncClient(
            headers=BROWSER_HEADERS, follow_redirects=True
        ) as client:
            try:
                response = await client.get(posting_page_url)
                response.raise_for_status()
                parser = ScrapyParser(
                    response.text, "//a[contains(@class, 'JobListItem_item')]"
                )
                return parser.extract_offers(
                    link_query="//@href",
                    name_query="//h3/text()",
                    tags_query="//div[contains(@class,'tags')]/span/text()",
                )
            except httpx.HTTPStatusError as ex:
                logging.error(
                    f"Failed to fetch offers from {posting_page_url}", exc_info=ex
                )
                raise HTTPServerError("Unable to fetch offers") from ex
