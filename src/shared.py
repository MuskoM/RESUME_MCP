from collections.abc import Iterable
from dataclasses import dataclass
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
class Offer:
    language: ProgrammingLanguage
    seniority: Seniority
    body: str
    tags: Iterable[str]
