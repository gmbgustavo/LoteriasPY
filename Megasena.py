"""
Classe da Mega-Sena
"""

import secrets

MAXBET = 15
RANGEBET = range(1, 61)


class Megasena:

    def __init__(self, *args, dezenas=6):
        """
        Cria um objeto do tipo Megasena.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=6)
        :param dezenas: Quantidade de dezenas da aposta (6-15)
        """
        assert len(args) <= MAXBET
        self.__dezenas = dezenas
        if len(args) > 0 and self.__checkargs(args):
            self.__jogo = self.__surpresinha(set(args))
        if len(args) == 0:
            self.__jogo = self.__surpresinha()
        else:
            raise AttributeError('Megasena aceita numeros entre 01 e 60 somente.')

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
            retorno.add(numeros.pop(secrets.choice(range(0, count, 1))))
            count -= 1
        return set(retorno)

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
