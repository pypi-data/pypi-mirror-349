from google import genai
from google.genai import types

from .models import TextToAudioRequest, TextToAudioResponse


class GoogleTTSClient:
    def __init__(self, model: str = "gemini-2.5-flash-preview-tts"):
        self.client = genai.Client()
        self.model = model

    def text_to_audio(self, req: TextToAudioRequest) -> TextToAudioResponse:
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{req.instructions}: {req.text}",
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=req.voice_name,
                        )
                    ),
                ),
            ),
        )
        data = response.candidates[0].content.parts[0].inline_data.data
        return TextToAudioResponse.from_bytes(data)
