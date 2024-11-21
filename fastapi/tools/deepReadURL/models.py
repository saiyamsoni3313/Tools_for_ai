from typing import List
from pydantic import BaseModel


class INFO(BaseModel):
    title: str
    body: str
    links: List[str]
    images: List[str]


class DeepResponse(BaseModel):
    urls: List[str]
    info: List[INFO]


class DeepReadURL(BaseModel):
    url: str
    limit: int = 10
    summarize: bool = False
    entities: str = None

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://en.wikipedia.org/wiki/Adolf_Hitler",
                "limit": 10,
            }
        }
