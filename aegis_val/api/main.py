from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aegis_val.api.core.config import settings
from aegis_val.api.routes import critique

def get_application() -> FastAPI:
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(critique.router, prefix=settings.API_V1_STR)

    @_app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": settings.VERSION}

    @_app.get("/")
    async def root():
        return {"message": "Welcome to Aegis-Val API"}

    return _app

app = get_application()
