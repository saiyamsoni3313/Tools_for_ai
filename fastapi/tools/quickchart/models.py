from pydantic import BaseModel


# Define the GraphvizRequest model
class QuickChartRequest(BaseModel):
    chart: str
    width: int
    height: int
    backgroundColor: str = "transparent"

    class Config:
        json_schema_extra = {
            "example": {
                "chart": "{'backgroundColor': '#fff', 'width': 500, 'height': 300, 'devicePixelRatio': 1.0, 'chart': {'type': 'bar', 'data': {'labels': [2012, 2013, 2014, 2015, 2016], 'datasets': [{'label': 'Users', 'data': [120, 60, 50, 180, 120]}]}}}",
                "width": 500,
                "height": 300,
                "backgroundColor": "transparent",
            }
        }
