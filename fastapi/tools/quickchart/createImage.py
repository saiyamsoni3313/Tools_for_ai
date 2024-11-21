import os
import requests
import uuid
from constants import IMAGE_DIR
from tools.quickchart.models import QuickChartRequest
from tools.models import CommandResponse
from tools.urlBuilder import urlFor, staticURL


def createQuickCharts(data: QuickChartRequest) -> CommandResponse:
    try:
        response = requests.get(
            "https://quickchart.io/chart",
            params={
                "backgroundColor": data.backgroundColor,
                "width": data.width,
                "height": data.height,
                "devicePixelRatio": 2.0,
                "format": "png",
                "chart": data.chart,
            },
        )
        if response.status_code == 200:
            print("Saving Image")

            id = str(uuid.uuid4())
            path = os.getcwd() + f"/{IMAGE_DIR}"

            if not os.path.exists(path):
                os.makedirs(path)

            with open(f"{path}/{id}.png", "wb") as f:
                f.write(response.content)

            return CommandResponse(
                output="Image Generated",
                imageURL=urlFor(f"{id}.png"),
            )
    except:
        return CommandResponse(
            output=f"Error generating wordcloud",
            imageURL=staticURL("invalid.png"),
        )
