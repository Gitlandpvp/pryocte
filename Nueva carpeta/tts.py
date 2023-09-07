import os
from dotenv import load_dotenv
import requests

class TTS():
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('dfe272ff5841262653d5418e33acfb8c')
    
    def process(self, text):
        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.key
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v1",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.55
            }
        }

        #Lo guarda en static/response.mp3 para que el sitio web
        #pueda leerlo y reproducirlo en el explorador
        file_name = "response.mp3"
        response = requests.post(url, json=data, headers=headers)
        with open("static/" + file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
                    
        return file_name