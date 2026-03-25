"""
Modulo principal
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from API.Salvadados import *
from Caixa.Sorteio import *
from API.Gerador import *

# Configuração regional
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def gerar_apenas_numeros(dezenas: int, fixados: list, qtd: int, modalidade: str):
    """
    Função simplificada que apenas gera e exibe as apostas formatadas
    """
    print(f'\n🎲 Gerando apostas para {modalidade}...')
    print('Acessando a API RANDOM.ORG, pode levar até 30 segundos dependendo da quantidade de apostas.')
    
    try:
        apostas = Gerador(modalidade=modalidade,
                          dezenas=dezenas,
                          fixados=fixados,
                          quantidade=qtd)
        volante = apostas.gerajogo()   # O volante é uma lista com todos os jogos instanciados
        
        print(f'\n✅ {qtd} APOSTA(S) GERADA(S) PARA {modalidade.upper()}')
        print('=' * 60)
        
        # Formatação melhorada das apostas
        formatar_apostas(volante, modalidade)
        
    except Exception as e:
        print(f'❌ Erro ao gerar apostas: {e}')

def formatar_apostas(volante: list, modalidade: str):
    """
    Formata as apostas para exibição mais legível
    """
    for i, aposta in enumerate(volante, 1):
        print(f'\n🎫 APOSTA {i}:')
        
        if modalidade == 'Supersete':
            # Supersetê tem formato especial (colunas)
            if hasattr(aposta, '_Supersete__colunas'):
                for j, coluna in enumerate(aposta._Supersete__colunas, 1):
                    print(f'   Coluna {j}: {coluna}')
            else:
                print(f'   Números: {aposta}')
        elif modalidade == 'Timemania':
            # Timemania tem time do coração
            if hasattr(aposta, '_Timemania__timedocoracao') and aposta._Timemania__timedocoracao != -1:
                print(f'   Time do coração: {aposta._Timemania__timedocoracao}')
            if hasattr(aposta, '_Timemania__jogo'):
                numeros = sorted(aposta._Timemania__jogo)
                print(f'   Números: {formatar_lista(numeros)}')
            else:
                print(f'   Números: {sorted(aposta)}')
        elif modalidade == 'Diadesorte':
            # Dia de Sorte tem mês do sorteio
            if hasattr(aposta, '_Diadesorte__mes'):
                meses = ('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez')
                mes_nome = meses[aposta._Diadesorte__mes] if aposta._Diadesorte__mes < len(meses) else 'desconhecido'
                print(f'   Mês da sorte: {mes_nome}')
            if hasattr(aposta, '_Diadesorte__jogo'):
                numeros = sorted(n for n in aposta._Diadesorte__jogo if isinstance(n, int))
                print(f'   Números: {formatar_lista(numeros)}')
            else:
                print(f'   Números: {sorted(n for n in aposta if isinstance(n, int))}')
        else:
            # Modalidades padrão (Mega-Sena, Quina, Lotofácil, Lotomania)
            try:
                # Tenta acessar o atributo jogo do objeto
                if hasattr(aposta, '_Megasena__jogo'):
                    numeros = sorted(aposta._Megasena__jogo)
                elif hasattr(aposta, '_Quina__jogo'):
                    numeros = sorted(aposta._Quina__jogo)
                elif hasattr(aposta, '_Lotofacil__jogo'):
                    numeros = sorted(aposta._Lotofacil__jogo)
                elif hasattr(aposta, '_Lotomania__jogo'):
                    numeros = sorted(aposta._Lotomania__jogo)
                else:
                    # Fallback para lista direta
                    numeros = sorted(aposta) if isinstance(aposta, list) else aposta
                
                print(f'   Números: {formatar_lista(numeros)}')
                
            except:
                # Fallback final
                print(f'   Números: {sorted(aposta) if isinstance(aposta, list) else aposta}')

def formatar_lista(numeros: list) -> str:
    """
    Formata uma lista de números para exibição legível
    """
    if not numeros:
        return "[]"
    
    # Se tiver muitos números, quebra em linhas
    if len(numeros) > 15:
        metade = len(numeros) // 2
        primeira = numeros[:metade]
        segunda = numeros[metade:]
        return f"[{', '.join(map(str, primeira))},\n         {', '.join(map(str, segunda))}]"
    else:
        return f"[{', '.join(map(str, numeros))}]"

def loteria_caixa(dezenas: int, fixados: list, qtd: int, modalidade: str, rep=1):
    """
    Função original mantida para o loop até vencer
    """
    print(f'\nAcessando a API RANDOM.ORG, pode levar até 30 segundos dependendo da quantidade de apostas.')
    apostas = Gerador(modalidade=modalidade,
                      dezenas=dezenas,
                      fixados=fixados,
                      quantidade=qtd)
    volante = apostas.gerajogo()   # O volante é uma lista com todos os jogos instanciados, limite 10 jogos
    concurso_loteria = Sorteio(modalidade)            # Cria um objeto do tipo sorteio

    # Para chamar o métod0 conferir da classe Sorteio, um objeto Sorteio deve ter sido instanciado previamente,
    # executando o métod0 sortear()
    # Deve ser informado o parametro ao metodo conferir() a propriedade 'jogo' do ojbeto de aposta, Megasena, Quina...
    analise = {'modalidade': modalidade, 'dezenas': len(apostas), 'concursos': 0, 'apostas': len(volante)}
    for stat in range(0, rep):
        # Medição de desempenho
        start_time = time.time()        
        estatistica = Salvadados(dados=analise)
        concursos = 1
        resultado_loteria = concurso_loteria.sortear()    # Primeiro sorteio
        if modalidade == 'Supersete':
            print(f'Suas apostas: {volante[0:]}')
        else:
            print(f'Suas apostas: {sorted(volante[0:len(volante)])}')  # Apresenta a aposta ao usuario
        print('\n' + Fore.YELLOW + f'---------------------------INÍCIO---------------------------' + Fore.RESET)
        print(f'Modalidade: {modalidade}')
        print(Fore.RED + f'Iteração {stat + 1}' + Fore.RESET)
        while True not in concurso_loteria.conferir(volante):
            resultado_loteria = concurso_loteria.sortear()    # Novo sorteio
            concursos += 1                                    # Controla o numero de concursos
            print(f'\rConcursos {concursos:,}', end='')

        # Calcula a quantidade de iterações por segundo para fins de métricas de desempenho
        tempototal = time.time() - start_time

        # Apresenta os resultados finais
        print(Fore.LIGHTYELLOW_EX + f'\nForam necessarios {concursos:,} concursos. ')
        print(Fore.RED + f'Numeros sorteados: {resultado_loteria}')
        print(Fore.LIGHTBLUE_EX + f'\nTempo total: {tempototal:.2f} segundos' + Fore.RESET)
        print(f'\n-----------------------FIM-----------------------')

        analise['concursos'] = concursos
        estatistica.grava_csv()
        del estatistica
        del resultado_loteria

def obter_dados_modalidade(modalidade):
    """
    Retorna os dados da modalidade para validação de parâmetros
    """
    modalidades = {
        'Megasena': {
            'min_dezenas': 6,
            'max_dezenas': 15,
            'min_num': 1,
            'max_num': 60,
            'dezena_fixa': False
        },
        'Quina': {
            'min_dezenas': 5,
            'max_dezenas': 15,
            'min_num': 1,
            'max_num': 80,
            'dezena_fixa': False
        },
        'Lotofacil': {
            'min_dezenas': 15,
            'max_dezenas': 18,
            'min_num': 1,
            'max_num': 25,
            'dezena_fixa': False
        },
        'Lotomania': {
            'min_dezenas': 50,
            'max_dezenas': 50,
            'min_num': 1,
            'max_num': 100,
            'dezena_fixa': True
        },
        'Timemania': {
            'min_dezenas': 7,
            'max_dezenas': 10,
            'min_num': 1,
            'max_num': 80,
            'dezena_fixa': False,
            'parametro_extra': 'timedocoracao'
        },
        'Diadesorte': {
            'min_dezenas': 7,
            'max_dezenas': 15,
            'min_num': 1,
            'max_num': 31,
            'dezena_fixa': False
        },
        'Supersete': {
            'min_dezenas': 7,
            'max_dezenas': 7,
            'min_num': 0,
            'max_num': 9,
            'dezena_fixa': True
        }
    }
    
    return modalidades.get(modalidade, {})

def menu_modalidades():
    """
    Exibe o menu de modalidades disponíveis
    """
    print("\n🎰 MODALIDADES DISPONÍVEIS 🎰")
    print("=" * 50)
    print("1 - Mega-Sena")
    print("2 - Quina")
    print("3 - Lotofácil")
    print("4 - Lotomania")
    print("5 - Timemania")
    print("6 - Dia de Sorte")
    print("7 - Supersetê")
    print("=" * 50)

def validar_numero_inteiro(mensagem, min_val=None, max_val=None):
    """
    Valida entrada de número inteiro com opcionais limites
    """
    while True:
        try:
            valor = int(input(mensagem))
            if min_val is not None and valor < min_val:
                print(f"❌ Valor mínimo é {min_val}")
                continue
            if max_val is not None and valor > max_val:
                print(f"❌ Valor máximo é {max_val}")
                continue
            return valor
        except ValueError:
            print("❌ Digite um número válido!")

def validar_lista_numeros(mensagem, qtd_numeros, min_val, max_val):
    """
    Valida entrada de lista de números
    """
    while True:
        try:
            entrada = input(mensagem).strip()
            if not entrada:
                return []
            
            numeros = []
            for num in entrada.split(','):
                num = num.strip()
                if num:
                    numeros.append(int(num))
            
            # Validação dos números
            for num in numeros:
                if num < min_val or num > max_val:
                    print(f"❌ Números devem estar entre {min_val} e {max_val}")
                    raise ValueError
            
            if len(set(numeros)) != len(numeros):
                print("❌ Não pode repetir números!")
                continue
                
            return numeros
            
        except ValueError:
            print("❌ Digite números separados por vírgula (ex: 1,2,3,4,5,6)")

def gerar_numeros():
    """
    Função para gerar números aleatórios
    """
    print("\n🎲 GERAR NÚMEROS DA SORTE 🎲")
    print("=" * 50)
    
    # Menu de modalidades
    menu_modalidades()
    modalidade_escolha = validar_numero_inteiro("Escolha a modalidade (1-7): ", 1, 7)
    
    modalidades_map = {
        1: 'Megasena',
        2: 'Quina',
        3: 'Lotofacil',
        4: 'Lotomania',
        5: 'Timemania',
        6: 'Diadesorte',
        7: 'Supersete'
    }
    
    modalidade = modalidades_map[modalidade_escolha]
    dados = obter_dados_modalidade(modalidade)
    
    print(f"\n📋 Modalidade escolhida: {modalidade}")
    print(f"📊 Faixa de números: {dados['min_num']}-{dados['max_num']}")
    print(f"📊 Faixa de dezenas: {dados['min_dezenas']}-{dados['max_dezenas']}")
    
    # Quantidade de apostas
    qtd_apostas = validar_numero_inteiro(f"\nQuantidade de apostas (1-10): ", 1, 10)
    
    # Dezenas fixas (se permitido)
    fixados = []
    if not dados.get('dezena_fixa', False):
        usar_fixos = input("\nDeseja fixar alguma dezena? (S/N): ").strip().upper()
        if usar_fixos == 'S':
            max_fixos = dados['max_dezenas'] - 1
            qtd_fixos = validar_numero_inteiro(f"Quantas dezenas fixas (1-{max_fixos}): ", 1, max_fixos)
            fixados = validar_lista_numeros(
                f"Digite as {qtd_fixos} dezenas fixas (separadas por vírgula): ",
                qtd_fixos,
                dados['min_num'],
                dados['max_num']
            )
    
    # Dezenas da aposta
    dezenas = dados['min_dezenas']
    if not dados.get('dezena_fixa', False):
        dezenas = validar_numero_inteiro(
            f"Quantidade de dezenas por aposta ({dados['min_dezenas']}-{dados['max_dezenas']}): ",
            dados['min_dezenas'],
            dados['max_dezenas']
        )
    
    # Parâmetro extra para Timemania (time do coração)
    kwargs = {}
    if modalidade == 'Timemania':
        print("\n⚽ TIMEMANIA - Time do Coração")
        print("0 - Não informar time")
        # Aqui poderíamos listar os times, mas para simplificar vamos aceitar qualquer número
        kwargs['timedocoracao'] = validar_numero_inteiro("Time do coração (0 para não informar): ", 0, 999)
    
    print(f"\n🎯 GERANDO {qtd_apostas} APOSTA(S) PARA {modalidade.upper()}...")
    print(f"📊 Dezenas: {dezenas} | Fixos: {fixados if fixados else 'Nenhum'}")
    
    # Chama a função simplificada que apenas gera as apostas
    gerar_apenas_numeros(dezenas=dezenas, fixados=fixados, qtd=qtd_apostas, modalidade=modalidade)

def loop_ate_vencer():
    """
    Função para fazer o loop até que a aposta seja ganhadora
    """
    print("\n🔄 LOOP ATÉ VENCER 🔄")
    print("=" * 50)
    
    # Menu de modalidades
    menu_modalidades()
    modalidade_escolha = validar_numero_inteiro("Escolha a modalidade (1-7): ", 1, 7)
    
    modalidades_map = {
        1: 'Megasena',
        2: 'Quina',
        3: 'Lotofacil',
        4: 'Lotomania',
        5: 'Timemania',
        6: 'Diadesorte',
        7: 'Supersete'
    }
    
    modalidade = modalidades_map[modalidade_escolha]
    dados = obter_dados_modalidade(modalidade)
    
    print(f"\n📋 Modalidade escolhida: {modalidade}")
    print(f"📊 Faixa de números: {dados['min_num']}-{dados['max_num']}")
    print(f"📊 Faixa de dezenas: {dados['min_dezenas']}-{dados['max_dezenas']}")
    
    # Quantidade de apostas
    qtd_apostas = validar_numero_inteiro(f"\nQuantidade de apostas (1-10): ", 1, 10)
    
    # Dezenas fixas (se permitido)
    fixados = []
    if not dados.get('dezena_fixa', False):
        usar_fixos = input("\nDeseja fixar alguma dezena? (S/N): ").strip().upper()
        if usar_fixos == 'S':
            max_fixos = dados['max_dezenas'] - 1
            qtd_fixos = validar_numero_inteiro(f"Quantas dezenas fixas (1-{max_fixos}): ", 1, max_fixos)
            fixados = validar_lista_numeros(
                f"Digite as {qtd_fixos} dezenas fixas (separadas por vírgula): ",
                qtd_fixos,
                dados['min_num'],
                dados['max_num']
            )
    
    # Dezenas da aposta
    dezenas = dados['min_dezenas']
    if not dados.get('dezena_fixa', False):
        dezenas = validar_numero_inteiro(
            f"Quantidade de dezenas por aposta ({dados['min_dezenas']}-{dados['max_dezenas']}): ",
            dados['min_dezenas'],
            dados['max_dezenas']
        )
    
    # Número de repetições do loop
    repeticoes = validar_numero_inteiro("\nQuantas repetições do loop deseja fazer? (1-1000): ", 1, 1000)
    
    # Parâmetro extra para Timemania
    kwargs = {}
    if modalidade == 'Timemania':
        print("\n⚽ TIMEMANIA - Time do Coração")
        kwargs['timedocoracao'] = validar_numero_inteiro("Time do coração (0 para não informar): ", 0, 999)
    
    print(f"\n🎯 INICIANDO {repeticoes} LOOP(S) PARA {modalidade.upper()}...")
    print(f"📊 Dezenas: {dezenas} | Fixos: {fixados if fixados else 'Nenhum'}")
    print("⚠️ ESTA OPERAÇÃO PODE DEMORAR VÁRIOS MINUTOS!")
    
    confirmar = input("Confirma? (S/N): ").strip().upper()
    if confirmar != 'S':
        print("❌ Operação cancelada.")
        return
    
    # Chama a função principal com o número de repetições
    loteria_caixa(dezenas=dezenas, fixados=fixados, qtd=qtd_apostas, modalidade=modalidade, rep=repeticoes)

def menu_principal():
    """
    Menu principal do programa
    """
    print("\n🎰 LOTERIAS CAIXA 🎰")
    print("=" * 50)
    print("1 - Gerar números")
    print("2 - Loop até vencer")
    print("3 - Sair")
    print("=" * 50)
    
    while True:
        escolha = validar_numero_inteiro("\nEscolha uma opção (1-3): ", 1, 3)
        
        if escolha == 1:
            gerar_numeros()
            break
        elif escolha == 2:
            loop_ate_vencer()
            break
        elif escolha == 3:
            print("👋 Até logo!")
            break

if __name__ == '__main__':
    menu_principal()




