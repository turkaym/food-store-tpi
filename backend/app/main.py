from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html

from app.core.config import settings
from app.core.database import create_all_tables
from app.modules.auth.router import router as auth_router
from app.modules.categorias.router import router as categories_router
from app.modules.productos.router import router as products_router
from app.modules.pedidos.router import router as orders_router
from app.modules.usuarios.router import router as users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_all_tables()
    yield


app = FastAPI(
    title="Food Store API",
    version="1.0.0",
    lifespan=lifespan,
    redoc_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url=(
            "https://cdn.redoc.ly/redoc/v2.5.3/bundles/redoc.standalone.js"
        ),
    )


app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")
