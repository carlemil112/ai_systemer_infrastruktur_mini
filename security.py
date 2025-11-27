# security.py
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

# navnet på headeren:
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

# gyldige nøgler (brug en af dem som value)
VALID_KEYS = {"secret123", "testkey456"}


async def get_current_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    # api_key er None hvis headeren mangler
    if api_key in VALID_KEYS:
        return api_key

    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key",
    )
