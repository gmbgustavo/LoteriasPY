"""
Classe da Lotofacil
"""

import secrets

MAXBET = 18
RANGEBET = range(1, 26)


class Lotofacil:

    def __init__(self, *args, dezenas=15):
        """
        Cria um objeto do tipo Lotofacil.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas padrao (15)
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

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 25
        :return: set
        """
        count = 25
        retorno = set(fixos)    # Apenas no caso de gerador
        numeros = [x for x in range(1, count + 1)]
        while len(retorno) < self.__dezenas:
            retorno.add(numeros.pop(secrets.choice(range(0, count, 1))))
            count -= 1
        return set(retorno)

    @property
    def jogo(self):
        return set(self.__jogo)

    @staticmethod
    def __checkargs(numeros):
        for i in numeros:
            if i > 25 or i <= 0:
                return False
        return True


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')


