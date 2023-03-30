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
import time
from Sorteio import *


if __name__ == '__main__':
    print(f'\nCriando seus jogos, isto pode levar até 20 segundos a depender da quantidade de apostas.')
    print(f'Inicialização de entropia...\n')
    modalidade = 'Supersete'
    aposta1 = Supersete(dezenas=7)   # (surpresinha automatica para faltantes)
    aposta2 = Supersete(dezenas=15)
    volante = [aposta1.jogo, aposta2.jogo]
    concursos = 1                                     # Quantidade de concursos, comecando com o primeiro
    print(f'Suas apostas: {volante}')                 # Apresenta a aposta ao usuario
    print(f'Quantidade de dezenas: {len(aposta1)}')
    print(f'Modalidade: {modalidade}')
    concurso_loteria = Sorteio(modalidade)            # Cria um objeto do tipo sorteio
    time.sleep(1)
    resultado_loteria = concurso_loteria.sortear()    # Executa o sorteio e armazena na variavel

    # Medição de desempenho
    start_time = time.time()

    # Para chamar o método conferir da classe Sorteio, um objeto Sorteio deve ter sido instanciado previamente,
    # executando o método sortear()
    # Deve ser informado o parametro ao metodo conferir() a propriedade jogo do ojbeto de aposta, Megasena, Quina...
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
    print('\n_______________________________________________________')
    print(f'Foram necessarios {concursos:,} concursos. ')
    print(f'Numeros sorteados: {resultado_loteria}')
    print(f'\nSorteios por segundo: {int(iterations_per_second)}', sep='.')

