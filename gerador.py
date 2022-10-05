"""
Gerador de apostas
"""

from Quina import Quina
from Megasena import Megasena
from Lotofacil import Lotofacil
from Lotomania import Lotomania
from Duplasena import Duplasena
from Diadesorte import Diadesorte
from Supersete import Supersete

MODALIDADES = ['Quina', 'Megasena', 'Lotofacil', 'Lotomania',
               'Diadesorte', 'Duplasena', 'Supersete', 'Milionaria']

MAXJOGOS = 10    # Maximo 10 jogos para não extrapolar um tempo razoável na geração


class Gerador:

    def __init__(self, modalidade: str, dezenas: int, fixados: list, quantidade=1, mes=0):
        """
        :param modalidade: Nome do jogo em string. (Quina, Megasena, Lotofacil, Lotomania, Diadesorte, Duplasena)
        :param dezenas: quantidade de dezenas para apostar (observar minimos e maximos)
        :param fixados: dezenas que obrigatoriamente estarao no jogo
        :param quantidade: numero de apostas para gerar
        :param mes: mes fixo a ser apostado (apenas diadesorte)
        """
        assert modalidade in MODALIDADES, \
            f'Modalidade inválida: Válidas apenas {MODALIDADES}. Informado {modalidade}.'
        assert 1 <= quantidade <= MAXJOGOS and isinstance(quantidade, int), \
            f'Quantidades de jogos deve ser um número inteiro entre 1 e {MAXJOGOS}'
        self.__jogo = set()
        self.__modalidade = modalidade
        self.__fixados = set(fixados)
        self.__dezenas = dezenas
        self.__quantidade = quantidade
        self.__sugestoes = []
        self.__mes = mes    # Usado apenas no Diadesorte

    def gerajogo(self):
        if self.__modalidade == 'Quina':
            for i in range(1, self.__quantidade + 1):
                lf = Quina(*self.__fixados, dezenas=self.__dezenas)
                self.__sugestoes.append(list(lf.jogo))
                del lf
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
                lf = Diadesorte(*self.__fixados, dezenas=self.__dezenas, mes=self.__mes)
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
        elif self.__modalidade == 'Supersete':
            for i in range(1, self.__quantidade + 1):
                lf = Supersete(*self.__fixados, dezenas=self.__dezenas)
                self.__sugestoes.append(list(lf.jogo))
        return self.__sugestoes

    def sugestoes(self):
        assert len(self.__sugestoes) >= 1, 'Você deve gerar o jogo primeiro. Use o método gerajogo()'
        self.__sugestoes.sort(key=lambda item: str(item))
        for aposta in self.__sugestoes:
            aposta.sort(key=lambda item: (0, int(item)) if isinstance(item, int) else (1, item))
            for dezena in aposta:
                print(f'{str(dezena).zfill(2)} ', end='')
            print('\n')
        return None

    def __repr__(self):
        l_exib = list(self.__sugestoes)
        l_exib.sort(key=lambda item: str(item))
        return str(l_exib)

    def __len__(self):
        return self.__dezenas


if __name__ == '__main__':
    jogo = Gerador(modalidade='Diadesorte',
                   dezenas=7,
                   fixados=[],
                   quantidade=3)
    print(f'Tamanho do jogo {len(jogo)}')
    print(f'Gerando em aproximadamente 6 segundos...')
    jogo.gerajogo()
    jogo.sugestoes()
