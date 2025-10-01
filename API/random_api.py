"""Codigo para chamadas API do serviço RANDOM.ORG"""

import requests
import json
import time
import os
import dotenv

# API INIT
dotenv.load_dotenv(encoding="UTF-8")
CHAVE_API_RANDOM_ORG = os.getenv("CHAVE_LOCA")
if not CHAVE_API_RANDOM_ORG:
    raise ValueError("Chave da API não encontrada no .env!")


def get_numbers(n: int, min_val: int, max_val: int, repeat=False):
    time.sleep(0.1)
    url = "https://api.random.org/json-rpc/4/invoke"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",    # Gera apenas números inteiros. Para outros ver documentação.
        "params": {
            "apiKey": CHAVE_API_RANDOM_ORG,
            "n": n,
            "min": min_val,
            "max": max_val,
            "replacement": repeat
        },
        "id": 1
    }

    response = requests.post(url=url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        if "result" in result and "random" in result["result"]:
            return result["result"]["random"]["data"]
        else:
            raise IndexError("Erro: A chave 'random' não consta na string de resposta.\nVerifique a"
                             "disponibilidade da API ou limite de uso.")
    else:
        raise ConnectionError(f"Erro: Response status code {response.status_code}")


if __name__ == '__main__':
    quit(3)
