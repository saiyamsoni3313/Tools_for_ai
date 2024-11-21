from pydantic import BaseModel
from typing import List


class ContentURL(BaseModel):
    urls: List[str]
    content: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "urls": [
                    "https://en.wikipedia.org/wiki/Adolf_Hitler",
                    "https://en.wikipedia.org/wiki/Adolf_Hitler",
                ],
                "content": ["Hello World", "Hello World"],
            }
        }


class ReadURL(BaseModel):
    urls: List[str]
    summarize: bool = False
    entities: str = None

    class Config:
        json_schema_extra = {
            "example": {
                "url": [
                    "https://en.wikipedia.org/wiki/Adolf_Hitler",
                    "https://en.wikipedia.org/wiki/Adolf_Hitler",
                ]
            }
        }
