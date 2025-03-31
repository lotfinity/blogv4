from django.apps import apps
from fastapi import APIRouter, HTTPException

router = APIRouter()

def get_all_models():
    try:
        return {app.label: [model.__name__ for model in app.get_models()] for app in apps.get_app_configs()}
    except Exception as e:
        raise RuntimeError(f"Error retrieving all models: {str(e)}")

def get_models_by_app(app_name: str):
    try:
        app = apps.get_app_config(app_name)
        return [model.__name__ for model in app.get_models()]
    except LookupError:
        raise ValueError("App not found")
    except Exception as e:
        raise RuntimeError(f"Error retrieving models for app '{app_name}': {str(e)}")

def get_model_details(app_name: str, model_name: str):
    try:
        app = apps.get_app_config(app_name)
        model = app.get_model(model_name)
        return {field.name: field.get_internal_type() for field in model._meta.get_fields()}
    except LookupError:
        raise ValueError("Model or app not found")
    except Exception as e:
        raise RuntimeError(f"Error retrieving details for model '{model_name}' in app '{app_name}': {str(e)}")

@router.get("/models/")
async def list_models():
    try:
        models = get_all_models()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{app_name}/")
async def list_app_models(app_name: str):
    try:
        models = get_models_by_app(app_name)
        return {app_name: models}
    except ValueError:
        raise HTTPException(status_code=404, detail="App not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{app_name}/{model_name}/")
async def get_model_details_route(app_name: str, model_name: str):
    try:
        fields = get_model_details(app_name, model_name)
        return {"model": model_name, "fields": fields}
    except ValueError:
        raise HTTPException(status_code=404, detail="Model or app not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))