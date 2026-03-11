from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
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
    print("Formato de link não reconhecido. Certifique-se de ser uma URL do YouTube.")
    exit()
ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username=os.getenv('proxy_user'),
        proxy_password=os.getenv('proxy_pw')
    )
)

try:
    transcricao = ytt_api.fetch(video_id, languages=['pt', 'en'])
    texto_completo = " ".join(bloco.text for bloco in transcricao)
    # caso queira limitar caracteres pra não queimar os tokens da ia: texto_completo = texto_completo[:20000]
    briefing = f"""
    Atue como um analista de conteúdo de YouTube.
    Leia a transcrição bruta do vídeo abaixo e crie um resumo profissional.
    Transcrição: {texto_completo}
    """

    resposta = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=briefing
    )
    print(resposta.text)

except TranscriptsDisabled:
    print("Legendas desativadas para este vídeo.")
except NoTranscriptFound:
    print("Nenhuma transcrição encontrada em Português ou Inglês.")
except VideoUnavailable:
    print("Vídeo indisponível ou ID inválido.")
except RequestBlocked:
    print("IP bloqueado pelo YouTube. Verifique o proxy.")