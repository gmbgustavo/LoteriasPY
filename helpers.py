# Funções para uso comum

import csv


def load_csv():
    with open('./dados/megasena.csv') as megasena:
        reader = csv.reader(megasena)
        for linha in reader:
            yield set(linha[2:8])


def confere_mega_hist(aposta: set):
    cont = 1
    quinas = 0
    quadras = 0
    senas = 0
    for sorteio in load_csv():
        if cont == 1:    # Remove o cabeçalho
            cont = -1
            continue
        convertido = [eval(i) for i in sorteio]
        convertido = set(convertido)
        pontos = len(convertido.difference(aposta))
        if pontos == 0:
            senas += 1
        elif pontos == 1:    # Há apenas um elemento diferente, então há 5 iguais. (elementos totais = 6)
            quinas += 1
        elif pontos == 2:
            quadras += 1
    print(f'Senas: {senas},\nQuinas: {quinas},\nQuadras {quadras}.')


if __name__ == '__main__':
    confere_mega_hist({1, 5, 6, 15, 22, 28})
