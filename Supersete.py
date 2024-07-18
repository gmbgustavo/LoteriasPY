"""
Classe do Supersete
"""

import time
from API.random_api import get_numbers


BET = 7
MIN_NUM = 0
MAX_NUM = 9
RANGEBET = range(MIN_NUM, MAX_NUM + 1)


class Supersete:

    def __init__(self, *args, dezenas=7):
        self.__colunas = {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1}
        assert len(args) == 7 or len(args) == 0, f'Deve-se informar 7 numeros ou nenhum.'
        self.__dezenas = dezenas
        self.__fixos = args
        if len(self.__fixos) == 0:
            self.__jogo = self.__surpresinha()
        else:
            self.__jogo = {i+1: args[i] for i in range(BET)}

    def __repr__(self):
        strout = '|'
        for n in self.__jogo.values():
            strout += str(n) + ' | '
        return strout

    def __len__(self):
        return BET

    def __iter__(self):
        yield self.__jogo

    def __surpresinha(self) -> dict:
        time.sleep(0.2)    # Limita a consulta a API
        numeros = get_numbers(n=BET, min_val=MIN_NUM, max_val=MAX_NUM, repeat=True)    # Pode repetir os numeros
        assert len(numeros) == BET
        coluna = 1
        for unidade in numeros:
            self.__colunas[coluna] = unidade
            coluna += 1
        return self.__colunas

    @property
    def jogo(self):
        return self.__jogo


if __name__ == '__main__':
    quit(3)






