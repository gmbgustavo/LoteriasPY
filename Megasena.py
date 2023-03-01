"""
Classe da Mega-Sena
"""
import secrets
import time

MAX_BET = 15
MIN_BET = 6
MIN_NUM = 1
MAX_NUM = 60
RANGEBET = range(MIN_NUM, MAX_NUM + 1)


class Megasena:

    def __init__(self, *args, dezenas):
        """
        Cria um objeto do tipo Megasena.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas(padrao=6)
        :param dezenas: Quantidade de dezenas da aposta (6-15)
        """
        assert len(args) <= MAX_BET, f'Esperado no máximo {MAX_BET} dezenas. (Passadas {len(args)})'
        assert MIN_BET <= dezenas <= MAX_BET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MIN_BET} e {MAX_BET}. (Foi informado {dezenas})'
        assert len(args) <= dezenas, f'Quantidade de números informados incompativel com o argumento "dezenas"'
        assert self.__checkargs(args), f'Megasena usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        self.__gira_globo = secrets.SystemRandom()
        self.__dezenas = dezenas
        self.__jogo = self.__surpresinha(set(args))

    def __repr__(self):
        l_exib = list(self.__jogo)
        l_exib.sort()
        return str(l_exib)

    def __iter__(self):
        yield set(self.__jogo)

    def __len__(self):
        return self.__dezenas

    @staticmethod
    def __checkargs(numeros):
        if len(numeros) == 0:
            return True
        else:
            for i in numeros:
                if i not in RANGEBET:
                    return False
            return True

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 60
        :return: set
        """
        retorno = set(fixos)
        numeros = [x for x in RANGEBET if x not in retorno]    # Generator desconsidera fixos
        while len(retorno) < self.__dezenas:
            self.__gira_globo.shuffle(numeros)
            time.sleep(0.3)
            retorno.add(numeros.pop(secrets.randbelow(len(numeros))))
            time.sleep(0.2)    # Aumenta a aleatoriedade
        return set(retorno)

    def sorteio(self):
        return self.__surpresinha()

    @property
    def jogo(self):
        return set(self.__jogo)


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
