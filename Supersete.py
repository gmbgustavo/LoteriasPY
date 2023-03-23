"""
Classe da Super Sete
Para apostar deve ser passado um dicionario com a chave sendo o numero da coluna (int)
e os valores uma tupla, de tamanho 1 a 3, com cada uma contendo numeros de 0 a 9
"""

import secrets
import time
import numpy as np

MAX_NUM_COL = 3
MIN_NUM_COL = 1
MIN_NUM = 0
MAX_NUM = 9
MIN_BET = 7
MAX_BET = 7
RANGEBET = range(MIN_NUM, MAX_NUM + 1)
JOGO = {1: (-1,), 2: (-1,), 3: (-1,), 4: (-1,), 5: (-1,), 6: (-1,), 7: (-1,)}


class Supersete:

    def __init__(self, aposta: dict, dezenas=7):
        """
        Cria um objeto do tipo Megasena.
        :param aposta: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=7)
               esse parâmetro deve ser passado como um dicionario de chave int e valor tupla
        :param dezenas: Quantidade de dezenas da aposta (7-15)
        """
        assert len(aposta) <= MAX_BET, f'Esperado no máximo {MAX_BET} dezenas. (Passadas {len(aposta)})'
        assert MIN_BET <= dezenas <= MAX_BET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MIN_BET} e {MAX_BET}. (Foi informado {dezenas})'
        assert len(aposta) <= dezenas, f'Quantidade de números informados incompativel com o argumento "dezenas"'
        assert self.__checkargs(aposta), f'Megasena usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        self.__dezenas = dezenas
        self.__jogo = self.__surpresinha(aposta)

    def __distribuir(self, fixos):
        pass

    @staticmethod
    def __checkargs(numeros: dict):
        if len(numeros) == 0:
            return True
        else:
            for i in numeros.values():
                for x in i:
                    if x not in RANGEBET:
                        return False
            return True

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 60
        :return: set
        """
        retorno = JOGO
        numeros = [x for x in RANGEBET]    # Generator desconsidera fixos
        coluna = 1
        while len(retorno) < self.__dezenas:
            retorno[coluna] = (numeros.pop(secrets.randbelow(len(numeros))),)
            time.sleep(0.1)    # Aumenta a entropia
            coluna += 1
        return set(retorno)

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
