
import io
import wave
from typing import Literal

from pydantic import BaseModel


VoiceNameTypes = Literal[
    "Zephyr",  # 明るい
    "Puck",  # アップビート
    "Charon",  # 情報提供
    "Kore",  # 会社
    "Fenrir",  # 興奮しやすい
    "Leda",  # 若々しい
    "Orus",  # 会社
    "Aoede",  # Breezy
    "Callirhoe",  # 気楽な
    "Autonoe",  # 明るい
    "Enceladus",  # 息づかい
    "Iapetus",  # クリア
    "Umbriel",  # 気楽な
    "Algieba",  # スムーズ
    "Despina",  # スムーズ
    "Erinome",  # クリア
    "Algenib",  # 砂利
    "Rasalgethi",  # 情報に富んでいる
    "Laomedeia",  # アップビート
    "Achernar",  # ソフト
    "Alnilam",  # 確実
    "Schedar",  # Even
    "Gacrux",  # 成人向け
    "Pulcherrima",  # 前方
    "Achird",  # フレンドリー
    "Zubenelgenubi",  # カジュアル
    "Vindemiatrix",  # 優しい
    "Sadachbia",  # 活発
    "Sadaltager",  # 知識豊富
    "Sulafar",  # 温かい
]


class TextToAudioRequest(BaseModel):
    text: str
    instructions: str
    voice_name: VoiceNameTypes = "Kore"


class TextToAudioResponse(BaseModel):
    audio: bytes

    @classmethod
    def from_bytes(cls, audio: bytes) -> "TextToAudioResponse":
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(audio)
        return cls(audio=buf.getvalue())

    def save_wav(self, path: str):
        if not path.endswith(".wav"):
            raise ValueError("path must end with .wav")
        with open(path, "wb") as f:
            f.write(self.audio)
