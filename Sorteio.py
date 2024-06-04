"""
Sorteia e retorna as dezenas de uma loteria especificada
"""

import random
import secrets

MODALIDADES = ['Quina', 'Megasena', 'Lotofacil', 'Lotomania', 'Timemania',
               'Diadesorte', 'Duplasena']


class Sorteio:
    MEGASENA = 6
    MAX_MEGASENA = 60
    QUINA = 5
    MAX_QUINA = 80
    LOTOFACIL = 15
    MAX_LOTOFACIL = 25
    LOTOMANIA = 20
    MAX_LOTOMANIA = 100
    DUPLASENA = 6
    MAX_DUPLASENA = 50
    DIADESORTE = 7
    MAX_DIADESORTE = 31
    MAX_TIMEMANIA = 80
    TIMEMANIA = 7
    MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

    def __init__(self, modalidade: str):
        assert modalidade in MODALIDADES, \
            f'Modalidade inválida: Válidas apenas {MODALIDADES}. Informado {modalidade}.'
        self.__modalidade = modalidade
        self.__sorteado = set()
        self.__res_duplasena1 = set()
        self.__res_duplasena2 = set()
        self.__res_supersete = list()
        self.__res_timemania = list()
        self.__gira_globo = random.shuffle    # Simula o 'embaralhamento' num globo com as bolas

    def __megasena(self) -> set:
        self.__sorteado.clear()
        numeros = [x for x in range(1, self.MAX_MEGASENA + 1)]
        self.__gira_globo(numeros)
        while len(self.__sorteado) < self.MEGASENA:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
        return self.__sorteado

    def __quina(self) -> set:
        self.__sorteado.clear()
        count = self.MAX_QUINA
        numeros = [x for x in range(1, self.MAX_QUINA + 1)]
        self.__gira_globo(numeros)
        while len(self.__sorteado) < self.QUINA:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
            count -= 1
        return self.__sorteado

    def __timemania(self) -> set:
        self.__sorteado.clear()
        numeros = [x for x in range(1, self.MAX_TIMEMANIA + 1)]
        self.__gira_globo(numeros)
        while len(self.__sorteado) < self.TIMEMANIA:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
        return self.__sorteado

    def __lotofacil(self) -> set:
        self.__sorteado.clear()
        numeros = [x for x in range(1, self.MAX_LOTOFACIL + 1)]
        self.__gira_globo(numeros)
        while len(self.__sorteado) < self.LOTOFACIL:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
        return self.__sorteado

    def __diadesorte(self) -> set:
        self.__sorteado.clear()
        numeros = [x for x in range(1, self.MAX_DIADESORTE + 1)]
        self.__gira_globo(numeros)
        while len(self.__sorteado) < self.DIADESORTE:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
        return set(self.__sorteado)

    def __lotomania(self) -> set:
        self.__sorteado.clear()
        numeros = [x for x in range(1, self.MAX_LOTOMANIA + 1)]
        self.__gira_globo(numeros)
        while len(self.__sorteado) < self.LOTOMANIA:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
        self.__res_timemania = self.__sorteado
        return set(self.__res_timemania)

    def __duplasena(self) -> list:
        """
        Executa o sorteio da Dupla sena (Dois sets de seis numeros)
        :return: Um set com a uniao dos dos sorteios, ignorando dezenas repetidas
        """
        self.__sorteado.clear()
        self.__res_duplasena1.clear()
        self.__res_duplasena2.clear()
        numeros = [x for x in range(1, self.MAX_DUPLASENA + 1)]
        self.__gira_globo(numeros)
        while len(self.__res_duplasena1) < self.DUPLASENA:
            self.__res_duplasena1.add(numeros.pop(secrets.randbelow(len(numeros))))
        del numeros

        numeros = [x for x in range(1, self.MAX_DUPLASENA + 1)]
        self.__gira_globo(numeros)
        while len(self.__res_duplasena2) < self.DUPLASENA:
            self.__res_duplasena2.add(numeros.pop(secrets.randbelow(len(numeros))))
        return [self.__res_duplasena1, self.__res_duplasena2]

    @property    # Propriedade para exibir os sorteios da Dupla sena de forma separada.
    def sorteio_duplasena(self):
        return [self.__res_duplasena1, self.__res_duplasena2]

    @property
    def modalidade(self):
        return self.__modalidade

    @property    # Propriedade para saber a quantidade de acertos necessarios de cada modalidad
    def sorteio_len(self):
        return {
            'Quina': self.QUINA,
            'Megasena': self.MEGASENA,
            'Lotofacil': self.LOTOFACIL,
            'Lotomania': self.LOTOMANIA,
            'Duplasena': self.DUPLASENA,
            'Diadesorte': self.DIADESORTE,
        }.get(self.__modalidade, AssertionError('Modalidade não implementada.'))

    def sortear(self):
        methods = {
            'Quina': self.__quina,
            'Megasena': self.__megasena,
            'Lotofacil': self.__lotofacil,
            'Lotomania': self.__lotomania,
            'Duplasena': self.__duplasena,
            'Diadesorte': self.__diadesorte,
            'Timemania': self.__timemania
        }
        method = methods.get(self.__modalidade)
        if method:
            result = method()
            if self.__modalidade == 'Diadesorte':
                l_exib = list(result)
                l_exib.append(self.MESES[secrets.randbelow(len(self.MESES))])
                l_exib.sort(key=lambda item: str(item))
                return l_exib
            return result
        return AttributeError("Objeto não reconhecida como um jogo válido")

    def conferir(self, listadejogos) -> list:
        assert listadejogos is not None, f'É necessário informar um jogo para conferir'
        pontos = []
        if self.__modalidade == 'Duplasena':
            for jogo in listadejogos:
                pontos.append(self.__res_duplasena1.issubset(jogo))
                pontos.append(self.__res_duplasena2.issubset(jogo))
            return pontos

        for jogo in listadejogos:
            pontos.append(self.__sorteado.issubset(jogo))
        return pontos


if __name__ == '__main__':
    quit(3)
