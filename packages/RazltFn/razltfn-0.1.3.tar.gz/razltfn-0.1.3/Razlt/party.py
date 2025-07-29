import aiohttp
import asyncio
import sys
import base64
import os
import json


class Party:

    @staticmethod
    def is_online(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("account_id required.")
            account_id = args[0]
            url = f"https://yls.julesbot.com/api/accounts/{account_id}/onlineStatus"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("isOnline", False)
                    return False

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper

    @staticmethod
    def is_in_party(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return True if data else False
                    elif resp.status == 404:
                        return False
                    else:
                        return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper

    @staticmethod
    def meta(func):
        async def metaset(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            async with aiohttp.ClientSession() as session:
                url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}'
                headers = {
                    "Authorization": f"bearer {access_token}",
                    "Content-Type": "application/json"
                }

                async with session.get(url, headers=headers) as response:
                    data = await response.json()
                    if "current" not in data or not data["current"]:
                        return None, None

                    current_party = data["current"][0]
                    party_id = current_party["id"]

                    revision = None
                    for member in current_party["members"]:
                        if member["account_id"] == account_id:
                            revision = member["revision"]
                            break

                    if revision is None:
                        return None, None
                    
                payload["revision"] = revision
                if "update" in payload:
                    payload["update"] = {
                        key: json.dumps(value) for key, value in payload["update"].items()
                    }

                patch_url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/parties/{party_id}/members/{account_id}/meta'

                if "revision" not in payload:
                    payload["revision"] = revision

                async with session.patch(patch_url, headers=headers, json=payload) as response:
                    return

                return func(*args, **kwargs)

        def wrapper(*args, **kwargs):
            return asyncio.run(metaset(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def invite(func):
        async def invite1(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]

            async with aiohttp.ClientSession() as session:
                url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}'
                headers = {
                    "Authorization": f"bearer {access_token}",
                    "Content-Type": "application/json"
                }

                async with session.get(url, headers=headers) as response:
                    data = await response.json()
                    if "current" not in data or not data["current"]:
                        return None, None
                    platform = data['current'][0]['members'][0]['connections'][0]['meta'].get('urn:epic:conn:platform_s')
                    user = data['current'][0]['members'][0]['meta']['urn:epic:member:dn_s']
                    build_ids = data['current'][0]['meta']['urn:epic:cfg:build-id_s']
                    current_party = data["current"][0]
                    for member in current_party["members"]:
                        if member["account_id"] == account_id:
                            break

                data = {
                    'urn:epic:cfg:build-id_s': build_ids,
                    'urn:epic:conn:platform_s':platform,
                    'urn:epic:conn:type_s': 'game',
                    'urn:epic:invite:platformdata_s': '',
                    'urn:epic:member:dn_s': user
                }
                    
                patch_url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{friend_id}/pings/{account_id}'

                async with session.post(patch_url, headers=headers, json=data) as response:
                    return

                return func(*args, **kwargs)

        def wrapper(*args, **kwargs):
            return asyncio.run(invite1(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def leave(func):
        async def leave1(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]

            async with aiohttp.ClientSession() as session:
                url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}'
                headers = {
                    "Authorization": f"bearer {access_token}",
                    "Content-Type": "application/json"
                }

                async with session.get(url, headers=headers) as response:
                    data = await response.json()
                    if "current" not in data or not data["current"]:
                        return None, None
                    platform = data['current'][0]['members'][0]['connections'][0]['meta'].get('urn:epic:conn:platform_s')
                    user = data['current'][0]['members'][0]['meta']['urn:epic:member:dn_s']
                    build_ids = data['current'][0]['meta']['urn:epic:cfg:build-id_s']
                    current_party = data["current"][0]
                    party_id = current_party["id"]
                    for member in current_party["members"]:
                        if member["account_id"] == account_id:
                            break

                data = {
                    'urn:epic:cfg:build-id_s': build_ids,
                    'urn:epic:conn:platform_s':platform,
                    'urn:epic:conn:type_s': 'game',
                    'urn:epic:invite:platformdata_s': '',
                    'urn:epic:member:dn_s': user
                }
                    
                patch_url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/parties/{party_id}/members/{account_id}'

                async with session.delete(patch_url, headers=headers, json=data) as response:
                    return

                return func(*args, **kwargs)

        def wrapper(*args, **kwargs):
            return asyncio.run(leave1(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def requests_to_join(func):
        async def request_to_join(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]

            async with aiohttp.ClientSession() as session:
                url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}'
                headers = {
                    "Authorization": f"bearer {access_token}",
                    "Content-Type": "application/json"
                }

                async with session.get(url, headers=headers) as response:
                    data = await response.json()
                    if "current" not in data or not data["current"]:
                        return None, None
                    platform = data['current'][0]['members'][0]['connections'][0]['meta'].get('urn:epic:conn:platform_s')
                    user = data['current'][0]['members'][0]['meta']['urn:epic:member:dn_s']
                    build_ids = data['current'][0]['meta']['urn:epic:cfg:build-id_s']
                    current_party = data["current"][0]
                    for member in current_party["members"]:
                        if member["account_id"] == account_id:
                            break

                data = {
                    'urn:epic:cfg:build-id_s': build_ids,
                    'urn:epic:conn:platform_s':platform,
                    'urn:epic:conn:type_s': 'game',
                    'urn:epic:invite:platformdata_s': '',
                    'urn:epic:member:dn_s': user
                }
                    
                patch_url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/members/{friend_id}/intentions/{account_id}'

                async with session.post(patch_url, headers=headers, json=data) as response:
                    return

                return func(*args, **kwargs)

        def wrapper(*args, **kwargs):
            return asyncio.run(request_to_join(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def cancel_invite(func):
        async def cancelinvite(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]

            async with aiohttp.ClientSession() as session:
                url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}'
                headers = {
                    "Authorization": f"bearer {access_token}",
                    "Content-Type": "application/json"
                }

                async with session.get(url, headers=headers) as response:
                    data = await response.json()
                    if "current" not in data or not data["current"]:
                        return None, None
                    platform = data['current'][0]['members'][0]['connections'][0]['meta'].get('urn:epic:conn:platform_s')
                    user = data['current'][0]['members'][0]['meta']['urn:epic:member:dn_s']
                    build_ids = data['current'][0]['meta']['urn:epic:cfg:build-id_s']
                    current_party = data["current"][0]
                    party_id = current_party["id"]
                    for member in current_party["members"]:
                        if member["account_id"] == account_id:
                            break

                data = {
                    'urn:epic:cfg:build-id_s': build_ids,
                    'urn:epic:conn:platform_s':platform,
                    'urn:epic:conn:type_s': 'game',
                    'urn:epic:invite:platformdata_s': '',
                    'urn:epic:member:dn_s': user
                }
                    
                patch_url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{friend_id}/pings/{account_id}'

                async with session.delete(patch_url, headers=headers, json=data) as response:
                    return

                return func(*args, **kwargs)

        def wrapper(*args, **kwargs):
            return asyncio.run(cancelinvite(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def kick_member(func):
        async def kick(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]

            async with aiohttp.ClientSession() as session:
                url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}'
                headers = {
                    "Authorization": f"bearer {access_token}",
                    "Content-Type": "application/json"
                }

                async with session.get(url, headers=headers) as response:
                    data = await response.json()
                    if "current" not in data or not data["current"]:
                        return None, None
                    platform = data['current'][0]['members'][0]['connections'][0]['meta'].get('urn:epic:conn:platform_s')
                    user = data['current'][0]['members'][0]['meta']['urn:epic:member:dn_s']
                    build_ids = data['current'][0]['meta']['urn:epic:cfg:build-id_s']
                    current_party = data["current"][0]
                    party_id = current_party["id"]
                    for member in current_party["members"]:
                        if member["account_id"] == account_id:
                            break

                data = {
                    'urn:epic:cfg:build-id_s': build_ids,
                    'urn:epic:conn:platform_s':platform,
                    'urn:epic:conn:type_s': 'game',
                    'urn:epic:invite:platformdata_s': '',
                    'urn:epic:member:dn_s': user
                }
                    
                patch_url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/parties/{party_id}/members/{friend_id}'

                async with session.delete(patch_url, headers=headers, json=data) as response:
                    return

                return func(*args, **kwargs)

        def wrapper(*args, **kwargs):
            return asyncio.run(kick(*args, **kwargs))

        return wrapper