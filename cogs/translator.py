import discord
from discord import app_commands
from discord.ext import commands


from utils.translate import (
    translate_text,
    get_language_choices
)
from config.enviroment import SERVER_ID


class Translator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='translate_text', description='Translate text')
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    @app_commands.choices(
        src_lang=get_language_choices(add_auto=True),
        to=get_language_choices()
    )
    async def translate_text(self, interaction: discord.Interaction, text: str, src_lang: str, to: str):
        src, translated_text = translate_text(text, src_lang, to)
        await interaction.response.send_message(
            (
                f"{interaction.user} only you can this!"
                f"Original Text ({src}): {text} \n"
                f"Translated Text ({to}): {translated_text}"
            ),
            ephemeral=True
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded translator commands.')


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Translator(bot), guilds=[discord.Object(id=SERVER_ID)]
    )
