# src/{{ project_slug }}/main.py

from fastapi import FastAPI
import uvicorn

# from .core.config import settings # Assuming you'll have a Pydantic settings management
from .routers import items # Assuming an items router
# from . import __version__ # To access the version if needed

app = FastAPI(
    title="{{ project_name }}",
    # version=__version__,
    description="{{ project_description | default('A cool FastAPI application.') }}",
    # openapi_url=f"/{settings.API_V1_STR}/openapi.json" # Example if using versioned API
)

# Include routers
app.include_router(items.router, prefix="/api/v1", tags=["items"])
# Add other routers here

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to {{ project_name }}! Visit /docs for API documentation."}

def run_dev():
    """Run the development server."""
    uvicorn.run(
        "{{ project_slug }}.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )

# For Gunicorn or other ASGI servers in production, you would point to `{{ project_slug }}.main:app` 