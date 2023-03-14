"""
Classe da Dupla Sena - Sao dois sorteios por jogo
"""

import secrets
import time

MIN_BET = 6
MAX_BET = 15
MIN_NUM = 1
MAX_NUM = 50
RANGEBET = range(MIN_NUM, MAX_NUM + 1)


class Duplasena:

    def __init__(self, *args, dezenas):
        """
        Cria um objeto do tipo Duplasena.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=6)
        :param dezenas: Quantidade de dezenas da aposta (6-15)
        """
        assert len(args) <= MAX_BET, f'Esperado no máximo {MAX_BET} dezenas. (Passadas {len(args)})'
        assert MIN_BET <= dezenas <= MAX_BET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MIN_BET} e {MAX_BET}. (Passadas {dezenas})'
        assert self.__checkargs(args), f'Duplasena aceita números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        assert len(args) <= dezenas, f'Quantidade de números informados incompativel com o argumento "dezenas"'
        self.__gira_globo = secrets.SystemRandom()
        self.__dezenas = dezenas
        self.__jogo = self.__surpresinha(set(args))

    @staticmethod
    def __checkargs(numeros):
        if len(numeros) == 0:
            return True
        else:
            for i in numeros:
                if i not in RANGEBET:
                    return False
            return True

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.sort()
        return str(l_exib)

    def __iter__(self):
        yield set(self.__jogo)

    def __len__(self):
        return self.__dezenas

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 50
        :return: set
        """
        retorno = set(fixos)
        numeros = [x for x in RANGEBET if x not in retorno]    # Generator desconsidera os fixos
        while len(retorno) < self.__dezenas:
            self.__gira_globo.shuffle(numeros)
            time.sleep(0.1)
            retorno.add(numeros.pop(secrets.randbelow(len(numeros))))
            time.sleep(0.25)    # Aumenta a aleatoriedade
        return set(retorno)

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
