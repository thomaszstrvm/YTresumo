# YT Resumo

Script Python que transcreve vídeos do YouTube e gera um resumo profissional usando a API do Gemini (Google GenAI).

## Funcionalidades

- Aceita links nos formatos `youtube.com/watch?v=...` e `youtu.be/...`
- Busca transcrição automática em Português ou Inglês
- Gera resumo com tópicos e conclusões usando o modelo `gemini-2.5-flash`
- Suporte opcional a proxy (Webshare) para evitar bloqueios do YouTube

## Pré-requisitos

- Python 3.8+
- Conta na [Google AI Studio](https://aistudio.google.com/) para obter a chave da API Gemini
- Conta no [Webshare](https://www.webshare.io/) (opcional, necessário se seu IP for bloqueado pelo YouTube)

## Instalação

Instale as dependências:

```bash
pip install google-genai youtube-transcript-api python-dotenv
```

Configure as variáveis de ambiente criando um arquivo `.env`:

```env
GOOGLE_API_KEY=sua_chave_gemini
proxy_user=seu_usuario_webshare
proxy_pw=sua_senha_webshare
```

## Uso

```bash
python yt_resumo.py
```

O script pedirá o link do vídeo:

```
Digite o link do vídeo do YouTube a ser resumido: https://www.youtube.com/watch?v=...
```
## O script irá:

Extrair a transcrição do vídeo

Enviar o texto para a API Gemini

Gerar um resumo estruturado
## Estrutura do Projeto

```
yt-resumo/
├── .env              # Variáveis de ambiente (não versionar)
├── .gitignore
├── requirements.txt
├── README.md
└── yt_resumo.py      # Script principal
```

## requirements.txt

```
google-genai
youtube-transcript-api
python-dotenv
```

## Limitações

- O vídeo precisa ter legendas disponíveis em Português ou Inglês
- Vídeos muito longos podem consumir muitos tokens — descomente a linha `texto_completo = texto_completo[:20000]` no script para limitar
- O YouTube pode bloquear IPs que fazem muitas requisições seguidas. Se isso acontecer, na página do youtube-transcript-api
  (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception) tem um passo a passo ensinando como usar proxies e reverter a situação

## Licença

MIT