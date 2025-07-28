import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator

from scrapy.selector import Selector

from shared import Offer, ProgrammingLanguage


class Parser(ABC):
    def __init__(self, html_text: str) -> None:
        self._html_text = html_text

    @abstractmethod
    def extract_offers(
        self, link_query: str, name_query: str, tags_query: str
    ) -> Iterator[Offer]: ...


class ScrapyParser(Parser):
    def __init__(self, html_text: str, offer_query: str) -> None:
        super().__init__(html_text)
        self.page = Selector(text=self._html_text)
        self.offers = self.page.xpath(offer_query).getall()

    def extract_offers(
        self, link_query: str, name_query: str, tags_query: str
    ) -> Iterator[Offer]:
        for offer in self.offers:
            yield self.extract_offer_info(offer, link_query, name_query, tags_query)

    def extract_offer_info(
        self, offer_html: str, link_query: str, name_query: str, tags_query: str
    ) -> Offer:
        offer = Selector(text=offer_html)
        return Offer(
            url=offer.xpath(link_query).get(),
            tags=offer.xpath(tags_query).getall(),
            language=ProgrammingLanguage.python,
            name=offer.xpath(name_query).get(),
        )
