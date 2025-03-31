from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.interactive_shell import execute_python_code

router = APIRouter()

class ShellRequest(BaseModel):
    code: str

@router.post(
    "/shell/execute",
    description=(
        "Execute Python code within the Django shell environment. "
        "Note: This endpoint only supports valid Python statements and does not execute shell commands like 'ls'."
    )
)
async def execute_shell_code(request: ShellRequest):
    try:
        result = execute_python_code(request.code)
        return {
            "output": result["output"],
            "errors": result["errors"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))