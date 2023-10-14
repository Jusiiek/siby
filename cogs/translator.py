import discord
from discord import app_commands, Interaction
from discord.ext import commands


from utils.translate import translate_text, get_language_selects
from config.enviroment import SERVER_ID


class TranslatorModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.TextInput(
            label='Enter text to translate',
            placeholder='Type something...',
            custom_id='text_input',
            max_length=200,
            style=discord.TextStyle.long
        ))

        self.add_item(discord.ui.Select(
            placeholder='Translate from',
            options=get_language_selects(add_auto=True),
            custom_id='src_menu'
        ))
        self.add_item(discord.ui.Select(
            placeholder='Translate to',
            options=get_language_selects(),
            custom_id='to_menu'
        ))


class Translator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='translate_text', description='Translate text')
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def translate_text(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TranslatorModal())

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded translator commands.')


async def setup(bot: commands.Bot):
    await bot.add_cog(Translator(bot))
