# CARTELA DE BINGO PADRÃO
#
# Uma cartela válida tem 25 dezenas distribuídas em 5 colunas, cada uma com a
# sua faixa: B (1-15), I (16-30), N (31-45), G (46-60) e O (61-75).
# A lista interna é guardada na ordem coluna a coluna, ou seja,
# indice = coluna * 5 + linha, que é a ordem usada para desenhar a grade.

import random

try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from API.random_api import *
except Exception:
    # Fallback para geração local de números aleatórios (a API é opcional)
    def get_numbers(n, min_val, max_val, repeat=False):
        if repeat:
            return [random.randint(min_val, max_val) for _ in range(n)]
        return random.sample(range(min_val, max_val + 1), n)

try:
    from .Geracartela import Geracartela
except ImportError:
    # Fallback caso matplotlib não esteja disponível
    class Geracartela:
        @staticmethod
        def salva_pdf(cartelas, nome_arquivo="cartelas_bingo.pdf", titulo="BINGO DA AMIZADE"):
            print("⚠️ Não é possível gerar PDF. matplotlib não está disponível.")
            print(f"Seriam geradas {len(cartelas)} cartelas no arquivo {nome_arquivo}")


LETRAS = ('B', 'I', 'N', 'G', 'O')
DEZENAS_POR_COLUNA = 5


class Cartela:
    def __init__(self, tam_cartela=25, quantidade=1, num_max=75, gerar=True):
        """
        :param tam_cartela: total de dezenas da cartela (25 no bingo tradicional)
        :param quantidade: quantas cartelas gerar
        :param num_max: maior dezena possível (75 no bingo tradicional)
        :param gerar: se False, não gera nada no construtor (útil para a cartela manual)
        """
        if tam_cartela != DEZENAS_POR_COLUNA * len(LETRAS):
            raise ValueError(f'A cartela deve ter {DEZENAS_POR_COLUNA * len(LETRAS)} dezenas '
                             f'({DEZENAS_POR_COLUNA} por coluna); recebido {tam_cartela}.')
        self.tam_cartela = tam_cartela
        self.min = 1
        self.max = num_max
        self.quantidade = quantidade
        self.cartela = self.gerar_cartela() if gerar else []

    # ------------------------------------------------------------------
    # Faixas de cada coluna
    # ------------------------------------------------------------------
    def faixas_colunas(self) -> list:
        """Faixas (início, fim) de cada uma das 5 colunas.

        Para o bingo tradicional (1 a 75) resulta em
        B 1-15, I 16-30, N 31-45, G 46-60 e O 61-75.
        """
        total = self.max - self.min + 1
        largura = total / len(LETRAS)
        faixas = []
        for indice in range(len(LETRAS)):
            inicio = int(round(self.min + indice * largura))
            fim = int(round(self.min + (indice + 1) * largura)) - 1
            faixas.append((inicio, fim))
        return faixas

    def __embaralha_faixa(self) -> list:
        """Permutação completa das dezenas da faixa (uma consulta ao RANDOM.ORG).

        Se o serviço estiver indisponível, usa o gerador local — o bingo é um
        passatempo local e não deve parar por causa de rede.
        """
        total = self.max - self.min + 1
        try:
            numeros = list(get_numbers(n=total, min_val=self.min, max_val=self.max, repeat=False))
        except Exception as erro:
            print(f"⚠️ RANDOM.ORG indisponível ({erro}); usando o gerador local.")
            numeros = random.sample(range(self.min, self.max + 1), total)

        if len(set(numeros)) != total:
            numeros = random.sample(range(self.min, self.max + 1), total)
        return numeros

    def __cartela_random(self) -> list:
        """Uma cartela válida: 5 dezenas de cada coluna, dentro da faixa da coluna."""
        embaralhado = self.__embaralha_faixa()
        colunas = []
        for inicio, fim in self.faixas_colunas():
            da_faixa = [numero for numero in embaralhado if inicio <= numero <= fim]
            colunas.append(sorted(da_faixa[:DEZENAS_POR_COLUNA]))

        if any(len(coluna) < DEZENAS_POR_COLUNA for coluna in colunas):
            # não deveria acontecer com a faixa completa; refaz com o gerador local
            embaralhado = random.sample(range(self.min, self.max + 1),
                                        self.max - self.min + 1)
            colunas = []
            for inicio, fim in self.faixas_colunas():
                da_faixa = [numero for numero in embaralhado if inicio <= numero <= fim]
                colunas.append(sorted(da_faixa[:DEZENAS_POR_COLUNA]))

        return [numero for coluna in colunas for numero in coluna]

    def gerar_cartela(self, quantidade=None) -> list:
        """Gera `quantidade` cartelas (lista de listas, na ordem coluna a coluna)."""
        total = self.quantidade if quantidade is None else quantidade
        return [self.__cartela_random() for _ in range(total)]

    # ------------------------------------------------------------------
    # Cartela manual
    # ------------------------------------------------------------------
    def criar_cartela_manual(self) -> list:
        """Monta uma cartela válida com as dezenas digitadas, uma coluna por vez.

        Retorna a lista de 25 dezenas na ordem coluna a coluna.
        """
        print("\n📝 CRIAÇÃO DE CARTELA MANUAL")
        print("Digite as 5 dezenas de cada coluna, separadas por vírgula.")
        print("=" * 50)

        colunas = []
        for indice, (inicio, fim) in enumerate(self.faixas_colunas()):
            letra = LETRAS[indice]
            while True:
                entrada = input(f"Coluna {letra} (5 dezenas de {inicio} a {fim}): ").strip()
                try:
                    numeros = [int(parte) for parte in
                               entrada.replace(';', ' ').replace(',', ' ').split()]
                except ValueError:
                    print("❌ Digite apenas números separados por vírgula.")
                    continue
                if len(numeros) != DEZENAS_POR_COLUNA:
                    print(f"❌ Informe exatamente {DEZENAS_POR_COLUNA} dezenas "
                          f"(você informou {len(numeros)}).")
                    continue
                fora_da_faixa = [n for n in numeros if n < inicio or n > fim]
                if fora_da_faixa:
                    print(f"❌ {fora_da_faixa} fora da faixa da coluna {letra} "
                          f"({inicio} a {fim}).")
                    continue
                if len(set(numeros)) != DEZENAS_POR_COLUNA:
                    print("❌ Não pode repetir dezenas na mesma coluna.")
                    continue
                colunas.append(sorted(numeros))
                break

        return [numero for coluna in colunas for numero in coluna]

    # ------------------------------------------------------------------
    # Impressão no terminal
    # ------------------------------------------------------------------
    def print_cartela(self, indice=None):
        """Imprime as cartelas no terminal (ou só uma, quando `indice` é informado)."""
        indices = range(len(self.cartela)) if indice is None else [indice]

        for i in indices:
            if i > 0 and indice is None:
                print("\n")

            print(f"         CARTELA {i + 1}".center(30))
            print("   ╔═══╦═══╦═══╦═══╦═══╗")
            print(f"   ║ {LETRAS[0]} ║ {LETRAS[1]} ║ {LETRAS[2]} ║ {LETRAS[3]} ║ {LETRAS[4]} ║")
            print("   ╠═══╬═══╬═══╬═══╬═══╣")

            for linha in range(5):
                print("   ║", end='')
                for coluna in range(5):
                    numero = self.cartela[i][coluna * 5 + linha]
                    print(f"{numero:3d}║", end='')
                print()

                if linha < 4:
                    print("   ╠═══╬═══╬═══╬═══╬═══╣")

            print("   ╚═══╩═══╩═══╩═══╩═══╝")

    def salvar_pdf(self, nome_arquivo="cartelas_bingo.pdf"):
        """Salva todas as cartelas em um PDF usando a classe Geracartela."""
        Geracartela.salva_pdf(self.cartela, nome_arquivo)
