import aiohttp
import asyncio
import sys
import base64
import os
import json

class Device:
    @staticmethod
    def create_device(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        device_id = data.get("deviceId")
                        secret = data.get("secret")
                        if device_id and secret:
                            return account_id, device_id, secret
            return None, None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def create_DeviceCode(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/oauth/deviceAuthorization"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        verifications_uri_complete = data.get('verification_uri_complete')
                        return verifications_uri_complete, data
            return None, None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def delete_DeviceCode(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and code required.")
            access_token, code = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/oauth/deviceAuthorization/{code}"
            headers = {
                "Authorization": f"bearer {access_token}",
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
    def device_info(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and device_id required.")
            access_token, account_id, device_id = args[0], args[1], args[2]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth/{device_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
        
    @staticmethod
    def device_list(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id and device_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth/"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
