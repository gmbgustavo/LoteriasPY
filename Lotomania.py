"""
Classe da Lotomania
"""

from random import randrange


class Lotomania:

    def __init__(self, *args):
        """
        Cria um objeto do tipo Lotofacil.
        :param args: Se vazio, cria um jogo surpresinha com a 50 dezenas
        """
        self.__dezenas = 50
        if len(args) == 0:
            self.__jogo = self.__surpresinha()
        elif len(args) != 50:
            raise AttributeError('Os parametros de jogo devem ser 50 inteiros')
        else:
            self.__jogo = set(args)

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.sort()
        return str(l_exib)

    def __iter__(self):
        yield set(self.__jogo)

    def __len__(self):
        return self.__dezenas

    def __surpresinha(self):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 100
        :return: set
        """
        retorno = set()
        while len(retorno) < self.__dezenas:
            retorno.add(randrange(1, 101, 1))
        return set(retorno)

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
