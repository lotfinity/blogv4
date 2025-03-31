import os
from fastapi import HTTPException
from services.logs_debugging import logger
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DJANGO_PROJECT_DIR = os.getenv("DJANGO_PROJECT_DIR", "home/lotfikan/blogv3/")

ALLOWED_TYPES = ["management_command", "model", "generic_module"]

def validate_path(path: str):
    """Prevent directory traversal attacks."""
    if ".." in path or path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid path. Directory traversal is not allowed.")

def create_module(app: str, path: str, module_type: str, code: str = None):
    validate_path(path)

    base_dir = os.path.join(DJANGO_PROJECT_DIR, app)
    # Ensure the path ends with ".py" for Python files
    if not path.endswith(".py"):
        path = os.path.join(path, "__init__.py")

    full_path = os.path.join(base_dir, path)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Generate boilerplate code if needed
    if module_type == "management_command":
        if not code:
            code = (
                "from django.core.management.base import BaseCommand\n\n"
                "class Command(BaseCommand):\n"
                "    help = 'Describe your command here'\n\n"
                "    def handle(self, *args, **kwargs):\n"
                "        pass\n"
            )
    elif not code:
        code = ""

    # Write the code to the file
    with open(full_path, "w") as f:
        f.write(code)

    logger.info(f"Module created: {full_path}")
    return {"message": f"Module created at {full_path}"}

def list_modules(app: str):
    base_dir = os.path.join(DJANGO_PROJECT_DIR, app)
    logger.debug(f"Looking for modules in directory: {base_dir}")
    print(f"DEBUG: Looking for modules in directory: {base_dir}")  # Print the base directory for debugging
    modules = []

    for root, _, files in os.walk(base_dir):
        logger.debug(f"Checking directory: {root}")
        print(f"DEBUG: Checking directory: {root}")  # Print each directory being checked
        for file in files:
            if file.endswith(".py"):
                # Include package-style paths
                relative_path = os.path.relpath(os.path.join(root, file), base_dir)
                modules.append(relative_path.replace(os.sep, ".").rstrip(".py"))
                logger.debug(f"Found module: {relative_path}")

    logger.info(f"Total modules found: {len(modules)}")
    return {"modules": modules}

def get_module_code(app: str, path: str):
    validate_path(path)

    base_dir = os.path.join(DJANGO_PROJECT_DIR, app)
    full_path = os.path.join(base_dir, path)

    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail=f"Module '{path}' not found.")

    with open(full_path, "r") as f:
        code = f.read()

    logger.info(f"Module retrieved: {full_path}")
    return {"code": code}

def update_module_code(app: str, path: str, code: str):
    validate_path(path)

    base_dir = os.path.join(DJANGO_PROJECT_DIR, app)
    full_path = os.path.join(base_dir, path)

    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail=f"Module '{path}' not found.")

    with open(full_path, "w") as f:
        f.write(code)

    logger.info(f"Module updated: {full_path}")
    return {"message": f"Module updated at {full_path}"}

def deactivate_module(app: str, path: str):
    validate_path(path)

    base_dir = os.path.join(DJANGO_PROJECT_DIR, app)
    full_path = os.path.join(base_dir, path)

    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail=f"Module '{path}' not found.")

    with open(full_path, "r") as f:
        code = f.read()

    deactivated_code = f"# DEACTIVATED MODULE\n'''\n{code}\n'''"

    with open(full_path, "w") as f:
        f.write(deactivated_code)

    logger.info(f"Module deactivated: {full_path}")
    return {"message": f"Module deactivated at {full_path}"}
