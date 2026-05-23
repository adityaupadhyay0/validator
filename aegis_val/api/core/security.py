from fastapi import Request, HTTPException, Depends
from fastapi.security import APIKeyHeader
from aegis_val.api.core.config import settings

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != settings.SECRET_KEY: # Simple check for now
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key
