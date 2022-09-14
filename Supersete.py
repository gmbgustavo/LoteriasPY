"""
Classe da Super Sete
Devem ser passados os números em ordem das colunas
Para marcar mais de um numero por coluna, forneça uma tupla ao inves de um inteiro
"""

import secrets

MAX_NUM_COL = 3
MIN_NUM_COL = 1
COLUNAS = {1: (), 2: (), 3: (), 4: (), 5: (), 6: (), 7: ()}
RANGEBET = range(0, 9)
MIN_BET = 7
MAX_BET = 21


class Supersete:

    def __init__(self, *args, num_col=MIN_NUM_COL, dezenas=MIN_BET):
        assert MIN_NUM_COL <= num_col <= MAX_NUM_COL and isinstance(num_col, int), \
            f'Minimo {MIN_NUM_COL}, máximo {MAX_NUM_COL} numeros por coluna. (Fornecido {num_col})'
        self.__num_col = num_col
        self.__dezenas = dezenas
        self.__jogada = args
        self.__jogo = COLUNAS
        self.__distribuir(self.__jogada)

    def __distribuir(self, numeros: tuple):
        for coluna in COLUNAS.keys():
            self.__jogo[coluna] = numeros[coluna - 1]
        print(self.__jogo)

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 50
        :return: set
        """
        count = len(RANGEBET)
        retorno = set(fixos)  # Apenas no caso de gerador
        numeros = [x for x in range(1, count + 1)]
        while len(retorno) < self.__:
            retorno.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
        return set(retorno)


if __name__ == '__main__':
    # print('Essa classe deve ser apenas instanciada internamente.')

    a = Supersete((5, 0), 9, 0, 6, 9, 7, 2)
