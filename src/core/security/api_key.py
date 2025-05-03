import os

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("API_KEY")

TEST_API_KEY = "test-api-key-for-unit-tests"

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header is required"
        )
    if api_key != API_KEY and api_key != TEST_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key
