import discord
from discord import app_commands, Interaction
from discord.ext import commands


from utils.translate import translate_text, get_languages
from config.enviroment import SERVER_ID

from cogs.base import Base


class Translator(Base):
    @app_commands.command(name='translate_text', description='Translate text')
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def translate_text(self, interaction: Interaction, text: str, src_from: str, to: str):
        try:
            src, translated_text = translate_text(
                text, src_from, to
            )
            await interaction.response.send_message(
                (
                    f"{interaction.user} only you can this!\n" +
                    f"Original Text ({src}): {text}\n" +
                    f"Translated Text ({to}): {translated_text}"
                ),
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                (
                    f"{interaction.user} only you can this!\n" +
                    "Something went wrong"
                ),
                ephemeral=True
            )
            print(f"Exception: {str(e)}")

    @app_commands.command(name='show_available_languages', description='Translate text')
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def show_list_of_languages(self, interaction: Interaction):

        languages = get_languages()
        languages.insert(0, {'name': 'Auto', 'value': 'auto'})
        languages = [f"{lang['value']}: {lang['name']}" for lang in languages]
        try:
            await interaction.response.send_message(
                (
                    "LIST OF LANGUAGES\n" +
                    "WARNING!!  auto works only for src_from!!\n" +
                    "\n ".join(languages)

                ), ephemeral=True
            )
        except Exception as e:
            print(f"Exception: {str(e)}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Translator(bot))
