import random

class Cumbuca:
    def __init__(self):
        self.numeros = list(range(1, 76))
    
    def sortear(self):
        if not self.numeros:
            return None
        
        posicao = random.randint(0, len(self.numeros) - 1)
        numero_sorteado = self.numeros.pop(posicao)
        return numero_sorteado
    
    def conferir(self, numero_sorteado, cartelas):
        """
        Confere se o número sorteado existe nas cartelas e exibe as cartelas destacando o número.
        
        Args:
            numero_sorteado: Número que foi sorteado
            cartelas: Lista de listas representando as cartelas
        """
        encontrado = False
        
        for i, cartela in enumerate(cartelas):
            cartela_atual = cartela.cartela[i] if hasattr(cartela, 'cartela') else cartela
            
            if numero_sorteado in cartela_atual:
                encontrado = True
                break
        
        if encontrado:
            print(f"\n🎯 NÚMERO {numero_sorteado} ENCONTRADO NAS CARTELAS!")
            self._exibir_destacado(numero_sorteado, cartelas)
        else:
            print(f"\n❌ Número {numero_sorteado} não encontrado nas cartelas.")
    
    def _exibir_destacado(self, numero_sorteado, cartelas):
        """
        Exibe as cartelas com o número sorteado destacado.
        """
        for i, cartela_obj in enumerate(cartelas):
            cartela_atual = cartela_obj.cartela[i] if hasattr(cartela_obj, 'cartela') else cartela_obj
            # a cartela já vem na ordem coluna a coluna; ordenar a lista inteira
            # embaralharia as colunas B/I/N/G/O
            cartela_ordenada = list(cartela_atual)
            
            print(f"\n         CARTELA {i + 1}".center(30))
            print("   ╔═══╦═══╦═══╦═══╦═══╗")
            print("   ║ B ║ I ║ N ║ G ║ O ║")
            print("   ╠═══╬═══╬═══╬═══╬═══╣")
            
            for linha in range(5):
                print("   ║", end='')
                for coluna in range(5):
                    indice = coluna * 5 + linha
                    numero = cartela_ordenada[indice]
                    
                    if numero == numero_sorteado:
                        print(f"\033[91m{numero:3d}\033[0m║", end='')  # Vermelho
                    else:
                        print(f"{numero:3d}║", end='')
                print()
                
                if linha < 4:
                    print("   ╠═══╬═══╬═══╬═══╬═══╣")
            
            print("   ╚═══╩═══╩═══╩═══╩═══╝")
    
    def conferir_manual(self, cartelas):
        """
        Permite inserir números manualmente via teclado e conferir nas cartelas.
        
        Args:
            cartelas: Lista de listas representando as cartelas
        """
        numeros_inseridos = set()
        numeros_por_cartela = [set() for _ in range(len(cartelas))]
        
        print("\n🔢 MODO DE CONFERÊNCIA MANUAL")
        print("Digite os números sorteados um por vez (1-75)")
        print("Digite 'fim' para encerrar e ver o resultado final")
        print("=" * 50)
        
        while True:
            try:
                entrada = input("\nDigite um número (1-75) ou 'fim': ").strip().lower()
                
                if entrada == 'fim':
                    break
                
                numero = int(entrada)
                
                if numero < 1 or numero > 75:
                    print("❌ Número inválido! Digite um número entre 1 e 75.")
                    continue
                
                if numero in numeros_inseridos:
                    print(f"⚠️ Número {numero} já foi inserido!")
                    continue
                
                numeros_inseridos.add(numero)
                print(f"✅ Número {numero} adicionado")
                
                # Verifica em quais cartelas o número aparece
                cartela_completa_encontrada = False
                for i, cartela in enumerate(cartelas):
                    cartela_atual = cartela.cartela[i] if hasattr(cartela, 'cartela') else cartela
                    if numero in cartela_atual:
                        numeros_por_cartela[i].add(numero)
                        print(f"🎯 Número {numero} encontrado na Cartela {i + 1}")
                        
                        # Verifica se esta cartela foi completada
                        if len(numeros_por_cartela[i]) == 25:
                            cartela_completa_encontrada = True
                
                # Mostra o progresso atualizado após cada número
                print("\n📊 PROGRESSO ATUAL:")
                for i, numeros_cartela in enumerate(numeros_por_cartela):
                    acertos = len(numeros_cartela)
                    percentual = (acertos / 25) * 100
                    print(f"Cartela {i + 1}: {acertos}/25 números ({percentual:.1f}%)")
                    
                    if acertos == 25:
                        print(f"🎊🎉 BINGO! CARTELA {i + 1} COMPLETA! 🎉🎊")
                    elif acertos >= 20:
                        print(f"🔥 Quase lá! Cartela {i + 1} está quase completa!")
                    elif acertos >= 15:
                        print(f"👍 Bom progresso! Cartela {i + 1} com {acertos} acertos!")
                    elif acertos >= 10:
                        print(f"📈 Cartela {i + 1} com {acertos} acertos parciais")
                    elif acertos > 0:
                        print(f"📍 Cartela {i + 1} com {acertos} acerto(s)")
                
                # Se alguma cartela foi completada, pergunta se deseja continuar
                if cartela_completa_encontrada:
                    print("\n" + "=" * 50)
                    print("🎊 UMA OU MAIS CARTELAS FORAM COMPLETAS! 🎊")
                    print("=" * 50)
                    
                    while True:
                        continuar = input("\nDeseja continuar sorteando números? (S/N): ").strip().upper()
                        if continuar in ['S', 'N']:
                            break
                        print("❌ Digite 'S' para sim ou 'N' para não!")
                    
                    if continuar == 'N':
                        break
                
            except ValueError:
                print("❌ Entrada inválida! Digite um número ou 'fim'.")
        
        # Exibe resultado final
        print("\n" + "=" * 50)
        print("📊 RESULTADO FINAL DA CONFERÊNCIA")
        print("=" * 50)
        
        if numeros_inseridos:
            numeros_ordenados = sorted(numeros_inseridos)
            print(f"🎲 Números conferidos: {' - '.join(map(str, numeros_ordenados))}")
            print(f"\n📈 PONTUAÇÃO DAS CARTELAS:")
            
            for i, numeros_cartela in enumerate(numeros_por_cartela):
                acertos = len(numeros_cartela)
                percentual = (acertos / 25) * 100
                print(f"Cartela {i + 1}: {acertos}/25 números ({percentual:.1f}%)")
                
                if acertos == 25:
                    print(f"🎊🎉 BINGO! CARTELA {i + 1} COMPLETA! 🎉🎊")
                elif acertos >= 20:
                    print(f"🔥 Quase lá! Cartela {i + 1} está quase completa!")
                elif acertos >= 15:
                    print(f"👍 Bom progresso! Cartela {i + 1} com {acertos} acertos!")
                elif acertos >= 10:
                    print(f"📈 Cartela {i + 1} com {acertos} acertos parciais")
                elif acertos > 0:
                    print(f"📍 Cartela {i + 1} com {acertos} acerto(s)")
            
            print(f"\n📋 Total de números conferidos: {len(numeros_inseridos)}")
        else:
            print("Nenhum número foi inserido.")


