"""
Classe da Timemania
"""

import secrets
import time
import csv
import locale

# Configuração regional
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

BET = 10
MIN_NUM = 1
MAX_NUM = 80
RANGEBET = range(MIN_NUM, MAX_NUM + 1)
LISTA_TIMES = './dados/times.csv'


class Timemania:

    def __init__(self, *args, timedocoracao=-1):
        """
        Cria um objeto do tipo Lotofacil.
        :param args: Se vazio, cria um jogo surpresinha com a 50 dezenas
        """
        assert self.__checkargs(args), f'Timemania usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        self.__listadetimes = self.__carregatimes()
        if timedocoracao == -1:
            self.__timedocoracao = self.__listadetimes[secrets.randbelow(len(self.__listadetimes))]
        else:
            self.__timedocoracao = timedocoracao
        assert self.__timedocoracao in self.__listadetimes, f'Time inválido - {timedocoracao}'
        self.__jogo = self.__surpresinha(args)

    @staticmethod
    def __carregatimes():
        with open(LISTA_TIMES, "r", encoding="utf8") as times:
            reader = csv.reader(times, delimiter=',')
            retorno = list(reader)
            return retorno

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.append(self.__timedocoracao)
        l_exib.sort(key=lambda ele: (0, int(ele)) if isinstance(ele, int) else (1, ele))
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
        numeros = [x for x in RANGEBET if x not in retorno]    # Generator desconsidera os fixos
        while len(retorno) < BET:
            retorno.add(numeros.pop(secrets.randbelow(len(numeros))))
            time.sleep(0.1)    # Aumenta a aleatoriedade
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
    jogo = Timemania()
    print(jogo)
