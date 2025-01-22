from fastapi import APIRouter
from app.services.redis_cache import clear_cache

router = APIRouter()

@router.post("/clear_cache", summary="Limpia toda la caché")
async def clear_cache_endpoint():
    try:
        await clear_cache()
        return {"message": "Caché limpiada exitosamente"}
    except Exception as e:
        return {"error": str(e)}
