from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.orm_query_executor import execute_orm_query

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query/execute", description="Execute a raw ORM query on the Django database and return the results.")
async def execute_query(request: QueryRequest):
    try:
        result = execute_orm_query(request.query)  # Removed 'await'
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))