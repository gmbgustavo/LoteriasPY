"""
Classe da Super Sete
Para apostar deve ser passado um dicionario com a chave sendo o numero da coluna (int)
e os valores uma tupla, de tamanho 1 a 3, com cada uma contendo numeros de 0 a 9
"""

import secrets

MAX_NUM_COL = 3
MIN_NUM_COL = 1
COLUNAS = {1: (), 2: (), 3: (), 4: (), 5: (), 6: (), 7: ()}
RANGEBET = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
MIN_BET = 7
MAX_BET = 21


class Supersete:

    def __init__(self, aposta=None):
        assert self.__checkargs(aposta), 'São válidos numeros entre 0 e 9 como valor das colunas'
        assert self.__checktuple(aposta), 'Permitido no máximo 3 números por coluna'
        if aposta is not None:
            self.__dezenas = len(aposta)
        else:
            self.__dezenas = MIN_BET
        self.__jogo = aposta
        self.__distribuir(self.__jogo)

    def __distribuir(self, numeros: dict):
        for coluna in self.__jogo.keys():
            self.__jogo[coluna] = numeros[coluna]
        print(self.__jogo)

    @staticmethod
    def __checkargs(aposta):
        if aposta is None:
            return True
        for i in aposta.values():
            if i[0] not in RANGEBET:
                return False
        return True

    @staticmethod
    def __checktuple(aposta):
        if aposta is None:
            return True
        for i in aposta.values():
            if 1 <= len(i) <= 3:
                return True
        return False


if __name__ == '__main__':
    # print('Essa classe deve ser apenas instanciada internamente.')

    a = Supersete()
