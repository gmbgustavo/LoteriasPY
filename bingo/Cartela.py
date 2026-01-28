# CARTELA DE BINGO PADRÃO

from API.random_api import *
from .Geracartela import Geracartela

class Cartela:
    def __init__(self, tam_cartela=25, quantidade=1, num_max=75):
        self.tam_cartela = tam_cartela
        self.min = 1
        self.max = num_max
        self.quantidade = quantidade
        self.cartela = self.gerar_cartela()

    def __cartela_random(self):
        cartela = get_numbers(n=self.tam_cartela, min_val=self.min, max_val=self.max, repeat=False)
        return list(cartela)

    def gerar_cartela(self):
        cartela=[]
        for x in range(0, self.quantidade):
            cartela.append(self.__cartela_random())
        return cartela

    def print_cartela(self):
        # Itera sobre todas as cartelas geradas (self.quantidade)
        for i in range(self.quantidade):
            # Ordena a cartela atual
            self.cartela[i].sort()

            # Se não for a primeira cartela, adiciona uma linha em branco para separar
            if i > 0:
                print("\n")  # Espaço extra entre cartelas

            # Imprime o título opcional da cartela (ex: Cartela 1, Cartela 2...)
            print(f"         CARTELA {i + 1}".center(30))

            # Cabeçalho da caixa
            print("   ╔═══╦═══╦═══╦═══╦═══╗")
            print("   ║ B ║ I ║ N ║ G ║ O ║")
            print("   ╠═══╬═══╬═══╬═══╬═══╣")

            # Corpo da cartela: 5 linhas, preenchendo por colunas
            for linha in range(5):
                print("   ║", end=' ')
                for coluna in range(5):
                    indice = coluna * 5 + linha
                    numero = self.cartela[i][indice]
                    print(f"{numero:2d}║", end=' ')
                print()  # Quebra de linha após os 5 números

                # Linha separadora intermediária (exceto após a última linha)
                if linha < 4:
                    print("   ╠═══╬═══╬═══╬═══╬═══╣")

            # Rodapé da caixa
            print("   ╚═══╩═══╩═══╩═══╩═══╝")

    def salvar_pdf(self, nome_arquivo="cartelas_bingo.pdf"):
        """
        Salva todas as cartelas em um PDF usando a classe Geracartela.
        """
        Geracartela.salva_pdf(self.cartela, nome_arquivo)
