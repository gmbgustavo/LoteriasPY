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

MODALIDADES = {
    'Quina': Quina,
    'Duplasena': Duplasena,
    'Megasena': Megasena,
    'Diadesorte': Diadesorte,
    'Lotomania': Lotomania,
    'Lotofacil': Lotofacil,
    'Supersete': Supersete,
    'Timemania': Timemania,
    'Milionaria': Milionaria
}

# Configurações iniciais
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
mod_select = ''
volante = []
concursos = 0


def apostar(modalidade: str, dezenas: int, bolas: tuple, quantidade=1):
    global mod_select
    print(f'\nCriando seus jogos, isto pode levar até 20 segundos a depender da quantidade de apostas.')
    print(f'Inicialização de entropia...\n')
    mod_select = modalidade
    volante.clear()
    for q in range(0, quantidade):
        aposta = MODALIDADES[modalidade](dezenas=dezenas)  # (surpresinha para faltantes)
        volante.append(aposta)


def executar():
    global concursos
    global mod_select
    concursos = 1  # Quantidade de concursos, comecando com o primeiro
    print(f'Suas apostas: {volante[0:2]}...')  # Apresenta a aposta ao usuario
    print(f'Quantidade de dezenas: {len(volante[1])}')
    print(f'Modalidade: {mod_select}')
    concurso_loteria = Sorteio(mod_select)  # Cria um objeto do tipo sorteio
    time.sleep(1)
    resultado_loteria = concurso_loteria.sortear()  # Executa o sorteio e armazena na variavel

    # Medição de desempenho
    start_time = time.time()

    # Para chamar o método conferir da classe Sorteio, um objeto Sorteio deve ter sido instanciado previamente,
    # executando o método sortear()
    # Deve ser informado o parametro ao metodo conferir() a propriedade jogo do ojbeto de aposta, Megasena, Quina...
    while True not in concurso_loteria.conferir(volante):
        resultado_loteria = concurso_loteria.sortear()  # Novo sorteio
        concursos += 1  # Controla o numero de concursos
        print(f'\rConcursos {concursos:,}', end='')
    if mod_select != 'Supersete':
        resultado_loteria = sorted(list(resultado_loteria),
                                   key=lambda elem: (0, int(elem))
                                   if isinstance(elem, int) else (1, elem))
    # Calcula a quantidade de iterações por segundo para fins de métricas de desempenho
    iterations_per_second = concursos / (time.time() - start_time)


if __name__ == '__main__':
    # Apostar - Modalidade, bolas, dezenas
    apostar(modalidade='Quina', dezenas=7, bolas=(1, 28), quantidade=2)
    executar()
    # Apresenta os resultados finais
    print('\n_______________________________________________________')
    print(f'Foram necessarios {concursos:,} concursos. ')
    # print(f'Numeros sorteados: {resultado_loteria}')
    # print(f'\nSorteios por segundo: {int(iterations_per_second):,}')

