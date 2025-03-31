from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.module_manager import (
    create_module,
    list_modules,
    get_module_code,
    update_module_code,
    deactivate_module,
)
import os

router = APIRouter()

BASE_DIR = "/home/lotfikan/djangoGPT/django_modules"  # Updated base directory for external Django modules

class CreateModuleRequest(BaseModel):
    path: str
    type: str
    code: str = None

class UpdateModuleRequest(BaseModel):
    code: str

@router.post("/modules/{app}/create/", description="Create a new module in a specified Django app.")
async def create_module_endpoint(app: str, request: CreateModuleRequest):
    try:
        result = create_module(app, request.path, request.type, request.code)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/modules/{app}/list/", description="List all modules in a specified Django app.")
async def list_modules_endpoint(app: str):
    try:
        result = list_modules(app)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/modules/{app}/{path:path}", description="Retrieve the code of a specific module in a Django app.")
async def get_module_code_endpoint(app: str, path: str):
    try:
        result = get_module_code(app, path.replace(".", os.sep) + ".py")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/modules/{app}/{path:path}", description="Update the code of a specific module in a Django app.")
async def update_module_code_endpoint(app: str, path: str, request: UpdateModuleRequest):
    try:
        result = update_module_code(app, path.replace(".", os.sep) + ".py", request.code)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/modules/{app}/{path:path}/deactivate/", description="Deactivate a specific module in a Django app by commenting out its code.")
async def deactivate_module_endpoint(app: str, path: str):
    try:
        result = deactivate_module(app, path.replace(".", os.sep) + ".py")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
