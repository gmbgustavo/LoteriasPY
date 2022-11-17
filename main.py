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
    modalidade = 'Quina'
    aposta1 = Quina(1, 5, 6, 15, 22, 28, dezenas=6)   # (surpresinha automatica para faltantes)
    aposta2 = Quina(2, 7, 10, 21, dezenas=5)
    volante = [aposta1.jogo, aposta2.jogo]
    concursos = 1                                        # Quantidade de concursos, comecando com o primeiro
    print(f'Suas apostas: {volante}')    # Apresenta a aposta ao usuario
    print(f'Quantidade de dezenas: {len(aposta1)}')
    concurso_loteria = Sorteio.Sorteio(modalidade)          # Cria um objeto do tipo sorteio
    resultado_loteria = concurso_loteria.sortear()       # Executa o sorteio e armazena na variavel

    # Para chamar o método conferir da classe Sorteio, um objeto Sorteio deve ter sido instanciado previamente,
    # executando o método sortear()
    # Deve ser informado o parametro ao metodo conferir() a propriedade jogo do ojbeto de aposta, Megasena, Quina...
    while concurso_loteria.sorteio_len not in concurso_loteria.conferir(*volante):
        resultado_loteria = concurso_loteria.sortear()    # Novo sorteio
        concursos += 1                                      # Controla o numero de concursos
        print(f'\rConcursos {concursos:,}', end='')
    resultado_loteria = list(resultado_loteria)
    resultado_loteria.sort(key=lambda ele: (0, int(ele)) if isinstance(ele, int) else (1, ele))

    print('\n_______________________________________________________')
    print(f'Foram necessarios {concursos:,} concursos. ')
    print(f'Numeros sorteados: {resultado_loteria}')

