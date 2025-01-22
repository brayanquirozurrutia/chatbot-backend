import aioredis
import json
from typing import Any

# Conexión a Redis
redis_host = "redis"
redis_port = 6379

async def get_redis():
    redis = await aioredis.from_url(f"redis://{redis_host}:{redis_port}", decode_responses=True)
    return redis

# Almacenar datos en caché
async def set_cache(key: str, value: Any, expire: int = 3600):
    redis = await get_redis()
    await redis.set(key, json.dumps(value), ex=expire)

# Obtener datos de la caché
async def get_cache(key: str) -> Any:
    redis = await get_redis()
    data = await redis.get(key)
    return json.loads(data) if data else None

# Eliminar clave de la caché
async def delete_cache(key: str):
    redis = await get_redis()
    await redis.delete(key)
