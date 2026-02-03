#!/usr/bin/env python3
import sys
sys.path.append('')
from bingo import *

TAM_CARTELA = 25

def main():
    print("🎲 BINGO DA AMIZADE 🎲")
    print("=" * 40)
    
    # Menu de escolha
    while True:
        print("\nEscolha o modo de jogo:")
        print("1 - Sorteio Automático")
        print("2 - Conferência Manual")
        print("3 - Sorteio Apenas")
        print("4 - Gerar Cartelas em PDF")
        print("5 - Sair")
        
        escolha = input("\nDigite sua opção (1-5): ").strip()
        
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
            modo_gerar_pdf()
            break
        elif escolha == '5':
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

def modo_automatico():
    # Instancia a Cumbuca1
    cumbuca = Cumbuca()
    qtde = -1
    while qtde not in range(1, 100):
        try:
            qtde = int(input("Quantas cartelas? (1 - 99):  "))
        except ValueError:
            print("❌ Digite um número válido!")

    cartelas = Cartela(tam_cartela=TAM_CARTELA, quantidade=qtde, num_max=75)
    
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
        print(f"🎲 Histórico: {' - '.join(map(str, numeros_ordenados))}")
        
        print(f"📋 Total de números sorteados: {len(numeros_sorteados_global)}")
        print(f"📋 Números restantes: {len(cumbuca.numeros)}")

def modo_manual():
    # Instancia a Cumbuca
    cumbuca = Cumbuca()

    qtde = -1
    while qtde not in range(1, 100):
        try:
            qtde = int(input("Quantas cartelas? (1 - 99):  "))
        except ValueError:
            print("❌ Digite um número válido!")

    cartelas = Cartela(tam_cartela=TAM_CARTELA, quantidade=qtde, num_max=75)
    
    # Exibe as cartelas iniciais
    print("\n🎲 CARTELAS INICIAIS 🎲")
    cartelas.print_cartela()
    
    # Chama a conferência manual
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

def modo_gerar_pdf():
    print("\n📄 GERADOR DE CARTELAS EM PDF 📄")
    print("=" * 40)
    
    # Solicita quantidade de cartelas
    while True:
        try:
            quantidade = int(input("Quantas cartelas deseja gerar? (1-99): ").strip())
            if 1 <= quantidade <= 99:
                break
            else:
                print("❌ Quantidade deve estar entre 1 e 99!")
        except ValueError:
            print("❌ Digite um número válido!")
    
    # Solicita nome do arquivo
    nome_arquivo = input("Nome do arquivo PDF (ex: cartelas.pdf): ").strip()
    if not nome_arquivo.lower().endswith('.pdf'):
        nome_arquivo += '.pdf'
    
    # Gera as cartelas
    print(f"\n🎲 Gerando {quantidade} cartela(s)...")
    cartelas = Cartela(tam_cartela=25, quantidade=quantidade, num_max=75)
    
    # Salva em PDF
    from bingo import Geracartela
    Geracartela.salva_pdf(cartelas.cartela, nome_arquivo)
    
    # Pergunta se deseja visualizar as cartelas
    visualizar = input("\nDeseja visualizar as cartelas geradas? (S/N): ").strip().upper()
    if visualizar == 'S':
        print("\n🎲 CARTELAS GERADAS 🎲")
        cartelas.print_cartela()

if __name__ == "__main__":
    main()
