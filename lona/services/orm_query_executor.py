import os
import django
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from typing import Any, Dict, List, Union
from subprocess import run, PIPE
from fastapi import HTTPException

# Ensure DJANGO_SETTINGS_MODULE is set dynamically only when executing ORM queries

def execute_orm_query(query: str) -> dict:
    try:
        project_dir = os.getenv("DJANGO_PROJECT_DIR")
        venv_path = os.getenv("VENV_PATH")
        if not project_dir or not venv_path:
            raise RuntimeError("Environment variables DJANGO_PROJECT_DIR or VENV_PATH are not set.")

        python_executable = os.path.join(venv_path, "bin", "python")
        manage_py_path = os.path.join(project_dir, "manage.py")

        # Set DJANGO_SETTINGS_MODULE dynamically
        if not os.getenv("DJANGO_SETTINGS_MODULE"):
            working_dir_name = os.path.basename(os.path.normpath(project_dir))
            os.environ["DJANGO_SETTINGS_MODULE"] = f"{working_dir_name}.settings.base"

        # Initialize Django
        django.setup()

        # Run the ORM query using Django's shell
        result = run(
            [python_executable, manage_py_path, "shell", "-c", query],
            stdout=PIPE,
            stderr=PIPE,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return {"output": result.stdout.strip()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error executing query: {str(e)}")

def get_model_fields(app_name: str, model_name: str) -> Union[List[str], str]:
    try:
        model = apps.get_model(app_name, model_name)
        return [field.name for field in model._meta.get_fields()]
    except LookupError:
        return f"Model {model_name} not found in app {app_name}."
    except Exception as e:
        return f"Error retrieving model fields: {str(e)}"