import requests
import uuid
import os
from constants import IMAGE_DIR
from langchain_community.document_loaders import PyPDFLoader


def download_pdf_if_appropriate(url):
    """Download the PDF from a URL if the content type is appropriate."""
    id = str(uuid.uuid4())
    path = os.getcwd() + f"/{IMAGE_DIR}"

    if not os.path.exists(path):
        os.makedirs(path)

    destination = f"{path}/{id}.pdf"
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Check for HTTP errors

            # Check if the Content-Type header indicates a PDF
            content_type = response.headers.get("Content-Type", "")
            if "application/pdf" in content_type:
                print("The content is a PDF. Starting download...")
                with open(destination, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print("Download successful.")
                loader = PyPDFLoader(destination)
                docs = loader.load_and_split()
                response = ""
                for doc in docs:
                    response += doc.page_content
                return response

            else:
                return None
    except requests.RequestException as e:
        print(f"Failed to download the file: {e}")
        return None
