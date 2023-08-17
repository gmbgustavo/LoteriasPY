"""
Modulo principal
"""

from Megasena import *
from Diadesorte import *
from Lotofacil import *
from Quina import *
from Duplasena import *
from Lotomania import *
from Milionaria import *
from Supersete import *
from Timemania import *
from Salvadados import *
from Sorteio import *
import time
import locale
import argparse
from colorama import Fore

# Configurações regionais
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

if __name__ == '__main__':
    print(f'\nCriando seus jogos, isto pode levar até 20 segundos a depender da quantidade de apostas.')
    print(f'Inicialização de entropia...\n')
    modalidade = 'Megasena'
    aposta1 = Megasena(1, 5, 6, 15, 22, 28, dezenas=6)   # (surpresinha automatica para faltantes)
    aposta2 = Megasena(dezenas=6)
    volante = [aposta1.jogo, aposta2.jogo]
    print(f'Suas apostas: {volante[0:2]} ...')   # Apresenta a aposta ao usuario
    print(f'Quantidade de dezenas: {len(aposta1)}')
    print(f'Modalidade: {modalidade}')
    concurso_loteria = Sorteio(modalidade)            # Cria um objeto do tipo sorteio
    time.sleep(0.2)

    # Para chamar o método conferir da classe Sorteio, um objeto Sorteio deve ter sido instanciado previamente,
    # executando o método sortear()
    # Deve ser informado o parametro ao metodo conferir() a propriedade jogo do ojbeto de aposta, Megasena, Quina...
    analise = {'modalidade': modalidade, 'dezenas': len(aposta1), 'concursos': 0, 'apostas': len(volante)}
    for stat in range(1000):
        # Medição de desempenho
        start_time = time.time()
        estatistica = Salvadados(dados=analise)
        concursos = 1
        resultado_loteria = concurso_loteria.sortear()    # Primeiro sorteio
        print(Fore.RED + f'Iteração {stat}' + Fore.RESET)
        while True not in concurso_loteria.conferir(volante):
            resultado_loteria = concurso_loteria.sortear()    # Novo sorteio
            concursos += 1                                    # Controla o numero de concursos
            print(f'\rConcursos {concursos:,}', end='')
        if modalidade != 'Supersete':
            resultado_loteria = sorted(list(resultado_loteria),
                                       key=lambda elem: (0, int(elem))
                                       if isinstance(elem, int) else (1, elem))

        # Calcula a quantidade de iterações por segundo para fins de métricas de desempenho
        iterations_per_second = concursos / (time.time() - start_time)

        # Apresenta os resultados finais
        print('\n\n_______________________________________________________')
        print(Fore.LIGHTYELLOW_EX + f'Foram necessarios {concursos:,} concursos. ')
        print(Fore.GREEN + f'Numeros sorteados: {resultado_loteria}')
        print(Fore.LIGHTBLUE_EX + f'\nSorteios por segundo: {int(iterations_per_second):,}\n\n' + Fore.RESET)

        analise['concursos'] = concursos
        estatistica.grava_csv()
        del estatistica
        del resultado_loteria
