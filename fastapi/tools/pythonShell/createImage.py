from tools.pythonShell.models import CommandRequest
from tools.models import CommandResponse
from io import BytesIO
import os
import uuid
from tools.pythonShell.PythonREPL import PythonREPL
from constants import IMAGE_DIR
from tools.urlBuilder import urlFor, staticURL


def execute_command(command: CommandRequest, seaborn_config=None):
    repl = PythonREPL()
    repl.globals.update(
        {"matplotlib": __import__("matplotlib"), "seaborn": __import__("seaborn")}
    )

    if seaborn_config:
        output, plot_image = repl.run(command.code, seaborn_config)
    else:
        output, plot_image = repl.run(command.code)
    if output == "The provided code is not safe to execute.":
        return CommandResponse(output=output, imageURL=staticURL("warning.png"))

    if plot_image:
        buffered = BytesIO()
        plot_image.save(buffered, format="PNG")
        id = str(uuid.uuid4())
        diagramDirectory = command.method.value
        path = os.getcwd() + f"/{IMAGE_DIR}/{diagramDirectory}"

        if not os.path.exists(path):
            os.makedirs(path)

        plot_image.save(f"{path}/{id}.png")
        return CommandResponse(
            output="Image Generated", imageURL=urlFor(f"{diagramDirectory}/{id}.png")
        )
    else:
        return CommandResponse(
            output=f"error: {output}, fix the code and try again",
            imageURL=staticURL("invalid.png"),
        )
