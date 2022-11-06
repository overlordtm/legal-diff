# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from dataclasses_json import DataClassJsonMixin

class LawKind(str, Enum):
  LAW = "LAW"
  REGULATION = "REGULATION"

@dataclass
class ParagraphItem(DataClassJsonMixin):
    content: str = field(default_factory=str)

@dataclass
class ArticleItem(DataClassJsonMixin):
    title: str
    children: list[ParagraphItem]

@dataclass
class ChapterItem(DataClassJsonMixin):
    title: str
    articles: list[ArticleItem]

@dataclass
class LawItem(DataClassJsonMixin):
    title: str = field(default_factory=str)
    kind: LawKind = field(default_factory=LawKind)
    url: str = field(default_factory=str)
    code: str = field(default_factory=str)
    preamble: list[ParagraphItem] = field(default_factory=list)
    chapters: list[ChapterItem] = field(default_factory=list)
    # preamble: str = field(default_factory=str)
    # childrens: list[ArticleItem] = field(default_factory=list)