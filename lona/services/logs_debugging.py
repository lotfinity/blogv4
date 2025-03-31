from fastapi import APIRouter, HTTPException
import logging
import os

router = APIRouter()

# Configure logging
logger = logging.getLogger("django_api_orchestrator")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("django_api_orchestrator.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_logs() -> list:
    try:
        log_file_path = os.getenv("LOG_FILE_PATH", "django_api_orchestrator.log")
        with open(log_file_path, "r") as log_file:
            logs = log_file.readlines()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching logs: {str(e)}")

def get_errors() -> list:
    try:
        log_file_path = os.getenv("LOG_FILE_PATH", "django_api_orchestrator.log")
        with open(log_file_path, "r") as log_file:
            logs = log_file.readlines()
        errors = [log for log in logs if "ERROR" in log]
        return errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching error logs: {str(e)}")

@router.get("/logs/")
async def get_logs_endpoint():  # Renamed from 'get_logs'
    try:
        logs = get_logs()
        return {"logs": logs}
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch logs")

@router.get("/errors/")
async def get_errors_endpoint():  # Renamed from 'get_errors'
    try:
        errors = get_errors()
        return {"errors": errors}
    except Exception as e:
        logger.error(f"Error fetching error logs: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch error logs")