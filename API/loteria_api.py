import requests
import json
import time
import os
import dotenv

# API INIT
dotenv.load_dotenv(encoding="UTF-8")
CHAVE_LOCA = os.getenv("CHAVE_LOCA")


def get_numbers(n=5, min_val=1, max_val=60, repeat=False):
    time.sleep(0.2)
    url = "https://api.random.org/json-rpc/4/invoke"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",    # Gera apenas números inteiros. Para outros ver documentação.
        "params": {
            "apiKey": CHAVE_LOCA,
            "n": n,
            "min": min_val,
            "max": max_val,
            "replacement": repeat
        },
        "id": 1
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        if "result" in result and "random" in result["result"]:
            return sorted(result["result"]["random"]["data"])
        else:
            return "Erro: A chave 'random' não consta na string de resposta."
    else:
        return f"Erro: Response status code {response.status_code}"


if __name__ == '__main__':
    quit(3)
