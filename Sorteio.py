"""
Sorteia e retorna as dezenas de uma loteria especificada
"""
from Quina import Quina
from Megasena import Megasena
from Lotofacil import Lotofacil
from Lotomania import Lotomania
from Duplasena import Duplasena
from Diadesorte import Diadesorte
from random import randrange


class Sorteio:

    SENA = 6
    QUINA = 5
    LOTOFACIL = 15
    LOTOMANIA = 20
    DUPLASENA = 6
    DIADESORTE = 8
    MESES = ('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez')

    def __init__(self, modalidade):
        self.__modalidade = modalidade
        self.__resultado = set()
        self.__res_duplasena1 = set()
        self.__res_duplasena2 = set()

    def __megasena(self) -> set:
        self.__resultado.clear()
        while len(self.__resultado) < self.SENA:
            # resultado.add(secrets.choice(range(1, 61)))
            self.__resultado.add(randrange(1, 61, 1))
        return self.__resultado

    def __quina(self) -> set:
        self.__resultado.clear()
        while len(self.__resultado) < self.QUINA:
            self.__resultado.add(randrange(1, 81, 1))
        return self.__resultado

    def __lotofacil(self) -> set:
        self.__resultado.clear()
        while len(self.__resultado) < self.LOTOFACIL:
            self.__resultado.add(randrange(1, 26, 1))
        return self.__resultado

    def __diadesorte(self) -> set:
        self.__resultado.clear()
        while len(self.__resultado) < self.DIADESORTE:
            self.__resultado.add(randrange(1, 32, 1))
        self.__resultado.add(str(self.MESES)[randrange(0, 12, 1)])
        return self.__resultado

    def __lotomania(self) -> set:
        self.__resultado.clear()
        while len(self.__resultado) < self.LOTOMANIA:
            self.__resultado.add(randrange(1, 101, 1))
        return self.__resultado

    def __duplasena(self) -> set:
        """
        Executa o sorteio da Dupla sena (Dois sets de seis numeros)
        :return: Um set com a uniao dos dos sorteis, ignorando dezenas repetidas
        """
        self.__resultado.clear()
        self.__res_duplasena1.clear()
        self.__res_duplasena2.clear()
        while len(self.__res_duplasena1) < self.DUPLASENA:     # Primeiro sorteio
            self.__res_duplasena1.add(randrange(1, 51, 1))

        while len(self.__res_duplasena2) < self.DUPLASENA:     # Segundo sorteio
            self.__res_duplasena2.add(randrange(1, 51, 1))

        for i in self.__res_duplasena1:
            self.__resultado.add(i)           # Adiciona o primeiro sorteio ao set
        for j in self.__res_duplasena2:
            self.__resultado.add(j)          # Adiciona o segundo sorteio ao set(remove repetidos)
        return self.__resultado

    @property    # Propriedade para exibir os sorteios da Dupla sena de forma separada.
    def sorteio_duplasena(self):
        return [self.__res_duplasena1, self.__res_duplasena2]

    @property    # Propriedade para saber a quantidade de acertos necessarios de cada modalidad
    def sorteio_len(self):
        if isinstance(self.__modalidade, Quina):
            return self.QUINA
        elif isinstance(self.__modalidade, Megasena):
            return self.SENA
        elif isinstance(self.__modalidade, Lotofacil):
            return self.LOTOFACIL
        elif isinstance(self.__modalidade, Lotomania):
            return self.LOTOMANIA
        elif isinstance(self.__modalidade, Duplasena):
            return self.DUPLASENA
        elif isinstance(self.__modalidade, Diadesorte):
            return self.DIADESORTE
        return None

    def resultado(self):
        if isinstance(self.__modalidade, Quina):
            return self.__quina()
        elif isinstance(self.__modalidade, Megasena):
            return self.__megasena()
        elif isinstance(self.__modalidade, Lotofacil):
            return self.__lotofacil()
        elif isinstance(self.__modalidade, Lotomania):
            return self.__lotomania()
        elif isinstance(self.__modalidade, Duplasena):
            return self.__duplasena()
        elif isinstance(self.__modalidade, Diadesorte):
            return self.__diadesorte()
        return None

    def conferir(self, jogo: set) -> int:
        return len(jogo.intersection(self.__resultado))


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
