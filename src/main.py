import discord 
from discord.ext import commands 
import loader
import asyncio

async def main():
    async with loader.bot:
        await loader.load_extensions()
        await loader.bot.start(loader.token.token)


asyncio.run(main())