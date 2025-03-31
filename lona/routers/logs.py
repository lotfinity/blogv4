from fastapi import APIRouter, HTTPException
from services.logs_debugging import get_logs as fetch_logs, get_errors as fetch_errors  # Updated imports

router = APIRouter()

@router.get("/logs/", description="Retrieve the application logs.")
async def get_logs():
    try:
        logs = fetch_logs()
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/errors/", description="Retrieve only the error logs from the application.")
async def get_errors():
    try:
        errors = fetch_errors()
        return {"errors": errors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))