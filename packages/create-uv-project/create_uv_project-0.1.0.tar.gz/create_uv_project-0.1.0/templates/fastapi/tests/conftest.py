# tests/conftest.py

import pytest
import pytest_asyncio # For async fixtures if needed; httpx can work without it for simple cases
from httpx import AsyncClient

from {{ project_slug }}.main import app # Import your FastAPI app

@pytest_asyncio.fixture(scope="function") # "function" scope ensures fresh client for each test
async def test_client() -> AsyncClient:
    """
    Create an AsyncClient instance for testing the FastAPI application.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

# You can add other global fixtures here, for example:
# - Database setup/teardown for integration tests
# - Mocked services
# - Test data factories 