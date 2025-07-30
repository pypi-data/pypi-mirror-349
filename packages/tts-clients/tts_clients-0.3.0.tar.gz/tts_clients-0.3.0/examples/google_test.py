from dotenv import load_dotenv

from tts_clients.google.client import GoogleTTSClient
from tts_clients.google.models import TextToAudioRequest


load_dotenv()

client = GoogleTTSClient()
r = client.text_to_audio(TextToAudioRequest(text="こんにちは！", instructions="Say cheerfully", voice_name="Charon"))
r.save_mp3("test.mp3")
