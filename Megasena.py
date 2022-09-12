"""
Classe da Mega-Sena
"""

import secrets

MAXBET = 15
MINBET = 6
MINNUM = 1
MAXNUM = 60
RANGEBET = range(MINNUM, MAXNUM + 1)


class Megasena:

    def __init__(self, *args, dezenas=MINBET):
        """
        Cria um objeto do tipo Megasena.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=6)
        :param dezenas: Quantidade de dezenas da aposta (6-15)
        """
        assert len(args) <= MAXBET, f'Esperado no máximo {MAXBET} dezenas. (Passadas {len(args)})'
        assert MINBET <= dezenas <= MAXBET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MINBET} e {MAXBET}. (Passadas {dezenas})'
        assert self.__checkargs(args), f'Lotofácil usa números inteiros entre 0{MINNUM} e {MAXNUM}'
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
        count = len(RANGEBET)
        retorno = set(fixos)
        numeros = [x for x in range(1, count + 1)]
        while len(retorno) < self.__dezenas:
            retorno.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
        return set(retorno)

    def sorteio(self):
        return self.__surpresinha()

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
