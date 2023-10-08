import asyncio
from tests.voice_assistant import VoiceAssistant


async def main():
    voice_assistant = VoiceAssistant()
    await voice_assistant.listen_for_command()


asyncio.run(main())
