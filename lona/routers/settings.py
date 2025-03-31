from fastapi import APIRouter, HTTPException
from services.settings_handler import get_all_settings, get_setting_value

router = APIRouter()

@router.get("/settings/", description="Retrieve all Django settings, including their values or error messages if inaccessible.")
async def read_settings():
    try:
        settings = get_all_settings()
        return {"settings": settings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/settings/{setting_name}/", description="Retrieve the value of a specific Django setting by its name.")
async def read_setting(setting_name: str):
    try:
        value = get_setting_value(setting_name)
        if value is None:
            raise HTTPException(status_code=404, detail="Setting not found")
        return {setting_name: value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))