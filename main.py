"""
Modulo principal
"""

from Megasena import Megasena
from Duplasena import Duplasena
from Quina import Quina
from Lotofacil import Lotofacil
from Lotomania import Lotomania
from Diadesorte import Diadesorte
import Sorteio
from time import time
import sys
# import tela_principal


if __name__ == '__main__':
    parametros = sys.argv
    aposta1 = Lotofacil()   # Cria uma nova aposta (se vazio faz surpresinha)
    concursos = 1                                        # Quantidade de concursos, comecando com o primeiro
    print(f'Sua aposta1: {aposta1}')                     # Apresenta a aposta ao usuario
    concurso_loteria = Sorteio.Sorteio(aposta1)          # Cria um objeto do tipo sorteio
    resultado_loteria = concurso_loteria.resultado       # Executa o sorteio e armazena na variavel

    while concurso_loteria.conferir(aposta1.jogo) < concurso_loteria.sorteio_len:
        resultado_loteria = concurso_loteria.resultado()    # Novo sorteio
        concursos += 1                                      # Controla o numero de concursos
        print(f'\rConcursos {concursos:,}', end='')

    print(f'\n\nForam necessarios {concursos:,} concursos. ')
#   print(f'Media de tempo a cada 50 mil calculos foi de {round(tempo_medio_final, 2)} segundos')
    print(f'Numeros sorteados: {resultado_loteria}')
