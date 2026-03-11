from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, RequestBlocked
)
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

user_video = input('Digite o link do vídeo do YouTube a ser resumido: ')

if "v=" in user_video:
    video_id = user_video.split('v=')[1].split('&')[0]
elif "youtu.be/" in user_video:
    video_id = user_video.split('youtu.be/')[1].split('?')[0]
else:
    print("Formato de link não reconhecido.")
    exit()

ytt_api = YouTubeTranscriptApi()

try:
    transcricao = ytt_api.fetch(video_id, languages=['pt', 'en'])
    texto_completo = " ".join(bloco.text for bloco in transcricao)

    #caso queira limitar caracteres pra não queimar os tokens da ia: texto_completo = texto_completo[:20000]

    briefing = f"""
    Você é um especialista em análise de conteúdo do YouTube.

    Leia a transcrição abaixo e produza:
    - Um resumo claro do vídeo
    - Principais tópicos abordados
    - Conclusões importantes

    Transcrição:
    {texto_completo}
    """

    resposta = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=briefing
    )

    print(resposta.text)

except TranscriptsDisabled:
    print("Legendas desativadas para este vídeo.")
except NoTranscriptFound:
    print("Nenhuma transcrição encontrada.")
except VideoUnavailable:
    print("Vídeo indisponível ou ID inválido.")
except RequestBlocked:
    print("IP bloqueado pelo YouTube.")