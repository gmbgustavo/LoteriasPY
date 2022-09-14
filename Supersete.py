"""
Classe da Super Sete
Para apostar deve ser passado um dicionario com a chave sendo o numero da coluna (int)
e os valores uma tupla, de tamanho 1 a 3, com cada uma contendo numeros de 0 a 9
"""

import secrets

MAX_NUM_COL = 3
MIN_NUM_COL = 1
COLUNAS = {1: (), 2: (), 3: (), 4: (), 5: (), 6: (), 7: ()}
RANGEBET = range(0, 9)
MIN_BET = 7
MAX_BET = 21


class Supersete:

    def __init__(self, aposta: dict, num_col=MIN_NUM_COL, dezenas=MIN_BET):
        assert MIN_NUM_COL <= num_col <= MAX_NUM_COL and isinstance(num_col, int), \
            f'Minimo {MIN_NUM_COL}, máximo {MAX_NUM_COL} numeros por coluna. (Fornecido {num_col})'
        self.__num_col = num_col
        self.__dezenas = dezenas
        self.__jogo = aposta
        self.__distribuir(self.__jogo)

    def __distribuir(self, numeros: dict):
        for coluna in COLUNAS.keys():
            self.__jogo[coluna] = numeros[coluna]
        print(self.__jogo)

    def __checkargs(self, aposta, dezenas):
        pass


if __name__ == '__main__':
    # print('Essa classe deve ser apenas instanciada internamente.')

    a = Supersete({1: (0,), 2: (5,), 3: (9,), 4: (8,), 5: (0,), 6: (7,), 7: (3,)})
