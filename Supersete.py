"""
Classe da Super Sete
Para apostar deve ser passado um dicionario com a chave sendo o numero da coluna (int)
e os valores uma tupla, de tamanho 1 a 3, com cada uma contendo numeros de 0 a 9
"""

import secrets
import random
import time

MIN_NUM = 0
MAX_NUM = 9
MIN_BET = 7
MAX_BET = 21
RANGEBET = range(MIN_NUM, MAX_NUM + 1)


class Supersete:

    def __init__(self, dezenas=7):
        """
        Cria um objeto do tipo Megasena.
        :param dezenas: Quantidade de dezenas da aposta (7-15)
        """
        assert MIN_BET <= dezenas <= MAX_BET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MIN_BET} e {MAX_BET}. (Foi informado {dezenas})'
        self.__dezenas = dezenas
        self.__jogo = self.__surpresinha(dezenas=dezenas)

    @staticmethod
    def __surpresinha(dezenas):
        """
        Retorna uma matriz
        :return: set
        """
        matriz = [[] for _ in range(MIN_BET)]
        time.sleep(0.1)
        for i in range(dezenas):
            time.sleep(0.1)
            coluna = i % 7
            if i < 7:
                matriz[coluna].append(secrets.randbelow(MAX_NUM + 1))
            else:
                coluna_count = [len(col) for col in matriz]
                coluna_aleatoria = random.choice([col for col in range(MIN_BET) if coluna_count[col] < 3])
                # noinspection PyTypeChecker
                matriz[coluna_aleatoria].append(secrets.randbelow(MAX_NUM + 1))
        return matriz

    @property
    def jogo(self):
        return self.__jogo

    def __len__(self):
        return self.__dezenas


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
