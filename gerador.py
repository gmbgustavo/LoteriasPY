"""
Gerador de apostas
"""

import secrets
from Quina import Quina
from Megasena import Megasena
from Lotofacil import Lotofacil
from Lotomania import Lotomania
from Duplasena import Duplasena
from Diadesorte import Diadesorte

SENA = 6
QUINA = 5
LOTOFACIL = 15
LOTOMANIA = 20
DUPLASENA = 6
DIADESORTE = 8
MESES = ('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez')


class Gerador:

    def __init__(self, modalidade: str, dezenas: int, fixados: list):
        self.__jogo = set()
        self.__jogo.clear()
        self.__modalidade = modalidade
        self.__fixados = set(fixados)
        self.__dezenas = dezenas

    def gerajogo(self):
        if self.__modalidade == 'Quina':
            pass
        elif self.__modalidade == 'Megasena':
            pass
        elif self.__modalidade == 'Diadesorte':
            pass
        elif self.__modalidade == 'Lotomania':
            pass
        elif self.__modalidade == 'Lotofacil':
            print('Modalidade = Lotofacil')
            self.__jogo = set(self.__fixados)
            while len(self.__jogo) < LOTOFACIL:
                self.__jogo.add(secrets.choice(range(1, 26, 1)))
            return self.__jogo
        elif self.__modalidade == 'Duplasena':
            pass

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.sort()
        return str(l_exib)

    def __len__(self):
        return self.__dezenas


if __name__ == '__main__':
    jogo = Gerador(modalidade='Lotofacil', dezenas=15, fixados=[])
    jogo.gerajogo()
    print(jogo)
    print(f'Tamanho do jogo {len(jogo)}')
