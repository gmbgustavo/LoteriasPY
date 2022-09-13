"""
Classe do Dia de sorte - 7 numeros de 1 a 31 e um mes
"""

import secrets

MAXBET = 15
MINBET = 7
MINNUM = 1
MAXNUM = 31
RANGEBET = range(MINNUM, MAXNUM + 1)
MESES = ('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez')


class Diadesorte:

    def __init__(self, *args, mes=0, dezenas=7):
        """
        Cria um objeto do tipo Dia de sorte.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=8)
        :param dezenas: Quantidade de dezenas da aposta (7-15)
        :param mes: Um inteiro de 1 a 12 representando o mes do ano
        """
        assert len(args) <= MAXBET, f'Esperado no máximo {MAXBET} dezenas. (Passadas {len(args)})'
        assert MINBET <= dezenas <= MAXBET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MINBET} e {MAXBET}. (Passadas {dezenas})'
        assert self.__checkargs(args), f'Dia de Sorte usa números inteiros entre 0{MINNUM} e {MAXNUM}'
        assert isinstance(mes, int) and 0 <= mes <= 12, \
            f'O mes deve ser escolhido explicitamente usando mes= e um numero de 1 a 12. (0 ou vazio para surpresinha)'
        self.__dezenas = dezenas
        self.__mes = mes
        self.__jogo = self.__surpresinha(set(args))

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.sort(key=lambda item: str(item))
        return str(l_exib)

    def __iter__(self):
        yield set(self.__jogo)

    def __len__(self):
        return self.__dezenas

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 31
        :return: set
        """
        count = len(RANGEBET)
        retorno = set(fixos)
        numeros = [x for x in range(1, count + 1)]
        while len(retorno) < self.__dezenas:
            retorno.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
        if self.__mes == 0:
            self.__mes = secrets.choice(range(0, len(MESES)))
            retorno.add(MESES[self.__mes])
        else:
            retorno.add(MESES[self.__mes - 1])
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

    @property
    def meses(self):
        return MESES


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
