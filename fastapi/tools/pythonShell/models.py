from pydantic import BaseModel
from enum import Enum


class Method(Enum):
    matplotlib = "matplotlib"
    seaborn = "seaborn"


class CommandRequest(BaseModel):
    code: str
    method: Method

    class Config:
        json_schema_extra = {
            "example": {
                "code": "import matplotlib.pyplot as plt\nimport seaborn as sns\nactivities = ['eat', 'sleep', 'work', 'play']\nslices = [3, 7, 8, 6]\ncolors = ['r', 'y', 'g', 'b']\nplt.pie(slices, labels=activities, colors=colors,\n        startangle=90, shadow=True, explode=(0, 0, 0.1, 0),\n        radius=1.2, autopct='%1.1f%%')\nplt.legend()\nplt.gcf()",
                "method": "seaborn",
            }
        }
