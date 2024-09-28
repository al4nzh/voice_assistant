from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
import openai
from rest_framework.response import Response
from TTS.api import TTS
import uuid
import whisper
import os
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()
openai.api_key = settings.OPEN_API_KEY
model = whisper.load_model("base")
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
from django.shortcuts import render

def voice_assistant(request):
    return render(request, 'tts_app/index.html')


def speech_to_text(audio_file):
    result = model.transcribe(audio_file)
    return result['text']

class TextToSpeechAPI(APIView):
    def post(self, request):
        audio_dir = os.path.join(settings.BASE_DIR, 'static', 'tts')
        audio_file = request.FILES['audio_file']
        audio_file_path = os.path.join(audio_dir, audio_file.name)
        with open(audio_file_path, 'wb') as f:
                    for chunk in audio_file.chunks():
                        f.write(chunk)
        user_input = speech_to_text(audio_file_path)
        messages = [{"role": "system", "content": "You are kind assistant"}]
        messages.append({"role": "user", "content": user_input})
        chat = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        audio_output_path = os.path.join(audio_dir, 'response_audio.mp3')  
        tts_model.tts_to_file(text=reply, file_path=audio_output_path)
        audio_url = '/static/tts/response_audio.mp3'
        return Response({'text': reply, 'audio_url': audio_url}, status=status.HTTP_200_OK)