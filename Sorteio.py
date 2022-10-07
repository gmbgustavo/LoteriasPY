"""
Sorteia e retorna as dezenas de uma loteria especificada
"""
from Quina import Quina
from Megasena import Megasena
from Lotofacil import Lotofacil
from Lotomania import Lotomania
from Duplasena import Duplasena
from Diadesorte import Diadesorte
from Supersete import Supersete
from Milionaria import Milionaria
import secrets


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
    SUPERSETE = 7
    MILIONARIA = 6
    MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    MODALIDADES = ['Quina', 'Megasena', 'Lotofacil', 'Lotomania',
                   'Diadesorte', 'Duplasena', 'Supersete', 'Milionaria']

    def __init__(self, modalidade: str):
        assert modalidade in MODALIDADES, \
            f'Modalidade inválida: Válidas apenas {MODALIDADES}. Informado {modalidade}.'
        self.__modalidade = modalidade
        self.__sorteado = set()
        self.__res_duplasena1 = set()
        self.__res_duplasena2 = set()

    def __megasena(self) -> set:
        self.__sorteado.clear()
        numeros = [x for x in range(1, self.MAX_MEGASENA + 1)]
        while len(self.__sorteado) < self.MEGASENA:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
        return self.__sorteado

    def __quina(self) -> set:
        self.__sorteado.clear()
        count = self.MAX_QUINA
        numeros = [x for x in range(1, self.MAX_QUINA + 1)]
        while len(self.__sorteado) < self.QUINA:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
            count -= 1
        return self.__sorteado

    def __lotofacil(self) -> set:
        self.__sorteado.clear()
        numeros = [x for x in range(1, self.MAX_LOTOFACIL + 1)]
        while len(self.__sorteado) < self.LOTOFACIL:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
        return self.__sorteado

    def __diadesorte(self) -> set:
        self.__sorteado.clear()
        numeros = [x for x in range(1, self.MAX_DIADESORTE + 1)]
        while len(self.__sorteado) < self.DIADESORTE:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
        return set(self.__sorteado)

    def __lotomania(self) -> set:
        self.__sorteado.clear()
        numeros = [x for x in range(1, self.MAX_LOTOMANIA + 1)]
        while len(self.__sorteado) < self.LOTOMANIA:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
        return set(self.__sorteado)

    def __duplasena(self) -> set:
        """
        Executa o sorteio da Dupla sena (Dois sets de seis numeros)
        :return: Um set com a uniao dos dos sorteis, ignorando dezenas repetidas
        """
        self.__sorteado.clear()
        self.__res_duplasena1.clear()
        self.__res_duplasena2.clear()
        numeros = [x for x in range(1, self.MAX_DUPLASENA + 1)]
        while len(self.__res_duplasena1) < self.DUPLASENA:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))

        numeros = [x for x in range(1, self.MAX_DUPLASENA + 1)]
        while len(self.__res_duplasena2) < self.DUPLASENA:
            self.__sorteado.add(numeros.pop(secrets.randbelow(len(numeros))))
        for i in self.__res_duplasena1:
            self.__sorteado.add(i)           # Adiciona o primeiro sorteio ao set
        for j in self.__res_duplasena2:
            self.__sorteado.add(j)          # Adiciona o segundo sorteio ao set(remove repetidos)
        return self.__sorteado

    @property    # Propriedade para exibir os sorteios da Dupla sena de forma separada.
    def sorteio_duplasena(self):
        return [self.__res_duplasena1, self.__res_duplasena2]

    @property
    def modalidade(self):
        return self.__modalidade

    @property    # Propriedade para saber a quantidade de acertos necessarios de cada modalidad
    def sorteio_len(self):
        if self.__modalidade == 'Quina':
            return self.QUINA
        elif self.__modalidade == 'Megasena':
            return self.MEGASENA
        elif self.__modalidade == 'Lotofacil':
            return self.LOTOFACIL
        elif self.__modalidade == 'Lotomania':
            return self.LOTOMANIA
        elif self.__modalidade == 'Duplasena':
            return self.DUPLASENA
        elif self.__modalidade == 'Diadesorte':
            return self.DIADESORTE
        elif self.__modalidade == 'Supersete':
            return self.SUPERSETE
        elif self.__modalidade == 'Milionaria':
            return self.MILIONARIA
        else:
            return AssertionError('Modalidade não implementada.')

    def sortear(self):
        if self.__modalidade == 'Quina':
            return self.__quina()
        elif self.__modalidade == 'Megasena':
            return self.__megasena()
        elif self.__modalidade == 'Lotofacil':
            return self.__lotofacil()
        elif self.__modalidade == 'Lotomania':
            return self.__lotomania()
        elif self.__modalidade == 'Duplasena':
            return self.__duplasena()
        elif self.__modalidade == 'Diadesorte':
            l_exib = list(self.__diadesorte())
            l_exib.append(self.MESES[secrets.randbelow(len(self.MESES))])
            l_exib.sort(key=lambda item: str(item))
            return l_exib
        elif self.__modalidade == 'Supersete':
            return NotImplementedError('Ainda não fiz essa.')
        elif self.__modalidade == 'Milionaria'
            return NotImplementedError('Ainda não fiz essa.')
        return AttributeError('Objeto não reconhecida como um jogo válido')

    def conferir(self, *args) -> int:
        assert args is not None, f'É necessário informar um jogo para conferir'
        apostas = args
        for jogo in apostas:
            pontos = len(jogo.intersection(self.__sorteado))
        return pontos


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
