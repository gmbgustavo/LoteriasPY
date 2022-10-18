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
    modalidade = 'Lotofacil'
    aposta1 = Lotofacil(1, 5, 6, 15, 22, 25, dezenas=15)   # (surpresinha automatica para faltantes)
    aposta2 = Lotofacil(dezenas=15)
    aposta3 = Lotofacil(dezenas=15)
    aposta4 = Lotofacil(dezenas=15)
    aposta5 = Lotofacil(dezenas=15)
    volante = [aposta1.jogo, aposta2.jogo, aposta3.jogo, aposta4.jogo, aposta5.jogo]
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

