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
from Sorteio import *
import time
import locale

# Configurações regionais
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

if __name__ == '__main__':
    print(f'\nCriando seus jogos, isto pode levar até 20 segundos a depender da quantidade de apostas.')
    print(f'Inicialização de entropia...\n')
    modalidade = 'Diadesorte'
    aposta1 = Diadesorte(1, 5, 6, 15, 22, 28, dezenas=8)   # (surpresinha automatica para faltantes)
    volante = [aposta1.jogo]
    concursos = 1                                     # Quantidade de concursos, comecando com o primeiro
    print(f'Suas apostas: {volante[0:2]} ...')   # Apresenta a aposta ao usuario
    print(f'Quantidade de dezenas: {len(aposta1)}')
    print(f'Modalidade: {modalidade}')
    concurso_loteria = Sorteio(modalidade)            # Cria um objeto do tipo sorteio
    time.sleep(0.6)

    # Medição de desempenho
    start_time = time.time()

    # Para chamar o método conferir da classe Sorteio, um objeto Sorteio deve ter sido instanciado previamente,
    # executando o método sortear()
    # Deve ser informado o parametro ao metodo conferir() a propriedade jogo do ojbeto de aposta, Megasena, Quina...
    analise = {}
    for stat in range(10):
        resultado_loteria = concurso_loteria.sortear()    # Primeiro sorteio
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
        print(f'\nSorteios por segundo: {int(iterations_per_second):,}')
        analise[stat] = concursos
        concursos = 0
        del resultado_loteria

    with open("dados/stats_concursos.csv", "a") as arq_estatistica:
        for i in analise.values():
            arq_estatistica.writelines(modalidade + ',' + str(len(aposta1)) + ',' + str(i))
            arq_estatistica.write('\n')
        arq_estatistica.close()
