"""
Sorteia e retorna as dezenas de uma loteria especificada
"""
from Quina import Quina
from Megasena import Megasena
from Lotofacil import Lotofacil
from Lotomania import Lotomania
from Duplasena import Duplasena
from Diadesorte import Diadesorte
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
    MESES = ('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez')

    def __init__(self, modalidade):
        self.__modalidade = modalidade
        self.__sorteado = set()
        self.__res_duplasena1 = set()
        self.__res_duplasena2 = set()

    def __megasena(self) -> set:
        self.__sorteado.clear()
        count = self.MAX_MEGASENA
        numeros = [x for x in range(1, count + 1)]
        while len(self.__sorteado) < self.MEGASENA:
            self.__sorteado.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
        return self.__sorteado

    def __quina(self) -> set:
        self.__sorteado.clear()
        count = self.MAX_QUINA
        numeros = [x for x in range(1, count + 1)]
        while len(self.__sorteado) < self.QUINA:
            self.__sorteado.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
        return self.__sorteado

    def __lotofacil(self) -> set:
        count = self.MAX_LOTOFACIL
        self.__sorteado.clear()
        numeros = [x for x in range(1, count + 1)]
        while len(self.__sorteado) < self.LOTOFACIL:
            self.__sorteado.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
        return self.__sorteado

    def __diadesorte(self) -> set:
        count = self.MAX_DIADESORTE
        self.__sorteado.clear()
        numeros = [x for x in range(1, count + 1)]
        while len(self.__sorteado) < self.DIADESORTE:
            self.__sorteado.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
        self.__sorteado.add(self.MESES[secrets.choice(range(0, len(self.MESES)))])
        return set(self.__sorteado)

    def __lotomania(self) -> set:
        count = self.MAX_LOTOMANIA
        self.__sorteado.clear()
        numeros = [x for x in range(1, count + 1)]
        while len(self.__sorteado) < self.LOTOMANIA:
            self.__sorteado.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
        return set(self.__sorteado)

    def __duplasena(self) -> set:
        """
        Executa o sorteio da Dupla sena (Dois sets de seis numeros)
        :return: Um set com a uniao dos dos sorteis, ignorando dezenas repetidas
        """
        self.__sorteado.clear()
        self.__res_duplasena1.clear()
        self.__res_duplasena2.clear()
        count = self.MAX_DUPLASENA
        numeros = [x for x in range(1, count + 1)]
        while len(self.__res_duplasena1) < self.DUPLASENA:
            self.__res_duplasena1.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1

        count = self.MAX_DUPLASENA
        numeros = [x for x in range(1, count + 1)]
        while len(self.__res_duplasena2) < self.DUPLASENA:
            self.__res_duplasena2.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
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
        if isinstance(self.__modalidade, Quina):
            return self.QUINA
        elif isinstance(self.__modalidade, Megasena):
            return self.MEGASENA
        elif isinstance(self.__modalidade, Lotofacil):
            return self.LOTOFACIL
        elif isinstance(self.__modalidade, Lotomania):
            return self.LOTOMANIA
        elif isinstance(self.__modalidade, Duplasena):
            return self.DUPLASENA
        elif isinstance(self.__modalidade, Diadesorte):
            return self.DIADESORTE + 1    # Inclui o mes
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
            l_exib = list(self.__diadesorte())
            l_exib.sort(key=lambda item: str(item))
            return l_exib
        return None

    def conferir(self, jogo: set) -> int:
        a = len(jogo.intersection(self.__sorteado))
        return a


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
