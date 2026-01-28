#!/usr/bin/env python3
from bingo.Cumbuca import Cumbuca
from bingo.Cartela import Cartela

def main():
    print("🎲 BINGO LOTERIASPY 🎲")
    print("=" * 40)
    
    # Menu de escolha
    while True:
        print("\nEscolha o modo de jogo:")
        print("1 - Sorteio Automático")
        print("2 - Conferência Manual")
        print("3 - Sorteio Apenas")
        print("4 - Sair")
        
        escolha = input("\nDigite sua opção (1-4): ").strip()
        
        if escolha == '1':
            modo_automatico()
            break
        elif escolha == '2':
            modo_manual()
            break
        elif escolha == '3':
            modo_sorteio_apenas()
            break
        elif escolha == '4':
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

def modo_automatico():
    # Instancia a Cumbuca
    cumbuca = Cumbuca()
    
    # Instancia 3 cartelas de bingo
    cartelas = Cartela(tam_cartela=25, quantidade=3, num_max=75)
    
    # Exibe as cartelas iniciais
    print("\n🎲 CARTELAS INICIAIS 🎲")
    cartelas.print_cartela()
    
    # Controle dos números sorteados para cada cartela e global
    numeros_sorteados_por_cartela = [set() for _ in range(cartelas.quantidade)]
    numeros_sorteados_global = set()
    
    print("\n🎮 MODO AUTOMÁTICO INICIADO! Pressione Enter para sortear um número (ou 'q' para sair)")
    print("=" * 70)
    
    while True:
        entrada = input("\n👆 Pressione Enter para sortear um número...").strip().lower()
        if entrada == 'q':
            break
        
        # Sorteia um número
        numero_sorteado = cumbuca.sortear()
        
        if numero_sorteado is None:
            print("\n🏁 Todos os números foram sorteados!")
            break
        
        print(f"\n🎯 NÚMERO SORTEADO: {numero_sorteado}")
        
        # Adiciona ao controle global
        numeros_sorteados_global.add(numero_sorteado)
        
        # Atualiza o controle de números sorteados por cartela
        for i, cartela_atual in enumerate(cartelas.cartela):
            if numero_sorteado in cartela_atual:
                numeros_sorteados_por_cartela[i].add(numero_sorteado)
        
        # Verifica se alguma cartela está completa
        for i, numeros_sorteados in enumerate(numeros_sorteados_por_cartela):
            if len(numeros_sorteados) == 25:
                print(f"\n🎊🎉 BINGO! CARTELA {i + 1} COMPLETA! 🎉🎊")
                print(f"Parabéns! Todos os números da Cartela {i + 1} foram sorteados!")
                
                # Exibe a cartela vencedora
                print(f"\n🏆 CARTELA VENCEDORA {i + 1}")
                cartelas.print_cartela()
                return
        
        # Mostra estatísticas
        print("\n📊 ESTATÍSTICAS:")
        for i, numeros_sorteados in enumerate(numeros_sorteados_por_cartela):
            print(f"Cartela {i + 1}: {len(numeros_sorteados)}/25 números")
        
        # Exibe números sorteados em sequência
        numeros_ordenados = sorted(numeros_sorteados_global)
        print(f"🎲 Números sorteados: {' - '.join(map(str, numeros_ordenados))}")
        
        print(f"📋 Total de números sorteados: {len(numeros_sorteados_global)}")
        print(f"📋 Números restantes: {len(cumbuca.numeros)}")

def modo_manual():
    # Instancia a Cumbuca
    cumbuca = Cumbuca()
    
    # Instancia 3 cartelas de bingo
    cartelas = Cartela(tam_cartela=25, quantidade=3, num_max=75)
    
    # Exibe as cartelas iniciais
    print("\n🎲 CARTELAS INICIAIS 🎲")
    cartelas.print_cartela()
    
    # Chama o método de conferência manual
    cumbuca.conferir_manual(cartelas.cartela)

def modo_sorteio_apenas():
    # Instancia a Cumbuca
    cumbuca = Cumbuca()
    
    numeros_sorteados_global = set()
    
    print("\n🎲 MODO DE SORTEIO APENAS 🎲")
    print("Use os números sorteados em sua cartela física")
    print("Pressione Enter para sortear um número (ou 'fim' para encerrar)")
    print("=" * 60)
    
    while True:
        entrada = input("\n👆 Pressione Enter para sortear...").strip().lower()
        if entrada == 'fim':
            break
        
        # Sorteia um número
        numero_sorteado = cumbuca.sortear()
        
        if numero_sorteado is None:
            print("\n🏁 Todos os números foram sorteados!")
            break
        
        print(f"\n🎯 NÚMERO SORTEADO: {numero_sorteado}")
        
        # Adiciona ao controle global
        numeros_sorteados_global.add(numero_sorteado)
        
        # Exibe números sorteados em sequência
        numeros_ordenados = sorted(numeros_sorteados_global)
        print(f"🎲 Números sorteados: {' - '.join(map(str, numeros_ordenados))}")
        print(f"📋 Total de números sorteados: {len(numeros_sorteados_global)}")
        print(f"📋 Números restantes: {len(cumbuca.numeros)}")
    
    # Exibe resultado final
    if numeros_sorteados_global:
        numeros_ordenados = sorted(numeros_sorteados_global)
        print(f"\n" + "=" * 60)
        print(f"🏁 SORTEIO FINALIZADO")
        print("=" * 60)
        print(f"🎲 Todos os números sorteados:")
        print(f"{' - '.join(map(str, numeros_ordenados))}")
        print(f"\n📋 Total de números sorteados: {len(numeros_sorteados_global)}")
    else:
        print("\nNenhum número foi sorteado.")

if __name__ == "__main__":
    main()
