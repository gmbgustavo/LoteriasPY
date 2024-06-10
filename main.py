"""
Modulo principal
"""

from Megasena import *
from Timemania import *
from Quina import *
from Diadesorte import *
from API.Salvadados import *
from Sorteio import *
from colorama import Fore
from API.helpers import *

# Configuração regional
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

if __name__ == '__main__':
    modalidade = 'Quina'
    aposta1 = Quina(1, dezenas=7)
    volante = [aposta1.jogo]    # O volante é uma lista com todos os jogos instanciados, limite 10 jogos
    concurso_loteria = Sorteio(modalidade)            # Cria um objeto do tipo sorteio
    print(f'\nCriando seus jogos, isto pode levar até 20 segundos a depender da quantidade de apostas.')
    print(f'Inicialização de entropia...\n')

    # Para chamar o método conferir da classe Sorteio, um objeto Sorteio deve ter sido instanciado previamente,
    # executando o método sortear()
    # Deve ser informado o parametro ao metodo conferir() a propriedade 'jogo' do ojbeto de aposta, Megasena, Quina...
    analise = {'modalidade': modalidade, 'dezenas': len(aposta1), 'concursos': 0, 'apostas': len(volante)}
    for stat in range(1):
        # Medição de desempenho
        start_time = time.time()
        estatistica = Salvadados(dados=analise)
        concursos = 1
        resultado_loteria = concurso_loteria.sortear()    # Primeiro sorteio
        print(Fore.YELLOW + f'-----------------------INÍCIO-----------------------' + Fore.RESET)
        print(f'Suas apostas: {sorted(volante[0:len(volante)])}')  # Apresenta a aposta ao usuario
        print(f'Quantidade de dezenas: {len(aposta1)}')
        print(f'Modalidade: {modalidade}')
        print(Fore.RED + f'Iteração {stat + 1}' + Fore.RESET)
        while True not in concurso_loteria.conferir(volante):
            resultado_loteria = concurso_loteria.sortear()    # Novo sorteio
            concursos += 1                                    # Controla o numero de concursos
            print(f'\rConcursos {concursos:,}', end='')

        # Calcula a quantidade de iterações por segundo para fins de métricas de desempenho
        iterations_per_second = concursos / (time.time() - start_time)

        # Apresenta os resultados finais
        print(f'\n\n-----------------------FIM-----------------------')
        print(Fore.LIGHTYELLOW_EX + f'Foram necessarios {concursos:,} concursos. ')
        print(Fore.GREEN + f'Numeros sorteados: {resultado_loteria}')
        print(Fore.LIGHTBLUE_EX + f'\nSorteios por segundo: {int(iterations_per_second):,}\n' + Fore.RESET)

        analise['concursos'] = concursos
        estatistica.grava_csv()
        del estatistica
        del resultado_loteria
