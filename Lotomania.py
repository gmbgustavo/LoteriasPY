"""
Classe da Lotomania
"""

import secrets

BET = 50
MIN_NUM = 1
MAX_NUM = 100
RANGEBET = range(MIN_NUM, MAX_NUM + 1)


class Lotomania:

    def __init__(self, *args):
        """
        Cria um objeto do tipo Lotofacil.
        :param args: Se vazio, cria um jogo surpresinha com a 50 dezenas
        """
        assert self.__checkargs(args), f'Lotofácil usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        self.__jogo = self.__surpresinha(args)

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.sort()
        return str(l_exib)

    def __iter__(self):
        yield set(self.__jogo)

    def __len__(self):
        return BET

    @staticmethod
    def __surpresinha(fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 100
        :param fixos: Numeros pre estabelecidos
        :return: set
        """
        retorno = set(fixos)
        numeros = [x for x in range(1, len(RANGEBET) + 1) if x not in retorno]    # Generator desconsidera os fixos
        count = len(numeros)
        while len(retorno) < BET:
            retorno.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
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
