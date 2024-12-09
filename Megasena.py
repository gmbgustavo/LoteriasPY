"""
Classe da Mega-Sena
"""

import time
from API.random_api import get_numbers

MAX_BET = 20
MIN_BET = 6
MIN_NUM = 1
MAX_NUM = 60
RANGEBET = range(MIN_NUM, MAX_NUM + 1)


class Megasena:

    def __init__(self, *args, dezenas=MIN_BET):
        """
        Cria um objeto do tipo Megasena.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=6)
        :param dezenas: Quantidade de dezenas da aposta (6-15)
        """
        assert len(args) <= MAX_BET, f'Esperado no máximo {MAX_BET} dezenas. (Passadas {len(args)})'
        assert MIN_BET <= dezenas <= MAX_BET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MIN_BET} e {MAX_BET}. (Foi informado {dezenas})'
        assert len(args) <= dezenas, f'Quantidade de números informados incompativel com o argumento "dezenas"'
        assert self.__checkargs(args), f'Megasena usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        self.__dezenas = dezenas
        self.__jogo = self.__surpresinha(set(args))

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.sort()
        return str(l_exib)

    def __iter__(self):
        yield set(self.__jogo)

    def __len__(self):
        return self.__dezenas

    @staticmethod
    def __checkargs(numeros):
        if len(numeros) == 0:
            return True
        else:
            for i in numeros:
                if i not in RANGEBET:
                    return False
            return True

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 60
        :return: set
        """
        gerados = len(fixos)
        qtde = self.__dezenas - len(fixos)
        if qtde <= 0:
            return set(fixos)
        time.sleep(0.2)
        while len(fixos) < self.__dezenas:
            if qtde >= 1:
                apicall = get_numbers(n=qtde, min_val=MIN_NUM, max_val=MAX_NUM, repeat=False)
                numeros = [x for x in apicall if x not in fixos]    # Generator desconsidera fixos
                for dez in numeros:
                    fixos.add(dez)
                gerados = len(fixos)
            qtde = self.__dezenas - gerados
        return set(fixos)

    def sorteio(self):
        return self.__surpresinha()

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    quit(3)
