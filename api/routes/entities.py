"""Stub route — entities CRUD (Phase 2 implementation)."""
from fastapi import APIRouter
router = APIRouter()

@router.get("/", summary="List entities (stub)")
async def list_entities():
    return {"message": "Entity routes — implemented in Phase 2", "status": "stub"}
