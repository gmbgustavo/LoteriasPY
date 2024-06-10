"""
Grava informações dos sorteios e conferências em arquivo CSV
"""
from pathlib import Path


class Salvadados:

    def __init__(self, dados: dict, arquivo=Path(__file__).resolve().parent / '../dados/stats_concursos.csv', modo='a'):
        self.__i = dados
        self.__arq = arquivo
        self.__modo = modo

    def grava_csv(self):
        with open(self.__arq, self.__modo) as arq_estatistica:
            arq_estatistica.writelines(str(self.__i['modalidade']) + ','
                                       + str(self.__i['dezenas']) + ','
                                       + str(self.__i['concursos']) + ','
                                       + str(self.__i['apostas']))
            arq_estatistica.write('\n')
            arq_estatistica.close()
