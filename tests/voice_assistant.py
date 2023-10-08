import os
import io

import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import pygame

from config.config import SOUNDS_FOLDER


class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.recognized_language = 'en'
        self.active = True
        self.working = True

    def _play_sound(self, sound_path):
        pygame.init()
        pygame.mixer.init()
        try:
            sound = pygame.mixer.Sound(sound_path)
            sound.play()
            pygame.time.delay(int(sound.get_length() * 1000))
        except pygame.error as e:
            print(f"Error playing sound: {e}")

    async def _active(self):
        sound_path = os.path.join(SOUNDS_FOLDER, 'active_sound.mp3')
        self._play_sound(sound_path)
        self.active = True

    async def _deactivate(self):
        self.active = False

    async def _recognize_language(self, text):
        self.recognized_language = self.translator.detect(text).lang
        print(f"Detected language is {self.recognized_language}")

    async def _translate_text(self, text, src, dest='en'):
        translation = self.translator.translate(
            text,
            src=src,
            dest=dest
        )
        return translation.text

    async def _speak_text(self, text):
        translated_text = await self._translate_text(
            text,
            'en',
            self.recognized_language
        )
        tts = gTTS(text=translated_text, lang=self.recognized_language)

        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)
        self._play_sound(audio_data)

    async def listen_for_command(self):
        while self.working:
            try:
                with sr.Microphone() as mic:
                    print("Listing for command")

                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio_data = self.recognizer.listen(mic)

                    command = self.recognizer.recognize_google(
                        audio_data, language='pl-PL'
                    ).lower()

                    print(f"Command received: {command}")
                    await self._recognize_language(command)

                    if ("hey siby" in command or "hey sibi" in command) and not self.active:
                        print("Activating Siby")
                        await self._active()
                    elif self.active:
                        command_en = await self._translate_text(
                            command,
                            self.recognized_language
                        )
                        print("Executing command", command_en)
                        if 'say hello' in command_en:
                            await self._speak_text("Hi")
                        await self._speak_text(command_en)
                    else:
                        response_text = "I couldn't understand the command"
                        await self._speak_text(response_text)
            except sr.UnknownValueError:
                response_text = "I couldn't understand the command"
                await self._speak_text(response_text)
                await self._deactivate()
                continue
            except sr.RequestError as e:
                await self._deactivate()
                print(f"Error with the speech recognition service: {e}")
                continue
