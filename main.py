"""
Modulo principal
"""

from Megasena import Megasena

import Sorteio


if __name__ == '__main__':
    modalidade = 'Megasena'
    aposta1 = Megasena(1, 5, 6, 15, 22, 28, dezenas=6)   # (surpresinha automatica para faltantes)
    volante = [aposta1.jogo]
    concursos = 1                                        # Quantidade de concursos, comecando com o primeiro
    print(f'Suas apostas: {volante}')    # Apresenta a aposta ao usuario
    print(f'Quantidade de dezenas: {len(aposta1)}')
    concurso_loteria = Sorteio.Sorteio(modalidade)          # Cria um objeto do tipo sorteio
    resultado_loteria = concurso_loteria.sortear()       # Executa o sorteio e armazena na variavel

    # Para chamar o método conferir da classe Sorteio, um objeto Sorteio deve ter sido instanciado previamente,
    # executando o método sortear()e
    # Deve ser informado o parametro ao metodo conferir() a propriedade jogo do ojbeto de aposta, Megasena, Quina...
    while True not in concurso_loteria.conferir(*volante):
        resultado_loteria = concurso_loteria.sortear()    # Novo sorteio
        concursos += 1                                      # Controla o numero de concursos
        print(f'\rConcursos {concursos:,}', end='')
    resultado_loteria = sorted(list(resultado_loteria),
                               key=lambda elem: (0, int(elem)) if isinstance(elem, int) else (1, elem))

    print('\n_______________________________________________________')
    print(f'Foram necessarios {concursos:,} concursos. ')
    print(f'Numeros sorteados: {resultado_loteria}')

