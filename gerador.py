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

    def __init__(self, modalidade: str, dezenas: int, fixados: list, quantidade=1):
        """
        :param modalidade: Nome do jogo em string
        :param dezenas: quantidade de dezenas para apostar (observar minimos e maximos)
        :param fixados: dezenas que obrigatoriamente estarao no jogo
        :param quantidade: numero de apostas para gerar
        """
        self.__jogo = set()
        self.__modalidade = modalidade
        self.__fixados = set(fixados)
        self.__dezenas = dezenas
        self.__quantidade = quantidade
        self.__sugestoes = []

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
            for i in range(1, self.__quantidade + 1):
                lf = Lotofacil(*self.__fixados, dezenas=self.__dezenas)
                self.__sugestoes.append(list(lf.jogo))
                del lf
        elif self.__modalidade == 'Duplasena':
            pass

    def sugestoes(self):
        for aposta in self.__sugestoes:
            for dezena in aposta:
                print(f'{str(dezena).zfill(2)} ', end='')
            print('\n')
        return None

    def __repr__(self):
        l_exib = self.__sugestoes
        l_exib.sort()
        return str(l_exib)

    def __len__(self):
        return self.__dezenas


if __name__ == '__main__':
    jogo = Gerador(modalidade='Lotofacil',
                   dezenas=15,
                   fixados=[2, 5, 9, 12, 14, 18, 21],
                   quantidade=5)
    print(f'Tamanho do jogo {len(jogo)}')
    jogo.gerajogo()
    jogo.sugestoes()

