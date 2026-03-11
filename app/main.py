from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api.router import master_router

app = FastAPI(
    title="TODO",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
)

app.include_router(master_router)

@app.get("/")
def root():
    return {"message": "TODO API"}

@app.get("/docs", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )