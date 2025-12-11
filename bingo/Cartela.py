# CARTELA DE BINGO PADRÃO

from API.random_api import *


class Cartela:
    def __init__(self, tam_cartela: int, quantidade=1, num_max=75):
        self.tam_cartela = tam_cartela
        self.min = 1
        self.max = num_max
        self.quantidade = quantidade

    def __cartela_random(self):
        cartela = get_numbers(n=self.tam_cartela, min_val=self.min, max_val=self.max, repeat=False)
        return cartela

    def gerar_cartela(self):
        cartela=[]
        for x in range(0, self.quantidade):
            cartela.append(self.__cartela_random())
        return cartela


teste = Cartela(tam_cartela=25, quantidade=5,num_max=75)
print(teste.gerar_cartela())






