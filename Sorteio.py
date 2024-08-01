"""
Sorteia e retorna as dezenas de uma loteria especificada
"""

import random
import secrets

MODALIDADES = ['Quina', 'Megasena', 'Lotofacil', 'Lotomania', 'Timemania', 'Diadesorte', 'Supersete']


class Sorteio:
    MEGASENA = 6
    MAX_MEGASENA = 60
    QUINA = 5
    MAX_QUINA = 80
    LOTOFACIL = 15
    MAX_LOTOFACIL = 25
    LOTOMANIA = 20
    MAX_LOTOMANIA = 100
    DIADESORTE = 7
    MAX_DIADESORTE = 31
    MAX_TIMEMANIA = 80
    TIMEMANIA = 7
    SUPERSETE = 7
    SUPERSETE_RANGE = range(1, 8)
    MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

    def __init__(self, modalidade: str):
        assert modalidade in MODALIDADES, \
            f'Modalidade inválida: Válidas apenas {MODALIDADES}. Informado {modalidade}.'
        self.__modalidade = modalidade
        self.__sorteado = set()
        self.__res_supersete = {}
        self.__res_timemania = []
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
        return self.__sorteado

    def __supersete(self) -> dict:
        self.__res_supersete.clear()
        index = 1
        while len(self.__res_supersete) < self.SUPERSETE:
            self.__res_supersete[index] = secrets.randbelow(10)
            index += 1
        return self.__res_supersete

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
            'Diadesorte': self.DIADESORTE,
        }.get(self.__modalidade, AssertionError('Modalidade não implementada.'))

    def sortear(self):
        methods = {
            'Quina': self.__quina,
            'Megasena': self.__megasena,
            'Lotofacil': self.__lotofacil,
            'Lotomania': self.__lotomania,
            'Diadesorte': self.__diadesorte,
            'Timemania': self.__timemania,
            'Supersete': self.__supersete
        }
        method = methods.get(self.__modalidade)
        if method:
            result = method()
            if self.__modalidade == 'Diadesorte':
                l_exib = list(result)
                l_exib.append(self.MESES[secrets.randbelow(len(self.MESES))])
                l_exib.sort(key=lambda item: str(item))
                return l_exib
            if self.__modalidade == 'Supersete':
                return result
            return result
        return AttributeError("Objeto não reconhecido como um jogo válido")

    def conferir(self, listadejogos) -> list:
        assert listadejogos is not None, f'É necessário informar um jogo para conferir'
        pontos = []
        for jogo in listadejogos:
            if self.__modalidade == 'Lotomania' and len(self.__sorteado.difference(jogo)) == 20:
                pontos.append(True)
            elif self.__modalidade == 'Supersete':
                acertos = 0
                for x in self.SUPERSETE_RANGE:
                    if self.__res_supersete[x] != jogo[x]:
                        break
                    else:
                        acertos += 1
                if acertos == self.SUPERSETE:
                    pontos.append(True)
            else:
                pontos.append(self.__sorteado.issubset(jogo))
        return pontos


if __name__ == '__main__':
    quit(3)
