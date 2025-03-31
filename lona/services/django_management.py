import os
import django
from django.core.management import call_command
from fastapi import HTTPException
from subprocess import run, PIPE

# Ensure DJANGO_SETTINGS_MODULE is set dynamically only when executing management commands

async def execute_management_command(command: str, *args: str) -> dict:
    try:
        project_dir = os.getenv("DJANGO_PROJECT_DIR")
        venv_path = os.getenv("VENV_PATH")
        if not project_dir or not venv_path:
            raise RuntimeError("Environment variables DJANGO_PROJECT_DIR or VENV_PATH are not set.")

        manage_py_path = os.path.join(project_dir, "manage.py")  # Construct the manage.py path
        python_executable = os.path.join(venv_path, "bin", "python")

        # Check if manage.py exists
        if not os.path.isfile(manage_py_path):
            raise RuntimeError(f"manage.py not found at {manage_py_path}")

        # Run the management command
        result = run(
            [python_executable, manage_py_path, command, *args],
            stdout=PIPE,
            stderr=PIPE,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return {"status": "success", "output": result.stdout.strip()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error executing command: {str(e)}")

async def list_available_commands() -> dict:
    try:
        # Get the Django project directory and virtual environment path from the .env file
        project_dir = os.getenv("DJANGO_PROJECT_DIR", ".")
        venv_path = os.getenv("VENV_PATH")
        if not venv_path:
            raise RuntimeError("Virtual environment path not set in .env file")

        manage_py_path = os.path.join(project_dir, "manage.py")
        python_executable = os.path.join(venv_path, "bin", "python")

        # Check if manage.py exists
        if not os.path.isfile(manage_py_path):
            raise RuntimeError(f"manage.py not found at {manage_py_path}")

        # Run the 'help' command to list available commands using the correct Python executable
        result = run([python_executable, manage_py_path, "help"], stdout=PIPE, stderr=PIPE, text=True)
        if result.returncode != 0:
            if "ModuleNotFoundError" in result.stderr:
                missing_module = result.stderr.split("No module named ")[-1].strip().strip("'")
                raise RuntimeError(f"Missing module: {missing_module}. Please install it using pip.")
            raise RuntimeError(result.stderr)

        commands = result.stdout.splitlines()
        return {"available_commands": commands}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing commands: {str(e)}")