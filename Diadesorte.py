"""
Classe do Dia de sorte - 7 numeros de 1 a 31 e um mes
Para fins de sorteio consideram-se apenas os números, conforme regras da Caixa
o mês é apenas para exibição e comparação pois é um prêmio pequeno independente dos números.
"""

import secrets
import time

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
        self.__jogo = self.__surpresinha(set(args))
        self.__gira_globo = secrets.SystemRandom()

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
        retorno = set(fixos)
        numeros = [x for x in RANGEBET if x not in retorno]    # Generator desconsidera os fixos
        while len(retorno) < self.__dezenas:
            self.__gira_globo.shuffle(numeros)
            retorno.add(numeros.pop(secrets.randbelow(len(numeros))))
            time.sleep(0.2)    # Aumenta a aleatoriedade
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
        return self.__mes


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
