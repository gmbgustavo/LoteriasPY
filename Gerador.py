"""
Gerador de apostas
"""

import inspect
import argparse
from Quina import *
from Megasena import *
from Lotofacil import *
from Lotomania import *
from Duplasena import *
from Diadesorte import *
from Timemania import *
from colorama import Fore

# Configurações regionais
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

MODALIDADES = ['Quina', 'Megasena', 'Lotofacil', 'Lotomania', 'Timemania',
               'Diadesorte', 'Duplasena']

MAX_JOGOS = 10    # Limite de sugestões devido ao custo da API


class Gerador:

    def __init__(self, modalidade: str, dezenas: int, fixados: list, quantidade=1):
        """
        :param modalidade: Nome do jogo em string. (Quina, Megasena, Lotofacil, Lotomania, Diadesorte, Duplasena)
        :param dezenas: quantidade de dezenas para apostar (observar minimos e maximos)
        :param fixados: dezenas que obrigatoriamente estarao no jogo
        :param quantidade: numero de apostas para gerar
        """
        assert modalidade in MODALIDADES, \
            f'Modalidade inválida: Válidas apenas {MODALIDADES}. Informado {modalidade}.'
        assert 1 <= quantidade <= MAX_JOGOS and isinstance(quantidade, int), \
            f'Quantidades de jogos deve ser um número inteiro entre 1 e {MAX_JOGOS}'
        self.__jogo = set()
        self.__modalidade = modalidade
        self.__fixados = set(fixados)
        self.__dezenas = dezenas
        self.__quantidade = quantidade
        self.__sugestoes = []

    def gerajogo(self):
        modalidades = {
            'Quina': Quina,
            'Duplasena': Duplasena,
            'Megasena': Megasena,
            'Diadesorte': Diadesorte,
            'Lotomania': Lotomania,
            'Lotofacil': Lotofacil,
            'Timemania': Timemania,
        }

        for i in range(1, self.__quantidade + 1):
            lf = modalidades[self.__modalidade](
                *self.__fixados,
                dezenas=self.__dezenas if 'dezenas' in inspect.signature(
                    modalidades[self.__modalidade]).parameters else None
            )
            self.__sugestoes.append(list(lf.jogo))
            del lf

        return self.__sugestoes

    def sugestoes(self):
        assert len(self.__sugestoes) >= 1, 'Você deve gerar o jogo primeiro. Use o método gerajogo()'
        print(f'\nSugestões para {self.__modalidade}:')
        print(f'-----------------------------------------------')
        self.__sugestoes.sort(key=lambda item: str(item))
        for aposta in self.__sugestoes:
            aposta.sort(key=lambda item: (0, int(item)) if isinstance(item, int) else (1, item))
            for dezena in aposta:
                print(f'{str(dezena).zfill(2)} ', end='')
            print('\n')

    def __repr__(self):
        l_exib = list(self.__sugestoes)
        l_exib.sort(key=lambda item: str(item))
        return str(l_exib)

    def __len__(self):
        return self.__dezenas

    def get_name(self):
        return self.__modalidade

# TODO: Add argparse


if __name__ == '__main__':
    jogo = Gerador(modalidade='Megasena',
                   dezenas=9,
                   fixados=[],
                   quantidade=3)
    print(f'Jogo a gerar: {jogo.get_name()} com {len(jogo)} dezenas.')
    print(f'Gerando, isso pode levar até 15 segundos dependendo da quantidade...\n' + Fore.LIGHTYELLOW_EX)
    jogo.gerajogo()
    jogo.sugestoes()
