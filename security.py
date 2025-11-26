from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

# til login
VALID_KEYS = {
    "secret-key-person1",
    "secret-key-person2",
    "secret-key-client",
}

async def get_current_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    if api_key in VALID_KEYS:
        return api_key
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
