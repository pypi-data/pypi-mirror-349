import aiohttp
import asyncio

class Auth:

    @staticmethod
    def generate_exchange_code(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get('code')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def token_is_valid(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/verify"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        return "Valid"
                    else:
                        return "Invalid"
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def is_mfa(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("tfa_enabled", False)
                    return None
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def refresh_token(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        exchange_code = data.get('code')
                        if not exchange_code:return
                        return 
                    
            url_oauth = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
            data = {"grant_type": "exchange_code","exchange_code": exchange_code,"token_type": "eg1"}
            async with session.post(url_oauth, data=data) as token_resp:
                if token_resp.status != 200:
                    token_data = token_resp.json()
                    return {
                        "access_token": token_data.get("access_token"),
                        "refresh_token": token_data.get("refresh_token"),
                        "expires_in": token_data.get("expires_in"),
                    }
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper

    @staticmethod
    def revoke_token(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token, session required.")
            access_token, session = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/oauth/sessions/kill/{session}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as resp:
                    if resp.status == 204:
                        return
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def KillAllSession(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token= args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/oauth/sessions/kill?killType=all"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as resp:
                    if resp.status == 204:
                        return
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper