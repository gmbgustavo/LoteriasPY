"""
Classe da +Milionária
"""

import secrets
import time

MAX_BET = 12
MIN_BET = 6
MIN_NUM = 1
MAX_NUM = 50
MIN_TREVOS = 2
MAX_TREVOS = 6
RANGE_TREVO = range(1, 7)
RANGEBET = range(MIN_NUM, MAX_NUM + 1)


class Milionaria:

    def __init__(self, *args, dezenas=MIN_BET, num_trevos=2, trevos=(0, 0)):
        """
        Cria um objeto do tipo +Milionaria.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=6)
        :param dezenas: Quantidade de dezenas da aposta (6-15)
        """
        assert len(args) <= MAX_BET, f'Esperado no máximo {MAX_BET} dezenas. (Passadas {len(args)})'
        assert MIN_BET <= dezenas <= MAX_BET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MIN_BET} e {MAX_BET}. (Foi informado {dezenas})'
        assert self.__checkargs(args), f'+Milionária usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        assert MIN_TREVOS <= num_trevos <= MAX_TREVOS, f'Devem ser escolhidos de 2 a 6 trevos.'
        assert set(trevos).issubset(RANGE_TREVO), f'Trevos devem ser números de 1 a 6'
        self.__dezenas = dezenas
        self.__num_trevos = num_trevos
        self.__trevos = set(trevos)
        self.__jogo = self.__surpresinha(set(trevos), set(args))

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.sort()
        return str(l_exib)

    def __iter__(self):
        yield set(self.__jogo)

    def __len__(self):
        return self.__dezenas + len(self.__trevos)

    @staticmethod
    def __checkargs(numeros):
        if len(numeros) == 0:
            return True
        else:
            for i in numeros:
                if i not in RANGEBET:
                    return False
            return True

    def __surpresinha(self, trevos=(), fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 50 mais dois trevos
        :return: set
        """
        # Sorteio dos 6 numeros principais
        retorno = set(fixos)
        numeros = [x for x in RANGEBET if x not in retorno]    # Generator desconsidera fixos
        while len(retorno) < self.__dezenas:
            retorno.add(numeros.pop(secrets.randbelow(len(numeros))))
            time.sleep(0.2)    # Aumenta a aleatoriedade
        # Sorteio dos trevos
        retorno_t = set(trevos)
        numeros_t = [t for t in RANGE_TREVO if t not in retorno_t]
        while len(retorno_t) < self.__num_trevos:
            retorno_t.add(numeros.pop(secrets.randbelow(len(numeros_t))))
        retorno.add(tuple(retorno_t))
        return set(retorno)

    def sorteio(self):
        return self.__surpresinha()

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
