from pydantic import BaseModel


class CommandResponse(BaseModel):
    output: str
    imageURL: str

    class Config:
        json_schema_extra = {
            "example": {
                "imageURL": "https://example.com/image.png",
                "output": "Image Generated",
            }
        }
