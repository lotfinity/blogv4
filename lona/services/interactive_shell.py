import os
from subprocess import run, PIPE
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class ShellRequest(BaseModel):
    code: str

@router.post("/shell/execute")
async def execute_shell_code(request: ShellRequest):
    try:
        result = execute_python_code(request.code)
        return {
            "output": result["output"],
            "errors": result["errors"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def execute_python_code(code: str) -> dict:
    """
    Executes Python code using Django's shell_plus and returns the result.

    Args:
        code (str): The Python code to execute.

    Returns:
        dict: A dictionary containing the output and errors.
    """
    try:
        # Get the virtual environment and Django project directory paths from the .env file
        venv_path = os.getenv("VENV_PATH")
        project_dir = os.getenv("DJANGO_PROJECT_DIR")
        if not venv_path or not project_dir:
            raise RuntimeError("Virtual environment or project directory path not set in .env file")

        python_executable = os.path.join(venv_path, "bin", "python")
        manage_py_path = os.path.join(project_dir, "manage.py")

        # Check if manage.py exists
        if not os.path.isfile(manage_py_path):
            raise RuntimeError(f"manage.py not found at {manage_py_path}")

        # Execute the Python code using shell_plus
        result = run(
            [python_executable, manage_py_path, "shell_plus", "--command", code],
            stdout=PIPE,
            stderr=PIPE,
            text=True
        )

        return {
            "output": result.stdout.strip(),
            "errors": result.stderr.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing Python code: {str(e)}")