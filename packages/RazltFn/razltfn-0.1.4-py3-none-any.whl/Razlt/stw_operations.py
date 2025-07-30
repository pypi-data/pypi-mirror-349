import aiohttp
import asyncio
import sys
import base64
import os
import json

class stw_operation:

    @staticmethod
    def compose(func):
        async def mcp(*args, **kwargs):
            if len(args) < 4:
                raise ValueError("access_token, account_id, profile, and operation required.")
            access_token, account_id, profile, operation = args[0], args[1], args[2], args[3]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/{operation}?profileId={profile}"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json={}) as response:
                        if response:
                            status = response.status
                            data = await response.json()
                            return status, data
                            
                
        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper

    @staticmethod
    def AbandonExpedition(func):
        async def mcp(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token, account_id, expeditions_id required.")
            access_token, account_id, expedition_id = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/AbandonExpedition?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json={"expeditionId": expedition_id}) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def ActivateConsumable(func):
        async def mcp(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token, account_id, targetItemId, friend_id required.")
            access_token, account_id, targetItemId, friend_id = args[0], args[1], args[2], args[3]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ActivateConsumable?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json={"targetItemId": targetItemId, "targetAccountId": friend_id}) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def AssignGadgetToLoadout(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/AssignGadgetToLoadout?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def AssignHeroToLoadout(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/AssignHeroToLoadout?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def AssignTeamPerkToLoadout(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/AssignTeamPerkToLoadout?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def AssignWorkerToSquad(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/AssignWorkerToSquad?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def AssignWorkerToSquadBatch(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/AssignWorkerToSquadBatch?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def AthenaPinQuest(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/AthenaPinQuest?profileId=athena&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def AthenaRemoveQuests(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/AthenaRemoveQuests?profileId=athena&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def AthenaTrackQuests(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/AthenaTrackQuests?profileId=athena&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def CancelOrResumeSubscription(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/CancelOrResumeSubscription?profileId=common_core&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def ChallengeBundleLevelUp(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ChallengeBundleLevelUp?profileId=athena&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def ClaimCollectedResources(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ClaimCollectedResources?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def ClaimCollectionBookRewards(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ClaimCollectionBookRewards?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def ClaimImportFriendsReward(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ClaimImportFriendsReward?profileId=common_core&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def ClaimMfaEnabled(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ClaimMfaEnabled?profileId=common_core&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def ClaimMissionAlertRewards(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ClaimMissionAlertRewards?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def ClaimSubscriptionRewards(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ClaimSubscriptionRewards?profileId=common_core&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def ClearHeroLoadout(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ClearHeroLoadout?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def CollectExpedition(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/CollectExpedition?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper

    @staticmethod
    def ConvertItem(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ConvertItem?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def ConvertLegacyAlterations(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ConvertLegacyAlterations?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def CraftWorldItem(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/CraftWorldItem?profileId=theater0&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def RecycleItem(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/RecycleItem?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper

    @staticmethod
    def RecycleItemBatch(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/RecycleItemBatch?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def RefreshExpeditions(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/RefreshExpeditions?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper

    @staticmethod
    def SetActiveHeroLoadout(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/SetActiveHeroLoadout?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def SetHomebaseBanner(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/SetHomebaseBanner?profileId=common_public&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def SetHomebaseName(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/SetHomebaseName?profileId=common_public&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def SetPinnedQuests(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/SetPinnedQuests?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def SkipTutorial(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/SkipTutorial?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def SkipTutorial(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/SkipTutorial?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def StartExpedition(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/StartExpedition?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def StorageTransfer(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/StorageTransfer?profileId=theater0&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def UnassignAllSquads(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/UnassignAllSquads?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper
    
    @staticmethod
    def SetGameplayStats(func):
        async def mcp(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token, account_id, payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]

            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            invite_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/SetGameplayStats?profileId=campaign&rvm=-1"

            async with aiohttp.ClientSession() as session:
                async with session.post(invite_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                            status = response.status
                            data = await response.json()
                            return status, data

        def wrapper(*args, **kwargs):
            return asyncio.run(mcp(*args, **kwargs))

        return wrapper