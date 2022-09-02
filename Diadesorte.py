"""
Classe do Dia de sorte - 7 numeros de 1 a 31 e um mes
"""


import secrets


class Diadesorte:

    __MESES = ('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez')

    def __init__(self, *args, mes='', dezenas=7):
        """
        Cria um objeto do tipo Dia de sorte.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=8)
        :param dezenas: Quantidade de dezenas da aposta (7-15)
        """
        self.__dezenas = dezenas
        self.__mes = mes
        if len(args) == 0:
            self.__jogo = self.__surpresinha()
        elif len(args) < 7 or len(args) > 15:
            raise AttributeError('Os parametros de jogo devem ser inteiros entre 7 e 15 finalizando com um mes')
        else:
            self.__dezenas = len(args)
            self.__jogo = set(args)
            self.__jogo.add(mes)

    def __repr__(self):
        l_exib = list(self.__jogo)
        return str(l_exib)

    def __iter__(self):
        yield set(self.__jogo)

    def __len__(self):
        return self.__dezenas

    def __surpresinha(self):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 31
        :return: set
        """
        retorno = set()
        while len(retorno) < self.__dezenas:
            retorno.add(secrets.choice(range(1, 32, 1)))
        retorno.add(self.__MESES[secrets.choice(range(0, 12, 1))])
        return set(retorno)

    @property
    def jogo(self):
        return set(self.__jogo)

    @property
    def meses(self):
        return self.__MESES


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
