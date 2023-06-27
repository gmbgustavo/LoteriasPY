"""
Classe da Lotomania
"""

import secrets
import time

BET = 50
MIN_NUM = 1
MAX_NUM = 100
RANGEBET = range(MIN_NUM, MAX_NUM + 1)


class Lotomania:

    def __init__(self, *args, dezenas=50,):
        """
        Cria um objeto do tipo Lotofacil.
        :param args: Se vazio, cria um jogo surpresinha com a 50 dezenas
        """
        assert dezenas == 50, 'Aposta única de 50 dezenas'
        assert self.__checkargs(args), f'Lotomania usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        self.__gira_globo = secrets.SystemRandom()
        self.__jogo = self.__surpresinha(args)

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.sort()
        return str(l_exib)

    def __iter__(self):
        yield set(self.__jogo)

    def __len__(self):
        return BET

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 100
        :param fixos: Numeros pre estabelecidos
        :return: set
        """
        retorno = set(fixos)
        numeros = [x for x in RANGEBET if x not in retorno]    # Generator desconsidera os fixos
        self.__gira_globo.shuffle(numeros)
        while len(retorno) < BET:
            retorno.add(numeros.pop(secrets.randbelow(len(numeros))))
        return set(retorno)

    @staticmethod
    def __checkargs(numeros):
        if len(numeros) == 0:
            return True
        else:
            for i in numeros:
                if i not in RANGEBET:
                    return False
            return True

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
