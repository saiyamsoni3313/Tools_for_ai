import io
import os
from PIL import Image
from plantuml import PlantUML
import uuid
from constants import IMAGE_DIR
from tools.models import CommandResponse
from tools.urlBuilder import urlFor, staticURL


def createPlantUML(plantumlText):
    try:
        # create a server object to call for your computations
        print("Calling PlantUML Server")
        server = PlantUML(
            url="https://www.plantuml.com/plantuml/img/",
            basic_auth={},
            form_auth={},
            http_opts={},
            request_opts={},
        )

        # Send and compile your diagram files to/with the PlantUML server
        rawImage = server.processes(plantumlText)
        imageStream = io.BytesIO(rawImage)
        imageFile = Image.open(imageStream)

        print("Saving Image")
        id = str(uuid.uuid4())
        path = os.getcwd() + f"/{IMAGE_DIR}/"

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
