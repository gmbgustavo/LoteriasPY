"""
Modulo principal
"""
import time

from Megasena import *
from Lotofacil import *
from Timemania import *
from Quina import *
from Lotomania import *
from Diadesorte import *
from Supersete import *
from API.Salvadados import *
from Sorteio import *
from colorama import Fore
from API.helpers import *

# Configuração regional
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

if __name__ == '__main__':
    modalidade = 'Megasena'
    aposta1 = Megasena(1, 2, 3, 4, 5, 6, dezenas=6)
    volante = [aposta1.jogo]    # O volante é uma lista com todos os jogos instanciados, limite 10 jogos
    concurso_loteria = Sorteio(modalidade)            # Cria um objeto do tipo sorteio
    print(f'\nCriando seus jogos, isto pode levar até 20 segundos dependendo da quantidade de apostas.')

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
        print('\n' + Fore.YELLOW + f'---------------------------INÍCIO---------------------------' + Fore.RESET)
        if modalidade == 'Supersete':
            print(f'Suas apostas: {volante}')
        else:
            print(f'Suas apostas: {sorted(volante[0:len(volante)])}')  # Apresenta a aposta ao usuario
        print(f'Quantidade de dezenas: {len(aposta1)}')
        print(f'Modalidade: {modalidade}')
        print(Fore.RED + f'Iteração {stat + 1}' + Fore.RESET)
        while True not in concurso_loteria.conferir(volante):
            resultado_loteria = concurso_loteria.sortear()    # Novo sorteio
            concursos += 1                                    # Controla o numero de concursos
            print(f'\rConcursos {concursos:,}', end='')

        # Calcula a quantidade de iterações por segundo para fins de métricas de desempenho
        tempototal = time.time() - start_time

        # Apresenta os resultados finais
        print(Fore.LIGHTYELLOW_EX + f'Foram necessarios {concursos:,} concursos. ')
        print(Fore.RED + f'Numeros sorteados: {resultado_loteria}')
        print(Fore.LIGHTBLUE_EX + f'\nTempo total: {tempototal:.2f} segundos\n' + Fore.RESET)
        print(f'\n\n-----------------------FIM-----------------------')

        analise['concursos'] = concursos
        estatistica.grava_csv()
        del estatistica
        del resultado_loteria
