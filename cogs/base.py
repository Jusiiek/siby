import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from config.enviroment import SERVER_ID, ADMINS_IDS


class Base(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Loaded {self.__class__.__name__} commands.")


class Basics(Base):
    @app_commands.command(name='change_bot_status', description='Set new status for the bot')
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    @app_commands.choices(
        status=[
            Choice(name='Game', value='game'),
            Choice(name='Streaming', value='streaming'),
            Choice(name='Watching', value='watching'),
            Choice(name='Listening', value='listening'),
        ]
    )
    async def change_bot_status(
            self, interaction: discord.Interaction, status: Choice[str], name: str, url: str = ''
    ):
        if status == 'streaming' and not url:
            await interaction.response.send_message(
                f"The url is required for status {status}", ephemeral=True
            )

        match status:
            case 'game':
                await self.__bot.change_presence(activity=discord.Game(name))
            case 'streaming':
                await self.__bot.change_presence(
                    activity=discord.Streaming(
                        name=name, url=url
                    )
                )
            case 'watching':
                await self.__bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching, name=name
                    )
                )
            case 'listening':
                await self.__bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.listening, name=name
                    )
                )
        await interaction.response.send_message(
            "Updated bot status", ephemeral=True
        )

    @commands.command()
    async def sync(self, ctx: commands.Context) -> None:
        print("Trying to sync")
        print(
            f"User {ctx.author.name} with id {ctx.author.id}" +
            f" trying to use sync command \n" +
            f"Is users in admins: {ctx.author.id in ADMINS_IDS}"

        )
        if ctx.author.id in ADMINS_IDS:
            fmt = await self.__bot.tree.sync(guild=ctx.guild)
            await ctx.send(
                f"Synced {len(fmt)} commands to the current guild."
            )
        else:
            await ctx.send('You must be the owner to use this command!')


async def setup(bot: commands.Bot):
    await bot.add_cog(Basics(bot))
