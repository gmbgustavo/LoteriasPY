"""
Classe da Lotofacil
"""

import secrets

MAX_BET = 20
MIN_BET = 15
MIN_NUM = 1
MAX_NUM = 25
RANGEBET = range(MIN_NUM, MAX_NUM + 1)


class Lotofacil:

    def __init__(self, *args, dezenas):
        f"""
        Cria um objeto do tipo Lotofacil.
        :param args: Se vazio, cria um jogo surpresinha com a quantidade de dezenas padrao ({MIN_BET})
        :param dezenas: quantidade de dezenas a serem preenchidas
        """
        assert len(args) <= MAX_BET, f'Esperado no máximo {MAX_BET} dezenas. (Passadas {len(args)})'
        assert MIN_BET <= dezenas <= MAX_BET and isinstance(dezenas, int), \
            f'Parametro dezenas deve ser inteiro entre {MIN_BET} e {MAX_BET}. (Passadas {dezenas})'
        assert self.__checkargs(args), f'Lotofácil usa números inteiros entre 0{MIN_NUM} e {MAX_NUM}'
        assert len(args) <= dezenas, f'Quantidade de números informados incompativel com o argumento "dezenas"'
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

    def __surpresinha(self, fixos=()):
        """
        Retorna um conjunto(set) com numeros inteiros entre 1 e 25
        :return: set
        """
        retorno = set(fixos)
        numeros = [x for x in range(1, len(RANGEBET) + 1) if x not in retorno]    # Generator desconsidera os fixos
        count = len(numeros)
        while len(retorno) < self.__dezenas:
            retorno.add(numeros.pop(secrets.choice(range(0, count))))
            count -= 1
        return set(retorno)

    @property
    def jogo(self):
        return set(self.__jogo)

    @staticmethod
    def __checkargs(numeros):
        if len(numeros) == 0:
            return True
        else:
            for i in numeros:
                if i not in RANGEBET:
                    return False
            return True


if __name__ == '__main__':
    print('Essa classe deve ser apenas instanciada internamente.')
