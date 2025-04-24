from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import redis.asyncio as redis_asyncio
from vec2.api import router

class VerboseRedisBackend(RedisBackend):
    async def get(self, key, *args, **kwargs):
        value = await super().get(key, *args, **kwargs)
        if value is not None:
            print("cache hit")
        return value

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    @app.on_event("startup")
    async def startup():
        redis_client = redis_asyncio.from_url("redis://redis:6379", encoding="utf8", decode_responses=True)
        FastAPICache.init(VerboseRedisBackend(redis_client), prefix="fastapi-cache")

    return app

app = create_app()
@app.get("/")
@cache(expire=60)
def read_root():
    return JSONResponse(content={"message": "server running"})
