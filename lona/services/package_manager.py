import os
from subprocess import run, PIPE
from fastapi import HTTPException

def install_package(package_name: str) -> dict:
    try:
        # Get the virtual environment path from the .env file
        venv_path = os.getenv("VENV_PATH")
        if not venv_path:
            raise RuntimeError("Virtual environment path not set in .env file")

        pip_path = os.path.join(venv_path, "bin", "pip")

        # Run pip install
        result = run([pip_path, "install", package_name], stdout=PIPE, stderr=PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return {"message": f"Package '{package_name}' installed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error installing package: {str(e)}")

def list_installed_packages() -> dict:
    try:
        # Get the virtual environment path from the .env file
        venv_path = os.getenv("VENV_PATH")
        if not venv_path:
            raise RuntimeError("Virtual environment path not set in .env file")

        pip_path = os.path.join(venv_path, "bin", "pip")

        # Run pip list
        result = run([pip_path, "list"], stdout=PIPE, stderr=PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        packages = result.stdout.splitlines()
        return {"installed_packages": packages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing packages: {str(e)}")
