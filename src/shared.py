from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class ProgrammingLanguage(StrEnum):
    python = "Python"
    java = "Python"


class Seniority(StrEnum):
    senior = "Senior"
    junior = "Junior"
    regular = "Regular"
    lead = "Lead"


@dataclass
class Criteria:
    include: Iterable[str] = field(default_factory=list)
    exclude: Iterable[str] = field(default_factory=list)


@dataclass
class Offer:
    language: ProgrammingLanguage
    name: str
    tags: Iterable[str]
    url: str
    seniority: Seniority = field(init=False)
    scraped_on: datetime = field(init=False, default_factory=datetime.now)

    def __post_init__(self):
        for seniority_level, enum_member in Seniority.__members__.items():
            if seniority_level.lower() in self.name.lower():
                self.seniority = enum_member
        self.seniority = Seniority.regular

    def __str__(self) -> str:
        return f"""### [{self.name}]({self.url})
        ---
        Seniority: {self.seniority}
        Tags: {list(self.tags)}
        Language: {self.language}
        Scraped on: {self.scraped_on}
        """

    def __repr__(self) -> str:
        return f"{self.name} on {self.url}"
