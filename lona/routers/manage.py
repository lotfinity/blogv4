from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.django_management import execute_management_command, list_available_commands

router = APIRouter()

class CommandRequest(BaseModel):
    command: str
    args: list = []

@router.post("/manage/command", description="Execute a Django management command with optional arguments.")
async def manage_command(request: CommandRequest):
    try:
        output = await execute_management_command(request.command, *request.args)  # Ensure correct args unpacking
        return {"success": True, "output": output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/manage/commands", description="List all available Django management commands.")
async def get_available_commands():
    try:
        commands = await list_available_commands()
        return {"success": True, "commands": commands}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))