from fastapi import APIRouter
from apis.v1.toolsAPI import toolsRouter


api_router = APIRouter()
api_router.include_router(toolsRouter, prefix="/api/v1", tags=["tool"])
