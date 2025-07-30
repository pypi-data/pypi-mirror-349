import aiohttp
import asyncio
import sys
import base64
import os
import json

class Friend:
    @staticmethod
    def friend_list(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends"
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
    def add_friend(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends/{friend_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def delete_friend(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends/{friend_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def AcceptBulk(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/incoming/accept"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def ClearFriendsList(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper

    @staticmethod
    def IncomingFriendRequests(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/incoming"
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
    def OutgoingFriendRequests(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/outgoing"
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
    def SuggestedFriends(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/suggested"
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
    def Summary(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/summary"
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
    def FriendShipInfo(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends/{friend_id}"
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
    def MutualFriends(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends/{friend_id}/mutual"
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
    def BlockFriends(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/blocklist/{friend_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def ClearBlockList(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/public/blocklist/{account_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def BlockList(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/public/blocklist/{account_id}"
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
    def UnblockFriends(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/blocklist/{friend_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
