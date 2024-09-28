from django.urls import path
from .views import TextToSpeechAPI, voice_assistant

urlpatterns = [
    path('api/convert', TextToSpeechAPI.as_view(), name='convert'),
    path('', voice_assistant, name='voice_assistant'),  

    ]