from mcp_server import mcp
import httpx
import os
from typing import Optional
from cachetools import TTLCache
from logger import get_logger
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)

def async_cached(cache):
    """Async-compatible cache decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in cache:
                return cache[key]
            result = await func(*args, **kwargs)
            cache[key] = result
            return result
        return wrapper
    return decorator

data_platform_url_prefix = os.getenv("DATA_PLATFORM_URL_PREFIX")
data_platform_app_key = os.getenv("DATA_PLATFORM_APP_KEY")
data_platform_app_secret = os.getenv("DATA_PLATFORM_APP_SECRET")

get_access_token_url = f"{data_platform_url_prefix}/open_api/authentication/get_access_token"
staff_info_url = f"{data_platform_url_prefix}/open_api/customization/trsjzgjbxx/full"

# Cache access tokens for 7200 seconds (2 hours)
token_cache = TTLCache(maxsize=100, ttl=7200)

@async_cached(token_cache)
async def get_access_token() -> dict:
    """Get access token from API using app key and secret"""
    logger.info("Fetching access token...")
    params = {
        "key": data_platform_app_key,
        "secret": data_platform_app_secret
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(get_access_token_url, params=params)
        response.raise_for_status()
        return response.json()["result"]

# Cache staff info for 86400 seconds (1 day)
staff_cache = TTLCache(maxsize=1000, ttl=86400)

@mcp.tool()
@async_cached(staff_cache)
async def get_staff_info(zgh: Optional[str|int] = None, xm: Optional[str] = None, sj: Optional[str] = None) -> dict:
    """获取教职工信息，可通过教职工工号、姓名、手机号等信息查询"""
    # check whether all parameters are None or empty
    if not zgh and not xm and not sj:
        logger.error("At least one parameter must be provided")
        raise ValueError("At least one parameter must be provided")
    if zgh and isinstance(zgh, int):
        zgh = str(zgh) # Ensure zgh is a string
    
    logger.info("Fetching access token...")
    token = await get_access_token()
    headers = {
        "Content-Type": "application/json"
    }
    # Build query conditions dynamically based on provided parameters
    conditions = []
    if zgh:
        conditions.append({"ZGH": {"eq": zgh}})
    if xm:
        conditions.append({"XM": {"eq": xm}})
    if sj:
        conditions.append({"SJ": {"eq": sj}})
    
    payload = {
        "access_token": token["access_token"],
        "and": conditions
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(staff_info_url, json=payload, headers=headers)
        response.raise_for_status()
        
        # check if the response is correct
        if response.json()["result"] == None:
            logger.error(f"Some error occurred when fetching staff info, error: {response.json()}")
            raise Exception(response.json())
        
        result = response.json()["result"]
        
        final_result = []
        # Map data to data_struct keys
        data_struct = result["data_struct"]
        for item in result["data"]:
            mapped_data = {}
            for key, value in item.items():
                if key in data_struct:
                    mapped_data[data_struct[key]] = value
            final_result.append(mapped_data)
                    
        return final_result
