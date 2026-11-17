from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, RequestBlocked
)
import os
import re
import sys
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv


LIMITE_CARACTERES = 200_000  # limite de segurança de custo; ajuste conforme o seu plano
HOSTS_YOUTUBE = {'youtube.com', 'www.youtube.com', 'm.youtube.com', 'music.youtube.com'}


def extrair_video_id(link):
    """Aceita somente URLs do YouTube e devolve um ID de 11 caracteres, ou None."""
    link = link.strip()
    partes = urlparse(link if '://' in link else 'https://' + link)
    host = (partes.hostname or '').lower()
    if partes.scheme not in ('http', 'https'):
        return None
    if host == 'youtu.be':
        candidato = partes.path.lstrip('/').split('/')[0]
    elif host in HOSTS_YOUTUBE and partes.path == '/watch':
        candidato = (parse_qs(partes.query).get('v') or [''])[0]
    else:
        return None
    return candidato if re.fullmatch(r'[A-Za-z0-9_-]{11}', candidato) else None

load_dotenv()

client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

user_video = input('Digite o link do vídeo do YouTube a ser resumido: ')

video_id = extrair_video_id(user_video)
if video_id is None:
    print("Formato de link não reconhecido. Certifique-se de ser uma URL do YouTube.")
    sys.exit(1)

ytt_api = YouTubeTranscriptApi()

try:
    transcricao = ytt_api.fetch(video_id, languages=['pt', 'en'])
    texto_completo = " ".join(bloco.text for bloco in transcricao)
    if len(texto_completo) > LIMITE_CARACTERES:
        print(f"Aviso: transcrição cortada em {LIMITE_CARACTERES} caracteres para limitar o consumo.")
        texto_completo = texto_completo[:LIMITE_CARACTERES]

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
except Exception as erro:
    # Não exibir a mensagem completa: ela pode conter dados de proxy ou da requisição.
    print(f"Falha inesperada ({type(erro).__name__}). Verifique as chaves no .env e a conexão.")
    sys.exit(1)
