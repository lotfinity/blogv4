from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models.element_assets import ElementAsset
from typing import Optional, List
import os

router = APIRouter()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///element_assets.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

class ElementQuery(BaseModel):
    html_element: Optional[str] = None
    template_file: Optional[str] = None

class ElementPatch(BaseModel):
    css_block: Optional[str] = None
    js_snippets: Optional[str] = None

@router.post("/elements/query", description="Query elements based on parameters.")
async def query_elements(query: ElementQuery):
    session = Session(bind=engine)
    try:
        filters = []
        if query.html_element:
            filters.append(ElementAsset.html_element == query.html_element)
        if query.template_file:
            filters.append(ElementAsset.template_file == query.template_file)

        elements = session.query(ElementAsset).filter(*filters).all()
        if not elements:
            raise HTTPException(status_code=404, detail="No elements found matching the query.")

        return [
            {
                "id": element.id,
                "html_element": element.html_element,
                "css_block": element.css_block,
                "js_snippets": element.js_snippets,
                "template_file": element.template_file,
                "created_at": element.created_at,
                "updated_at": element.updated_at,
            }
            for element in elements
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@router.patch("/elements/{element_id}", description="Patch an element's CSS block or JS snippets.")
async def patch_element(element_id: int, patch: ElementPatch):
    session = Session(bind=engine)
    try:
        element = session.query(ElementAsset).filter_by(id=element_id).first()
        if not element:
            raise HTTPException(status_code=404, detail="Element not found.")

        if patch.css_block is not None:
            element.css_block = patch.css_block
        if patch.js_snippets is not None:
            element.js_snippets = patch.js_snippets

        session.commit()
        return {
            "message": "Element updated successfully.",
            "element": {
                "id": element.id,
                "html_element": element.html_element,
                "css_block": element.css_block,
                "js_snippets": element.js_snippets,
                "template_file": element.template_file,
                "created_at": element.created_at,
                "updated_at": element.updated_at,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
