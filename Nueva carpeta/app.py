import os
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request
import json
from my_transcriber import Transcriber
from llm import LLM
from tts import TTS
from pc_command import PcCommand

load_dotenv()
openai.api_key = os.getenv ('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')
elevenlabs_key = os.getenv ('dfe272ff5841262653d5418e33acfb8c')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    audio = request.files.get("audio")
    
    if audio is not None:
        text = Transcriber().transcribe(audio)
        
        llm = LLM()
        function_name, args, message = llm.process_functions(text)
        if function_name is not None:
            
            if function_name == "open_chrome":
                PcCommand().open_chrome(args["website"])
                final_response = "Listo, ya abrí chrome en el sitio " + args["website"]
                tts_file = TTS().process(final_response)
                if tts_file is not None:
                    tts_file.save("audio.mp3")
                return {"result": "ok", "text": final_response, "file": tts_file}
            
            elif function_name == "dominate_human_race":
                final_response = "No te creas."
                tts_file = TTS().process(final_response)
                if tts_file is not None:
                    tts_file.save("audio.mp3")
                return {"result": "ok", "text": final_response, "file": tts_file}
        else:
            final_response = "No tengo idea de lo que estás hablando"
            tts_file = TTS().process(final_response)
            if tts_file is not None:
                tts_file.save("audio.mp3")
            return {"result": "ok", "text": final_response, "file": tts_file}
    else:
        return {"result": "error", "message": "No se ha subido ningún archivo de audio"}

if __name__ == "__main__":
    app.run()
