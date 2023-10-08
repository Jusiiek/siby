import discord
from discord.ext import commands


class DiscordBot(commands.Bot):
    intents = discord.Intents.all()
    intents.message_content = True

    def __init__(self):
        super().__init__(command_prefix='$', intents=self.intents)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot {self.user.display_name} is connected to server.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error:commands.CommandError):
        if error:
            await ctx.send('Command not found')
