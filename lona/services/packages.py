from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.package_manager import install_package, list_installed_packages

router = APIRouter()

class PackageRequest(BaseModel):
    package_name: str

@router.post("/packages/install")
async def install_package_endpoint(request: PackageRequest):
    try:
        result = install_package(request.package_name)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/packages/")
async def list_packages():
    try:
        packages = list_installed_packages()
        return {"success": True, "packages": packages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
