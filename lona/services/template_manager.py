import os
from fastapi import HTTPException
from dotenv import load_dotenv
from services.logs_debugging import logger

# Load environment variables from .env
load_dotenv()

TEMPLATES_DIR = os.getenv("TEMPLATES_DIR", "home/lotfikan/blogv3/templates/")

def validate_path(path: str):
    """Prevent directory traversal attacks."""
    if ".." in path or path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid path. Directory traversal is not allowed.")

def create_template(app: str, path: str, content: str = ""):
    validate_path(path)

    base_dir = os.path.join(TEMPLATES_DIR, app)
    full_path = os.path.join(base_dir, path)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Write the content to the file
    with open(full_path, "w") as f:
        f.write(content)

    logger.info(f"Template created: {full_path}")
    return {"message": f"Template created at {full_path}"}

def list_templates(app: str):
    base_dir = os.path.join(TEMPLATES_DIR, app)
    logger.debug(f"Looking for templates in directory: {base_dir}")
    print(f"DEBUG: Looking for templates in directory: {base_dir}")  # Print the base directory for debugging
    templates = []

    for root, _, files in os.walk(base_dir):
        logger.debug(f"Checking directory: {root}")
        print(f"DEBUG: Checking directory: {root}")  # Print each directory being checked
        for file in files:
            if file.endswith(".html"):
                relative_path = os.path.relpath(os.path.join(root, file), base_dir)
                templates.append(relative_path)
                logger.debug(f"Found template: {relative_path}")

    logger.info(f"Total templates found: {len(templates)}")
    return {"templates": templates}

def get_template_content(app: str, path: str):
    validate_path(path)

    base_dir = os.path.join(TEMPLATES_DIR, app)
    full_path = os.path.join(base_dir, path)

    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail=f"Template '{path}' not found.")

    with open(full_path, "r") as f:
        content = f.read()

    logger.info(f"Template retrieved: {full_path}")
    return {"content": content}

def update_template_content(app: str, path: str, content: str):
    validate_path(path)

    base_dir = os.path.join(TEMPLATES_DIR, app)
    full_path = os.path.join(base_dir, path)

    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail=f"Template '{path}' not found.")

    with open(full_path, "w") as f:
        f.write(content)

    logger.info(f"Template updated: {full_path}")
    return {"message": f"Template updated at {full_path}"}

def delete_template(app: str, path: str):
    validate_path(path)

    base_dir = os.path.join(TEMPLATES_DIR, app)
    full_path = os.path.join(base_dir, path)

    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail=f"Template '{path}' not found.")

    os.remove(full_path)

    logger.info(f"Template deleted: {full_path}")
    return {"message": f"Template deleted at {full_path}"}
