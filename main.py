import asyncio
import os

from classes.discord_bot import DiscordBot
from config.enviroment import TOKEN
from config.config import COGS_FOLDER


async def setup(bot):
    for filename in os.listdir(COGS_FOLDER):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    discord_bot = DiscordBot()
    await setup(discord_bot)
    await discord_bot.start(TOKEN)


asyncio.run(main())
