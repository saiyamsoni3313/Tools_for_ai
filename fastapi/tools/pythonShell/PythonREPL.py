import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import io
import re
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from contextlib import redirect_stdout
from typing import Dict, Optional, Tuple, Any

from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Restricted environment
RESTRICTED_PATTERNS = [
    r"(__import__|open|exec|eval|multiprocessing|compile|globals|locals|getattr|setattr|delattr|vars|input)",
    r"(import subprocess|import os|import sys|import file|import io|import shutil)",
    r"system\(|popen\(",
]
SAFE_MODULES = ["matplotlib.pyplot", "seaborn"]


class PythonREPL(BaseModel):
    """
    A class that simulates a standalone Python REPL with restricted execution
    environment for safe execution of arbitrary Python code, particularly for plotting.
    """

    globals: Dict = Field(default_factory=dict, alias="_globals")
    locals: Dict = Field(default_factory=dict, alias="_locals")

    @classmethod
    def is_code_safe(cls, code: str) -> bool:
        """
        Check if the code contains potentially dangerous patterns.
        :param code: A string of code to be checked.
        :return: True if the code does not contain dangerous patterns.
        """
        for pattern in RESTRICTED_PATTERNS:
            if re.search(pattern, code):
                logger.warning(f"Potentially unsafe code detected: {code}")
                return False
        return True

    @classmethod
    def execute_code(
        cls,
        command: str,
        safe_modules: Dict[str, str],
        seaborn_config: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, Optional[Image.Image]]:
        """
        Execute the given command within a safe and restricted environment.
        Handles the capturing and returning of both textual output and generated plots.
        :param command: Command string to execute.
        :param safe_modules: Dictionary of safe modules to import and use.
        :return: Tuple containing the text output and an image of the plot, if generated.
        """
        with io.StringIO() as buf, redirect_stdout(buf):
            try:
                # Set default figure size
                plt.figure(figsize=(10, 6))

                # Apply Seaborn configuration
                if seaborn_config:
                    sns.set(**seaborn_config)

                # Dynamically import safe modules
                safe_globals = {
                    name: __import__(module) for name, module in safe_modules.items()
                }
                exec(command, safe_globals)

                # Handle plot capturing
                buffer = io.BytesIO()
                plt.gcf().savefig(buffer, format="png")
                buffer.seek(0)
                img = Image.open(buffer)

                # Clear the current figure to avoid overlap in future runs
                plt.clf()

                return buf.getvalue(), img
            except Exception as e:
                logger.error(f"Error during code execution: {e}")
                return str(e), None

    def run(
        self,
        command: str,
        seaborn_config: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, Optional[Image.Image]]:
        """
        Run the given command string with a timeout option.
        :param command: The command string to execute.
        :param timeout: Optional timeout for the execution in seconds.
        :return: Tuple containing the output string and an image of the plot, if any.
        """
        if not self.is_code_safe(command):
            error_message = "The provided code is not safe to execute."
            logger.error(error_message)
            return error_message, None

        safe_modules = {name: name for name in SAFE_MODULES}

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                self.execute_code, command, safe_modules, seaborn_config
            )
            try:
                return future.result(timeout=10)
            except TimeoutError:
                logger.warning("Code execution timed out")
                return "Execution timed out", None
