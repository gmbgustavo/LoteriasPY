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


if __name__ == '__main__':
    aposta1 = Diadesorte(1, 5, 6, 15, 22, 28, dezenas=10)   # (surpresinha automatica para faltantes)
    concursos = 1                                        # Quantidade de concursos, comecando com o primeiro
    print(f'Sua aposta: {aposta1}')                     # Apresenta a aposta ao usuario
    print(f'Quantidade de dezenas: {len(aposta1)}')
    concurso_loteria = Sorteio.Sorteio(aposta1)          # Cria um objeto do tipo sorteio
    resultado_loteria = concurso_loteria.resultado       # Executa o sorteio e armazena na variavel

    while concurso_loteria.conferir(aposta1.jogo) < concurso_loteria.sorteio_len:
        resultado_loteria = concurso_loteria.resultado()    # Novo sorteio
        concursos += 1                                      # Controla o numero de concursos
        print(f'\rConcursos {concursos:,}', end='')
    resultado_loteria = list(resultado_loteria)
    resultado_loteria.sort(key=lambda ele: (0, int(ele)) if isinstance(ele, int) else (1, ele))

    print('\n_______________________________________________________')
    print(f'Foram necessarios {concursos:,} concursos. ')
    print(f'Numeros sorteados: {resultado_loteria}')

