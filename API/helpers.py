# Funções para uso comum

import csv
from pathlib import Path


MEGASENA = Path(__file__).resolve().parent / '../dados/megasena.csv'
QUINA = Path(__file__).resolve().parent / '../dados/quina.csv'
LOTOFACIL = Path(__file__).resolve().parent / '../dados/lotofacil.csv'


def read_csv_lines(arquivo_csv):
    assert arquivo_csv is not None, 'Arquivo não encontrado'
    with open(arquivo_csv) as m:
        reader = csv.reader(m)
        for linha in reader:
            yield linha


def confere_mega_hist(aposta: set):
    cont = 1
    quinas = 0
    quadras = 0
    senas = 0
    vencedor_sena = -1
    for sorteio in read_csv_lines(MEGASENA):
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


def confere_quina_hist(aposta: set):
    cont = 1
    quinas = 0
    quadras = 0
    vencedor_sena = -1
    for sorteio in read_csv_lines(QUINA):
        if cont == 1:    # Remove o cabeçalho
            cont = -1
            continue
        convertido = [eval(i) for i in sorteio[2:7]]
        convertido = set(convertido)
        concurso = sorteio[0]
        pontos = len(convertido.difference(aposta))
        if pontos == 0:    # Todos os elementos são iguais, logo, acertou todas as 5 dezenas.
            quinas += 1
            vencedor_sena = concurso
        elif pontos == 1:    # Há apenas um elemento diferente, então há 5 iguais (quina). (elementos totais = 6)
            quadras += 1
    print(f'Quinas: {quinas} (concurso {vencedor_sena}),\nQuadras {quadras}.')


def confere_lotofacil_hist(aposta: set):
    cont = 1
    quinze = 0
    quatorze = 0
    concurso_vencedor = -1
    for sorteio in read_csv_lines(LOTOFACIL):
        if cont == 1:  # Remove o cabeçalho
            cont = -1
            continue
        convertido = [eval(i) for i in sorteio[2:17]]
        convertido = set(convertido)
        concurso = sorteio[0]
        pontos = len(convertido.difference(aposta))
        if pontos == 0:  # Todos os elementos são iguais, logo, acertou tudo.
            quinze += 1
            concurso_vencedor = concurso
        elif pontos == 1:  # Há apenas um elemento diferente, então há 5 iguais (quina). (elementos totais = 6)
            quatorze += 1
    print(f'Quinze acertos: {quinze} (concurso {concurso_vencedor}),\nQuatorze acertos {quatorze}.')


def apostas_lote(qtde: int):
    pass


if __name__ == '__main__':
    confere_lotofacil_hist({8, 22, 5, 14, 16, 9, 23, 11, 7, 2, 13, 25, 24, 18, 17})
    quit(3)


