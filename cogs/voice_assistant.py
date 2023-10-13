import os
import io

import discord
from discord.ext import commands, tasks

import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import pygame

from config.config import SOUNDS_FOLDER
from config.enviroment import (
    SERVER_ID,
    MAIN_VC_CHANNEL_ID
)


class VoiceAssistant(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.recognized_language = 'en'
        self.connected_voice_channel = None
        self.active = False

    def _play_sound(self, sound_path):
        pygame.init()
        pygame.mixer.init()
        try:
            sound = pygame.mixer.Sound(sound_path)
            sound.play()
            pygame.time.delay(int(sound.get_length() * 1000))
        except pygame.error as e:
            print(f"Error playing sound: {e}")

    async def _join_voice_channel(self, vc_id):
        print("_join_voice_channel")
        voice_channel = discord.utils.get(self.bot.get_all_channels(), id=vc_id)
        if voice_channel:
            print("FOUND voice_client", voice_channel)
            print(type(voice_channel))
            voice_client = discord.utils.get(self.bot.voice_clients, guild=self.bot.get_guild(SERVER_ID))
            if voice_channel.members and not voice_client.is_connected():
                await voice_client.connect()
            elif voice_client.is_connected():
                await voice_channel.disconnect()

    async def _active(self):
        if self.connected_voice_channel:
            sound_path = os.path.join(SOUNDS_FOLDER, 'active_sound.mp3')
            self._play_sound(sound_path)
            self.active = True

    async def _deactivate(self):
        self.active = False

    async def _recognize_language(self, text):
        self.recognized_language = self.translator.detect(text).lang
        print(f"Detected language is {self.recognized_language}")

    async def _speak_text(self, text):
        await self._recognize_language(text)
        translated_text = await self._translate_text(
            text,
            'en',
            self.recognized_language
        )
        tts = gTTS(text=translated_text, lang=self.recognized_language)

        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        if self.connected_voice_channel:
            self._play_sound(audio_data)

    async def _translate_text(self, text, src, dest='en'):
        translation = self.translator.translate(
            text,
            src=src,
            dest=dest
        )
        return translation.text

    @tasks.loop(seconds=10)
    async def check_channel(self):
        print('CHEKING CHANNEL')
        await self._join_voice_channel(MAIN_VC_CHANNEL_ID)

    @commands.Cog.listener()
    async def listen_for_command(self):
        try:
            with sr.Microphone() as mic:
                print("Listing for command")

                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio_data = self.recognizer.listen(mic)
                command = self.recognizer.recognize_google(
                    audio_data, language='pl-PL'
                ).lower()

                await self._recognize_language(command)
                print(f"Command received: {command}")

                if "hey siby" in command or "hey sibi" in command:
                    print("Activating Siby")
                    await self._active()
                elif self.active:
                    command_en = await self._translate_text(
                        command,
                        self.recognized_language
                    )
                    print("Executing command", command_en)
                    if 'ping' in command_en:
                        await self.ping()
                    await self._speak_text(command_en)

        except sr.UnknownValueError:
            response_text = "I couldn't understand the command"
            await self._speak_text(response_text)
            await self._deactivate()
        except sr.RequestError as e:
            await self.connected_voice_channel.send("Error with the speech recognition service")
            await self._deactivate()
            print(f"Error with the speech recognition service: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded VoiceAssistant commands.')
        await self.check_channel()

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send("Ping")
        if self.connected_voice_channel:
            await self.connected_voice_channel.send("Ping")


async def setup(bot):
    await bot.add_cog(VoiceAssistant(bot))
