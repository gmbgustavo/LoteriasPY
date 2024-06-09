# Funções para uso comum

import csv
import pandas as pd


def load_csv():
    with open('./dados/megasena.csv') as megasena:
        reader = csv.reader(megasena)
        for linha in reader:
            yield linha


def pandas_read_csv():
    dataframe = pd.read_csv('./dados/megasena.csv')
    for row in dataframe:
        yield dataframe


def confere_mega_hist(aposta: set):
    cont = 1
    quinas = 0
    quadras = 0
    senas = 0
    vencedor_sena = -1
    for sorteio in load_csv():
        if cont == 1:    # Remove o cabeçalho
            cont = -1
            continue
        convertido = [eval(i) for i in sorteio[2:8]]
        convertido = set(convertido)
        concurso = sorteio[0]
        pontos = len(convertido.difference(aposta))
        if pontos == 0:    # Todos os elementos são iguais, logo acertou todas as 6 dezenas.
            senas += 1
            vencedor_sena = concurso
        elif pontos == 1:    # Há apenas um elemento diferente, então há 5 iguais (quina). (elementos totais = 6)
            quinas += 1
        elif pontos == 2:    # Há dois elementos diferente, então há 4 iguais (quadra). (elementos totais = 6)
            quadras += 1
    print(f'Senas: {senas} (concurso {vencedor_sena}),\nQuinas: {quinas},\nQuadras {quadras}.')


if __name__ == '__main__':
    quit(3)


