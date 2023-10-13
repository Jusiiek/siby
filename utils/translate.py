from discord.app_commands import Choice
from googletrans import Translator, LANGUAGES


translator = Translator()


def recognize_language(text):
    return translator.detect(text).lang


def translate_text(text, src, dest):
    if src == 'auto':
        src = recognize_language(text)
    translation = translator.translate(
        text=text,
        src=src,
        dest=dest
    )
    return src, translation.text


def get_languages():
    languages = [
        {'name': name.title(), 'value': code}
        for code, name in LANGUAGES.items()
    ]
    return languages


def get_language_choices(add_auto=False):
    language_choices = get_languages()
    language_choices = [
        Choice(name=lang['name'], value=lang['value'])
        for lang in language_choices
    ]
    if add_auto:
        language_choices.insert(
            0, Choice(name='Auto', value='auto')
        )
    return language_choices
