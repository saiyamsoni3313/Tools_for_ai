# fastapi library imports
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
import shutil
import os

# Local imports
from constants import URL, IMAGE_DIR

# Import Routes
from apis.base import api_router

# FastAPI Config
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Include routes
app.include_router(api_router)

## Mount static directories
app.mount("/" + IMAGE_DIR, StaticFiles(directory="images"), name="images")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", context={"request": request})


# Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Tools API",
        version="1.0.0",
        description="Multiple APIs to empower AI Agents",
        routes=app.routes,
        servers=[{"url": URL, "description": "Multiple APIs to empower AI Agents"}],
    )
    openapi_schema["info"]["x-logo"] = {"url": URL + "/static/logo.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Function to clean the IMAGE_DIR
def clean_image_dir():
    folder = IMAGE_DIR  # Assuming 'images' is the folder where IMAGE_DIR points to
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


# Set up the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(clean_image_dir, "interval", hours=24)
scheduler.start()
