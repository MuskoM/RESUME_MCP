from abc import ABC, abstractmethod
from collections.abc import Iterable
import logging
from typing import Protocol, TypeVar

import httpx
from scrapy.selector import Selector


class BaseSelector(ABC):
    @abstractmethod
    def build(self) -> str: ...


class Parser(ABC):
    @abstractmethod
    def get_multiple_entries(self, selector: BaseSelector) -> Iterable[str]: ...

    @abstractmethod
    def get_single_entry(self, selector: BaseSelector) -> str: ...


class ScrapySelector(Selector):
    def __init__(self, xpath: str) -> None:
        self.query = xpath

    def build(self) -> str:
        return self.query


class ScrapyParser(Parser):
    def __init__(self, html_text: str) -> None:
        logging.info(f"PAGE: {html_text}")
        self.page = Selector(text=html_text)

    def get_single_entry(self, selector: ScrapySelector) -> str:
        elements = self.page.xpath(selector.build())
        return elements.get()

    def get_multiple_entries(self, selector: ScrapySelector) -> Iterable[str]:
        elements = self.page.xpath(selector.build())
        return elements.getall()
