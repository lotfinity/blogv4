from fastapi import APIRouter, HTTPException
from services.models_metadata import get_all_models, get_models_by_app, get_model_details

router = APIRouter()

@router.get("/models/", description="Retrieve a list of all Django models grouped by app.")
async def list_models():
    try:
        models = get_all_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{app_name}/", description="Retrieve a list of all models in a specific Django app.")
async def list_models_by_app(app_name: str):
    try:
        models = get_models_by_app(app_name)
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{app_name}/{model_name}/", description="Retrieve detailed metadata for a specific Django model.")
async def get_model_detail(app_name: str, model_name: str):
    try:
        model_details = get_model_details(app_name, model_name)
        return {"model_details": model_details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))