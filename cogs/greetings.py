import discord
from discord import app_commands
from discord.ext import commands

from config.enviroment import WELCOME_CHANNEL_ID, SERVER_ID

from cogs.base import Base


class Greetings(Base):
    @app_commands.command(name='say_hello', description='Say hello to yourself')
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def say_hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Hello {interaction.user.display_name}')

    @commands.Cog.listener(name='on_member_join')
    async def on_member_join(self, member: discord.Member):
        print(f'Member {member.display_name} has joined to sever.')
        guild = self.__bot.get_guild(SERVER_ID)
        channel = self.__bot.get_channel(WELCOME_CHANNEL_ID)
        if channel is not None:
            await channel.send(f'Welcome to the {guild.name} Discord Server, {member.mention} !  :partying_face:')


async def setup(bot: commands.Bot):
    await bot.add_cog(Greetings(bot))
