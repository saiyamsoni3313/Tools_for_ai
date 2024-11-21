from PIL import Image
import base64
import os
import io
import requests
import uuid
from constants import IMAGE_DIR
from tools.models import CommandResponse
from tools.urlBuilder import urlFor, staticURL


def createMermaidDiagram(mermaidGraph):
    try:
        graphbytes = mermaidGraph.encode("ascii")

        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")

        rawImage = requests.get("https://mermaid.ink/img/" + base64_string).content
        imageFile = Image.open(io.BytesIO(rawImage))

        print("Saving Image")

        id = str(uuid.uuid4())
        path = os.getcwd() + f"/{IMAGE_DIR}"

        if not os.path.exists(path):
            os.makedirs(path)

        imageFile.save(f"{path}/{id}.png")
        return CommandResponse(
            output="Image Generated",
            imageURL=urlFor(f"{id}.png"),
        )

    except:
        return CommandResponse(
            output=f"error: fix the code and try again",
            imageURL=staticURL("invalid.png"),
        )
