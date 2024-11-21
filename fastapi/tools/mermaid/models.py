from pydantic import BaseModel


class Mermaid(BaseModel):
    mermaidText: str

    class Config:
        json_schema_extra = {
            "example": {
                "mermaidText": "flowchart TD\n    A[Christmas] -->|Get money| B(Go shopping)\n    B --> C{Let me think}\n    C -->|One| D[Laptop]\n    C -->|Two| E[iPhone]\n    C -->|Three| F[fa:fa-car Car]"
            }
        }
