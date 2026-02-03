# CARTELA DE BINGO PADRÃO

try:
    from API.random_api import *
except ImportError:
    # Fallback para geração local de números aleatórios
    import random
    def get_numbers(n, min_val, max_val, repeat=False):
        if repeat:
            return [random.randint(min_val, max_val) for _ in range(n)]
        else:
            return random.sample(range(min_val, max_val + 1), n)

try:
    from .Geracartela import Geracartela
except ImportError:
    # Fallback caso matplotlib não esteja disponível
    class Geracartela:
        @staticmethod
        def salva_pdf(cartelas, nome_arquivo="cartelas_bingo.pdf"):
            print(f"⚠️ Não é possível gerar PDF. matplotlib não está disponível.")
            print(f"Seriam geradas {len(cartelas)} cartelas no arquivo {nome_arquivo}")

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

    def criar_cartela_manual(self):
        """
        Cria uma cartela manualmente com input do usuário.
        Retorna uma lista com 25 números únicos.
        """
        cartela = []
        numeros_usados = set()
        
        print(f"\n📝 CRIAÇÃO DE CARTELA MANUAL")
        print(f"Digite {self.tam_cartela} números entre {self.min} e {self.max}")
        print("=" * 50)
        
        while len(cartela) < self.tam_cartela:
            try:
                numero = int(input(f"Digite o {len(cartela) + 1}º número ({self.min}-{self.max}): "))
                
                if numero < self.min or numero > self.max:
                    print(f"❌ Número inválido! Digite um número entre {self.min} e {self.max}.")
                    continue
                
                if numero in numeros_usados:
                    print(f"⚠️ Número {numero} já foi digitado! Escolha outro número.")
                    continue
                
                cartela.append(numero)
                numeros_usados.add(numero)
                print(f"✅ Número {numero} adicionado")
                
            except ValueError:
                print("❌ Digite um número válido!")
        
        return sorted(cartela)

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
