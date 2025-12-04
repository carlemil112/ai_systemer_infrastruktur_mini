from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

# Name on the header
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

# Keys to use
VALID_KEYS = {"secret123", "testkey456"}


async def get_current_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    # api_key = none if the header is missing
    if api_key in VALID_KEYS:
        return api_key

    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key",
    )

