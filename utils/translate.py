from discord import SelectOption
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
