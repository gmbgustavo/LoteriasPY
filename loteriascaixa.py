"""
Modulo principal
"""

from API.Salvadados import *
from caixa.Sorteio import *
from API.Gerador import *

# Configuração regional
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def loteria_caixa(dezenas: int, fixados: list, qtd: int, modalidade: str, rep=1):
    print(f'\nAcessando a API RANDOM.ORG, pode levar até 30 segundos dependendo da quantidade de apostas.')
    apostas = Gerador(modalidade=modalidade,
                      dezenas=dezenas,
                      fixados=fixados,
                      quantidade=qtd)
    volante = apostas.gerajogo()   # O volante é uma lista com todos os jogos instanciados, limite 10 jogos
    concurso_loteria = Sorteio(modalidade)            # Cria um objeto do tipo sorteio

    # Para chamar o métod0 conferir da classe Sorteio, um objeto Sorteio deve ter sido instanciado previamente,
    # executando o métod0 sortear()
    # Deve ser informado o parametro ao metodo conferir() a propriedade 'jogo' do ojbeto de aposta, Megasena, Quina...
    analise = {'modalidade': modalidade, 'dezenas': len(apostas), 'concursos': 0, 'apostas': len(volante)}
    for stat in range(0, rep):
        # Medição de desempenho
        start_time = time.time()        
        estatistica = Salvadados(dados=analise)
        concursos = 1
        resultado_loteria = concurso_loteria.sortear()    # Primeiro sorteio
        if modalidade == 'Supersete':
            print(f'Suas apostas: {volante[0:]}')
        else:
            print(f'Suas apostas: {sorted(volante[0:len(volante)])}')  # Apresenta a aposta ao usuario
        print('\n' + Fore.YELLOW + f'---------------------------INÍCIO---------------------------' + Fore.RESET)
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

if __name__ == '__main__':

    loteria_caixa(dezenas=10, fixados=[], qtd=1, modalidade='Megasena', rep=1)




