import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.routers import main

from dotenv import load_dotenv

load_dotenv()

def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(main.router, prefix="/api/v1")
    return

def init_middleware(app: FastAPI) -> None:
    return


def create_app() -> FastAPI:
    app = FastAPI(
        title="Company Server",
        description="API",
        version="1.0.0",
        docs_url="/docs",
        debug = bool(os.getenv("DEBUG"))
    )
    init_routers(app=app)
    init_cors(app=app)
    init_middleware(app=app)
    return app



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    tags_desc_list = [
        {"name": "user", "description": "Operations about user"},
    ]
    openapi_schema = get_openapi(
        title="Company",
        version="1.0",
        routes=app.routes,
        description="This is a sample Company Server ",
    )
    openapi_schema["tags"] = tags_desc_list
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = create_app()
app.openapi = custom_openapi

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    host = os.getenv("HOST")

    uvicorn.run(app,port=port,host=host)