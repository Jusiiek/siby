import discord
from discord import app_commands
from discord.ext import commands

from config.enviroment import SERVER_ID, ADMINS_IDS


class Base(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _set_status(self):
        await self.bot.change_presence(activity=discord.Game('Existence'))

    @app_commands.command(name='change_bot_status', description='Set new status for the bot')
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def change_bot_status(self, interaction: discord.Interaction):
        await self.bot.change_presence(activity=discord.Game('Chilling'))
        await interaction.response.send_message("Changed bot status", ephemeral=True)

    @commands.command()
    async def sync(self, ctx: commands.Context) -> None:
        print("Trying to sync")
        print(
            f"User {ctx.author.name} with id {ctx.author.id}" +
            f" trying to use sync command \n" +
            f"Is users in admins: {ctx.author.id in ADMINS_IDS}"

        )
        if ctx.author.id in ADMINS_IDS:
            fmt = await self.bot.tree.sync(guild=ctx.guild)
            await ctx.send(
                f"Synced {len(fmt)} commands to the current guild."
            )
        else:
            await ctx.send('You must be the owner to use this command!')

    @commands.Cog.listener()
    async def on_ready(self):
        await self._set_status()
        print(f'Loaded base commands.')


async def setup(bot: commands.Bot):
    await bot.add_cog(Base(bot))
