"""
Classe do Dia de sorte - 7 numeros de 1 a 31 e um mes
Para fins de sorteio consideram-se apenas os números, conforme regras da Caixa
o mês é apenas para exibição e comparação pois é um prêmio pequeno independente dos números.
"""

import secrets
import time
from API.random_api import get_numbers

MAX_BET = 15
MIN_BET = 7
MIN_NUM = 1
MAX_NUM = 31
RANGEBET = range(MIN_NUM, MAX_NUM + 1)
MESES = ('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez')


class Diadesorte:

    def __init__(self, *args, dezenas, mes=0):
        """
        Cria um objeto do tipo Dia de sorte.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=8)
        :param dezenas: Quantidade de dezenas da aposta (7-15)
        :param mes: Um inteiro de 1 a 12 representando o mes do ano. 0 para surpresinha.
        """
        assert len(args) <= MAX_BET, f'Esperado no máximo {MAX_BET} dezenas. (Passadas {len(args)})'
        assert MIN_BET <= dezenas <= MAX_BET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MIN_BET} e {MAX_BET}. (Passadas {dezenas})'
        assert self.__checkargs(args), f'Dia de Sorte usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        assert isinstance(mes, int) and 0 <= mes <= 12, \
            f'O mes deve ser escolhido explicitamente usando mes= e um numero de 1 a 12. (0 para surpresinha)'
        assert len(args) <= dezenas, f'Quantidade de números informados incompativel com o argumento "dezenas"'
        self.__dezenas = dezenas
        self.__mes = mes
        self.__gira_globo = secrets.SystemRandom()
        self.__jogo = self.__surpresinha(set(args))

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.sort(key=lambda ele: (0, int(ele)) if isinstance(ele, int) else (1, ele))
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
        gerados = len(fixos)
        qtde = self.__dezenas - len(fixos)
        if qtde <= 0:
            return set(fixos)
        time.sleep(0.2)
        while len(fixos) < self.__dezenas:
            if qtde >= 1:
                apicall = get_numbers(n=qtde, min_val=MIN_NUM, max_val=MAX_NUM, repeat=False)
                numeros = [x for x in apicall if x not in fixos]    # Generator desconsidera fixos
                for dez in numeros:
                    fixos.add(dez)
                gerados = len(fixos)
            qtde = self.__dezenas - gerados
        if self.__mes == 0:
            self.__mes = secrets.choice(range(0, len(MESES)))
            fixos.add(MESES[self.__mes])
        else:
            fixos.add(MESES[self.__mes - 1])
        return set(fixos)

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
        l_exib = list(self.__jogo)
        l_exib.sort(key=lambda ele: (0, int(ele)) if isinstance(ele, int) else (1, ele))
        return l_exib

    @property
    def meses(self):
        return self.__mes


if __name__ == '__main__':
    print('Essa classe não deve ser executada diretamente.')
