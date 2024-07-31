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
from API.Gerador import *

# Configuração regional
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

if __name__ == '__main__':
    modalidade = 'Lotofacil'
    print(f'\nComunicando com a API Random.org, pode levar até 20 segundos dependendo da quantidade de apostas.')
    apostas = Gerador(modalidade=modalidade, dezenas=16, quantidade=9, fixados=[])
    volante = apostas.gerajogo()    # O volante é uma lista com todos os jogos instanciados, limite 10 jogos
    concurso_loteria = Sorteio(modalidade)            # Cria um objeto do tipo sorteio

    # Para chamar o método conferir da classe Sorteio, um objeto Sorteio deve ter sido instanciado previamente,
    # executando o método sortear()
    # Deve ser informado o parametro ao metodo conferir() a propriedade 'jogo' do ojbeto de aposta, Megasena, Quina...
    analise = {'modalidade': modalidade, 'dezenas': len(apostas), 'concursos': 0, 'apostas': len(volante)}
    for stat in range(1):
        # Medição de desempenho
        start_time = time.time()
        estatistica = Salvadados(dados=analise)
        concursos = 1
        resultado_loteria = concurso_loteria.sortear()    # Primeiro sorteio
        if modalidade == 'Supersete':
            print(f'Suas apostas: {volante[0]}')
        else:
            print(f'Suas apostas: {sorted(volante[0:len(volante)])}')  # Apresenta a aposta ao usuario
        print('\n' + Fore.YELLOW + f'---------------------------INÍCIO---------------------------' + Fore.RESET)
        print(f'Quantidade de dezenas: {len(apostas[-1])}')
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
