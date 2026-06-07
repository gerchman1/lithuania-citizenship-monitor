import requests
import json
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://e-seimas.lrs.lt/portal/documentSearch/lt"

ARQUIVO = "ultimo.txt"

try:
    with open(ARQUIVO, "r") as f:
        ultimo = f.read().strip()
except:
    ultimo = ""

pagina = requests.get(URL)

texto = pagina.text

if texto != ultimo:

    mensagem = (
        "Possível atualização encontrada "
        "na busca de cidadania lituana.\n\n"
        f"{URL}"
    )

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": mensagem
        }
    )

    with open(ARQUIVO, "w") as f:
        f.write(texto)
