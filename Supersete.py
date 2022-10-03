"""
Classe da Super Sete
Para apostar deve ser passado um dicionario com a chave sendo o numero da coluna (int)
e os valores uma tupla, de tamanho 1 a 3, com cada uma contendo numeros de 0 a 9
"""

import secrets
import time

MAX_NUM_COL = 3
MIN_NUM_COL = 1
MIN_NUM = 0
MAX_NUM = 9
MIN_BET = 7
MAX_BET = 7
RANGEBET = range(MIN_NUM, MAX_NUM + 1)

JOGO = {'C1': (),
        'C2': (),
        'C3': (),
        'C4': (),
        'C5': (),
        'C6': (),
        'C7': (),
        }


class Supersete:

    def __init__(self, *args, dezenas):
        """
        Cria um objeto do tipo Megasena.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=6)
        :param dezenas: Quantidade de dezenas da aposta (6-15)
        """
        assert len(args) <= MAX_BET, f'Esperado no máximo {MAX_BET} dezenas. (Passadas {len(args)})'
        assert MIN_BET <= dezenas <= MAX_BET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MIN_BET} e {MAX_BET}. (Foi informado {dezenas})'
        assert len(args) <= dezenas, f'Quantidade de números informados incompativel com o argumento "dezenas"'
        assert self.__checkargs(args), f'Megasena usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        self.__dezenas = dezenas
        self.__jogo = self.__surpresinha(set(args))

    def __distribuir(self, fixos):
        pass

    @staticmethod
    def __checkargs(numeros):
        if len(numeros) == 0:
            return True
        else:
            for i in numeros:
                if i not in RANGEBET:
                    return False
            return True

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 60
        :return: set
        """
        retorno = set(fixos)
        numeros = [x for x in RANGEBET if x not in retorno]    # Generator desconsidera fixos
        while len(retorno) < self.__dezenas:
            retorno.add(numeros.pop(secrets.randbelow(len(numeros))))
            time.sleep(0.1)    # Aumenta a entropia
        return set(retorno)

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
