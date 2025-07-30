import aiohttp
import asyncio
import sys
import base64
import os
import json

class epic_client():
    def __init__(self):
        self.launcherAppClient2 = ('34a02cf8f4414e29b15921876da36f9a', 'daafbccc737745039dffe53d94fc76cf')
        self.uefn = ('3e13c5c57f594a578abe516eecb673fe', '530e316c337e409893c55ec44f22cd62')
        self.fortniteAndroidGameClient = ('3f69e56c7649492c8cc29f1af08a8a12', 'b51ee9cb12234f50a69efa67ef53812e')
        self.fortniteSwitchGameClient = ('5229dcd3ac3845208b496649092f251b', 'e3bd2d3e-bf8c-4857-9e7d-f3d947d220c7')
        self.fortniteIosGameClient = ('af43dc71dd91452396fcdffbd7a8e8a9', '4YXvSEBLFRPLh1hzGZAkfOi5mqupFohZ')

        self.choice = {
            'LauncherAppClient2': self.launcherAppClient2,
            'UEFN': self.uefn,
            'FortniteAndroidGameClient': self.fortniteAndroidGameClient,
            'fortniteSwitchGameClient': self.fortniteSwitchGameClient,
            'fortniteIosGameClient': self.fortniteIosGameClient
        }


if sys.platform.startswith("win"):
    import asyncio.proactor_events
    from asyncio.proactor_events import _ProactorBasePipeTransport

    def silent_close(self):
        try:
            if self._loop.is_closed():
                    return
            self._loop.call_soon(self._call_connection_lost, None)
        except Exception:
            pass

    _ProactorBasePipeTransport.__del__ = silent_close

class fnclient:
    _config_data = {}

    @staticmethod
    def config(**config_kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs):
                fnclient._config_data.update(config_kwargs)
                fnclient._config_data.update(kwargs)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    
    @staticmethod
    def access_token(func):
        async def get_token():
            data = fnclient._config_data
            if 'client' not in data:
                raise Exception("you have not configured your client")

            client_id, client_secret = epic_client().choice[data['client']]
            auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            payload = {}
            auth_basic = None

            if "exchange_code" in data:
                payload = {
                    "grant_type": "exchange_code",
                    "exchange_code": data["exchange_code"],
                    "token_type": "eg1"
                }
                auth_basic = auth

            elif "authorization_code" in data:
                payload = {
                    "grant_type": "authorization_code",
                    "code": data["authorization_code"],
                }
                auth_basic = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="

            elif "device_auth" in data:
                device = data["device_auth"]
                payload = {
                    "grant_type": "device_auth",
                    "account_id": device["account_id"],
                    "device_id": device["device"],
                    "secret": device["secret"]
                }
                auth_basic = auth

            else:
                raise Exception()

            if auth_basic:
                headers["Authorization"] = f"Basic {auth_basic}"

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
                    data=payload,
                    headers=headers
                ) as resp:
                    response_json = await resp.json()
                    return response_json.get("access_token"), response_json.get('account_id')

        def wrapper(*args, **kwargs):
            return asyncio.run(get_token())
        return wrapper
