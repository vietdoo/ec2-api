from fastapi import FastAPI
from fastapi.responses import JSONResponse
from vec2.api import router

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    
    return app

app = create_app()
@app.get("/")
def read_root():
    return JSONResponse(content={"message": "server running"})

