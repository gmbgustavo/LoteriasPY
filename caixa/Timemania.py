"""
Classe da Timemania
"""

import secrets
import time
import csv
import locale
from pathlib import Path
from API.random_api import get_numbers

# Configuração regional
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

BET = 10
MIN_NUM = 1
MAX_NUM = 80
RANGEBET = range(MIN_NUM, MAX_NUM + 1)
LISTA_TIMES = Path(__file__).resolve().parent / './dados/times.csv'


class Timemania:

    def __init__(self, *args, timedocoracao=-1, dezenas=BET):
        """
        Cria um objeto do tipo Lotofacil.
        :param args: Se vazio, cria um jogo surpresinha com a 50 dezenas
        """
        assert self.__checkargs(args), f'Timemania usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        assert dezenas == BET, f'Aposta única de {BET}'
        self.__dezenas = dezenas
        self.__listadetimes = self.__carregatimes()
        if timedocoracao == -1:
            self.__timedocoracao = self.__listadetimes[secrets.randbelow(len(self.__listadetimes))]
        else:
            self.__timedocoracao = timedocoracao
        self.__jogo = self.__surpresinha(set(args))

    @staticmethod
    def __carregatimes():
        with open(LISTA_TIMES, "r", encoding="utf8") as times:
            reader = csv.reader(times)
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

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 100
        :param fixos: Numeros pre estabelecidos
        :return: set
        """
        qtde = self.__dezenas - len(fixos)
        if qtde <= 0:
            return set(fixos)
        buffer_size = qtde + 5
        apicall = get_numbers(n=buffer_size, min_val=MIN_NUM, max_val=MAX_NUM, repeat=False)
        disponiveis = [num for num in apicall if num not in fixos]
        for num in disponiveis:
            if len(fixos) < self.__dezenas:
                fixos.add(num)
            else:
                break
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
        return set(self.__jogo)


if __name__ == '__main__':
    quit(3)
