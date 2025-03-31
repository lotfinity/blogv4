from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.template_manager import (
    create_template,
    list_templates,
    get_template_content,
    update_template_content,
    delete_template,
)

router = APIRouter()

class CreateTemplateRequest(BaseModel):
    path: str
    content: str = ""

class UpdateTemplateRequest(BaseModel):
    content: str

@router.post("/templates/{app}/create/", description="Create a new template in a specified Django app.")
async def create_template_endpoint(app: str, request: CreateTemplateRequest):
    try:
        result = create_template(app, request.path, request.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/templates/{app}/list/", description="List all templates in a specified Django app.")
async def list_templates_endpoint(app: str):
    try:
        result = list_templates(app)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/templates/{app}/{path:path}", description="Retrieve the content of a specific template in a Django app.")
async def get_template_content_endpoint(app: str, path: str):
    try:
        result = get_template_content(app, path)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/templates/{app}/{path:path}", description="Update the content of a specific template in a Django app.")
async def update_template_content_endpoint(app: str, path: str, request: UpdateTemplateRequest):
    try:
        result = update_template_content(app, path, request.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/templates/{app}/{path:path}", description="Delete a specific template in a Django app.")
async def delete_template_endpoint(app: str, path: str):
    try:
        result = delete_template(app, path)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
