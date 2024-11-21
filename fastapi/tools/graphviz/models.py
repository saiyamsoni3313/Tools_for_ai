from pydantic import BaseModel
from enum import Enum


# Define the enumeration for layout types
class LayoutType(str, Enum):
    dot = "dot"
    fdp = "fdp"
    neato = "neato"
    circo = "circo"
    twopi = "twopi"
    osage = "osage"
    patchwork = "patchwork"


# Define the GraphvizRequest model
class GraphvizRequest(BaseModel):
    graph: str
    layout: LayoutType

    class Config:
        json_schema_extra = {
            "example": {
                "graph": "digraph G { A -> B; B -> C; C -> A; }",
                "layout": "dot",
            }
        }
