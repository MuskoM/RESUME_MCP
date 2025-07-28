from abc import ABC, abstractmethod
from typing import Self
from urllib import parse


class IUrlBuilder(ABC):
    ALLOWED_SCHEMAS = ("http", "https")

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.url = self.base_url
        super().__init__()

    @abstractmethod
    def build(self) -> Self:
        url = parse.urlparse(self.url)
        if not url.hostname:
            raise ValueError("Unable to find correct hostname")
        if url.scheme not in self.ALLOWED_SCHEMAS:
            raise ValueError("Only http(s) urls are allowed")
        return self

    @abstractmethod
    def parse_query(self, ) -> None:
        pass


class BulldogJobUrlBuilder(IUrlBuilder):
    def build(self) -> Self:
        return super().build()

    def parse_query(self) -> None:
        
