import aiohttp
import asyncio
import sys
import base64
import os
import json


class Account:
    @staticmethod
    def update_account(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id and payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json=payload) as resp:
                    if resp:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def account_info(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}"
            headers = {
                "Authorization": f"Bearer {access_token}"
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
    def acceptEula(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/corrections/acceptEula"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json={"continuation": ""}) as resp:
                    if resp:
                        data = await resp.json()
                        return data.get('code')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def acceptPrivacyPolicy(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/corrections/acceptPrivacyPolicy"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json={"continuation": ""}) as resp:
                    if resp:
                        data = await resp.json()
                        return data.get('code')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper


    @staticmethod
    def CancelAccountDeletion(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/corrections/cancelPendingDeletion"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json={"continuation": ""}) as resp:
                    if resp:
                        data = await resp.json()
                        return data.get('code')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper

    @staticmethod
    def ConfirmDisplayName(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/corrections/confirmDisplayName"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json={"continuation": ""}) as resp:
                    if resp:
                        data = await resp.json()
                        return data.get('code')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def lookup_id(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}"
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
    def lookup_display(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, displayName = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/displayName/{displayName}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return f"{displayName} was not found"

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def lookup_external(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/externalAuths"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        return await resp.json()
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper

    @staticmethod
    def lookup_mail(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and email required.")
            access_token, email = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/email/{email}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        return await resp.json()
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def batch_lookup(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and list of account_ids required.")
            access_token, account_ids = args[0], args[1]
            url = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=account_ids) as resp:
                    if resp.status == 200:
                        return await resp.json()
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper

