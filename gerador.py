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


class Gerador:

    def __init__(self, modalidade: str, dezenas: int, fixados: list, quantidade=1):
        """
        :param modalidade: Nome do jogo em string. (Quina, Megansena, Lotofacil, Lotomania, Diadesorte, Duplasena)
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
            for i in range(1, self.__quantidade + 1):
                lf = Quina(*self.__fixados, dezenas=self.__dezenas)
                self.__sugestoes.append(list(lf.jogo))
        elif self.__modalidade == 'Duplasena':
            for i in range(1, self.__quantidade + 1):
                lf = Duplasena(*self.__fixados, dezenas=self.__dezenas)
                self.__sugestoes.append(list(lf.jogo))
        elif self.__modalidade == 'Megasena':
            for i in range(1, self.__quantidade + 1):
                lf = Megasena(*self.__fixados, dezenas=self.__dezenas)
                self.__sugestoes.append(list(lf.jogo))
        elif self.__modalidade == 'Diadesorte':
            for i in range(1, self.__quantidade + 1):
                lf = Diadesorte(*self.__fixados, dezenas=self.__dezenas)
                self.__sugestoes.append(list(lf.jogo))
        elif self.__modalidade == 'Lotomania':
            for i in range(1, self.__quantidade + 1):
                lf = Lotomania(*self.__fixados)
                self.__sugestoes.append(list(lf.jogo))
        elif self.__modalidade == 'Lotofacil':
            for i in range(1, self.__quantidade + 1):
                lf = Lotofacil(*self.__fixados, dezenas=self.__dezenas)
                self.__sugestoes.append(list(lf.jogo))
        elif self.__modalidade == 'Duplasena':
            for i in range(1, self.__quantidade + 1):
                lf = Duplasena(*self.__fixados, dezenas=self.__dezenas)
                self.__sugestoes.append(list(lf.jogo))
        return self.__sugestoes

    def sugestoes(self):
        assert len(self.__sugestoes) >= 1, 'Você deve gerar o jogo primeiro. Use o método gerajogo()'
        for aposta in self.__sugestoes:
            aposta.sort()
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
                   fixados=[],
                   quantidade=5)
    print(f'Tamanho do jogo {len(jogo)}')
    jogo.gerajogo()
    jogo.sugestoes()

