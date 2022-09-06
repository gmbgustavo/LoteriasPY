"""
Classe da Lotofacil
"""

import secrets


class Lotofacil:

    def __init__(self, *args, dezenas=15):
        """
        Cria um objeto do tipo Lotofacil.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas padrao (15)
        """
        self.__dezenas = dezenas
        if len(args) == 0:
            self.__jogo = self.__surpresinha()
        elif len(args) < 15:
            self.__jogo = self.__surpresinha(set(args))
        elif len(args) > 20:
            raise AttributeError('Máximo 20 parametros.')

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
        retorno = set(fixos)
        while len(retorno) < self.__dezenas:
            retorno.add(secrets.choice(range(1, 26, 1)))
        return set(retorno)

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')


