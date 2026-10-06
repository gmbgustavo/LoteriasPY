# Funções para uso comum: leitura dos históricos oficiais das loterias da Caixa
# (pasta dados/) e conferência de apostas contra os resultados reais.
#
# As 11 modalidades com histórico em CSV estão registradas em MODALIDADES:
#   Megasena, Quina, Lotofacil, Lotomania, Timemania, Duplasena, Diadesorte,
#   Supersete, Maismilionaria, Loteca e Loteriafederal.
#
# Uso típico:
#   >>> from API.helpers import confere_aposta, normaliza_aposta
#   >>> aposta = normaliza_aposta('Megasena', [1, 5, 6, 15, 22, 28])
#   >>> relatorio = confere_aposta('Megasena', aposta)
#   >>> relatorio['premiado'], relatorio['melhor']

import csv
from pathlib import Path

DADOS = Path(__file__).resolve().parent / '../dados'

MEGASENA = DADOS / 'megasena.csv'
QUINA = DADOS / 'quina.csv'
LOTOFACIL = DADOS / 'lotofacil.csv'
DIADESORTE = DADOS / 'diadesorte.csv'
LOTOMANIA = DADOS / 'lotomania.csv'
TIMEMANIA = DADOS / 'timemania.csv'
DUPLASENA = DADOS / 'duplasena.csv'
SUPERSETE = DADOS / 'supersete.csv'
MAISMILIONARIA = DADOS / 'maismilionaria.csv'
LOTECA = DADOS / 'loteca.csv'
LOTERIAFEDERAL = DADOS / 'loteriafederal.csv'

# As colunas do CSV da Loteca guardam o texto oficial; internamente usamos 1/M/2
LOTECA_COLUNAS = {'Coluna 1': '1', 'Coluna do meio': 'M', 'Coluna 2': '2'}
LOTECA_TEXTO = {valor: chave for chave, valor in LOTECA_COLUNAS.items()}

# ---------------------------------------------------------------------------
# Registro das modalidades
# ---------------------------------------------------------------------------
#   arquivo        -> CSV do histórico em dados/
#   tipo           -> 'dezenas' (conjunto), 'colunas' (posição a posição)
#                     ou 'bilhete' (Loteria Federal)
#   aposta         -> quantidade padrão de dezenas/colunas de uma aposta simples
#   faixa          -> intervalo permitido para cada dezena/coluna
#   colunas        -> colunas do CSV com o resultado sorteado
#   premio         -> acertos necessários para o prêmio principal
#   faixas         -> acertos premiados -> nome da faixa
#   dois_sorteios  -> Dupla Sena: duas extrações de 6 dezenas no mesmo concurso
#   trevos         -> +Milionária: colunas do CSV com os 2 trevos
#   descricao      -> texto exibido nos menus

MODALIDADES = {
    'Megasena': dict(
        arquivo=MEGASENA, tipo='dezenas', aposta=6, faixa=(1, 60),
        colunas=(2, 8), premio=6,
        faixas={6: 'Sena', 5: 'Quina', 4: 'Quadra'},
        descricao='6 dezenas de 1 a 60, 6 sorteadas',
    ),
    'Quina': dict(
        arquivo=QUINA, tipo='dezenas', aposta=5, faixa=(1, 80),
        colunas=(2, 7), premio=5,
        faixas={5: 'Quina', 4: 'Quadra', 3: 'Terno', 2: 'Duque'},
        descricao='5 dezenas de 1 a 80, 5 sorteadas',
    ),
    'Lotofacil': dict(
        arquivo=LOTOFACIL, tipo='dezenas', aposta=15, faixa=(1, 25),
        colunas=(2, 17), premio=15,
        faixas={15: '15 acertos', 14: '14 acertos', 13: '13 acertos',
                12: '12 acertos', 11: '11 acertos'},
        descricao='15 dezenas de 1 a 25, 15 sorteadas',
    ),
    'Lotomania': dict(
        arquivo=LOTOMANIA, tipo='dezenas', aposta=50, faixa=(0, 99),
        colunas=(2, 22), premio=20,
        faixas={20: '20 acertos', 19: '19 acertos', 18: '18 acertos',
                17: '17 acertos', 16: '16 acertos', 15: '15 acertos',
                0: 'nenhum acerto'},
        descricao='50 dezenas de 00 a 99, 20 sorteadas',
    ),
    'Timemania': dict(
        arquivo=TIMEMANIA, tipo='dezenas', aposta=10, faixa=(1, 80),
        colunas=(2, 9), premio=7,
        faixas={7: '7 acertos', 6: '6 acertos', 5: '5 acertos',
                4: '4 acertos', 3: '3 acertos'},
        descricao='10 dezenas de 1 a 80, 7 sorteadas',
    ),
    'Duplasena': dict(
        arquivo=DUPLASENA, tipo='dezenas', aposta=6, faixa=(1, 50),
        colunas=(2, 14), premio=6, dois_sorteios=2,
        faixas={6: 'Sena', 5: 'Quina', 4: 'Quadra', 3: 'Terno'},
        descricao='6 dezenas de 1 a 50, dois sorteios de 6 por concurso',
    ),
    'Diadesorte': dict(
        arquivo=DIADESORTE, tipo='dezenas', aposta=7, faixa=(1, 31),
        colunas=(2, 9), premio=7,
        faixas={7: '7 acertos', 6: '6 acertos', 5: '5 acertos', 4: '4 acertos'},
        descricao='7 dezenas de 1 a 31, 7 sorteadas',
    ),
    'Supersete': dict(
        arquivo=SUPERSETE, tipo='colunas', aposta=7, faixa=(0, 9),
        colunas=(2, 9), premio=7, permite_repetir=True,
        faixas={7: '7 colunas', 6: '6 colunas', 5: '5 colunas',
                4: '4 colunas', 3: '3 colunas'},
        descricao='7 colunas de 0 a 9 (pode repetir)',
    ),
    'Maismilionaria': dict(
        arquivo=MAISMILIONARIA, tipo='dezenas', aposta=6, faixa=(1, 50),
        colunas=(2, 10), premio=6, trevos=2, trevos_faixa=(1, 6),
        faixas={6: '6 acertos', 5: '5 acertos', 4: '4 acertos',
                3: '3 acertos', 2: '2 acertos'},
        descricao='6 dezenas de 1 a 50 + 2 trevos de 1 a 6',
    ),
    'Loteca': dict(
        arquivo=LOTECA, tipo='colunas', aposta=14, faixa=None,
        valores=('1', 'M', '2'), colunas=(2, 16), premio=14,
        faixas={14: '14 acertos', 13: '13 acertos'},
        descricao='14 jogos, cada um em Coluna 1 / Coluna do meio / Coluna 2',
    ),
    'Loteriafederal': dict(
        arquivo=LOTERIAFEDERAL, tipo='bilhete', aposta=1, faixa=None,
        colunas=(2, 7), premio=1, rotulo_premio='Prêmio', unidade='prêmio',
        faixas={5: '5 prêmios', 4: '4 prêmios', 3: '3 prêmios',
                2: '2 prêmios', 1: '1 prêmio'},
        descricao='bilhete de 6 dígitos conferido nos 5 prêmios',
    ),
}

# apelidos aceitos ao escolher a modalidade pelo nome
APELIDOS = {
    'mega': 'Megasena', 'mega-sena': 'Megasena', 'megasena': 'Megasena',
    'quina': 'Quina',
    'lotofacil': 'Lotofacil', 'loto facil': 'Lotofacil', 'loto': 'Lotofacil',
    'lotomania': 'Lotomania',
    'timemania': 'Timemania', 'time': 'Timemania',
    'duplasena': 'Duplasena', 'dupla sena': 'Duplasena', 'dupla': 'Duplasena',
    'diadesorte': 'Diadesorte', 'dia de sorte': 'Diadesorte',
    'supersete': 'Supersete', 'super sete': 'Supersete',
    'maismilionaria': 'Maismilionaria', '+milionaria': 'Maismilionaria',
    'milionaria': 'Maismilionaria',
    'loteca': 'Loteca',
    'loteriafederal': 'Loteriafederal', 'federal': 'Loteriafederal',
}


def modalidade_valida(nome: str) -> str:
    """Devolve o nome canônico da modalidade a partir do nome ou apelido."""
    if nome in MODALIDADES:
        return nome
    chave = str(nome).strip().lower()
    if chave in APELIDOS:
        return APELIDOS[chave]
    raise ValueError(f'Modalidade inválida: {nome!r}. Válidas: {", ".join(MODALIDADES)}.')


# ---------------------------------------------------------------------------
# Leitura dos históricos
# ---------------------------------------------------------------------------
def read_csv_lines(arquivo_csv):
    assert arquivo_csv is not None, 'Arquivo não encontrado'
    with open(arquivo_csv, encoding='utf-8-sig') as m:
        reader = csv.reader(m)
        for linha in reader:
            yield linha


def ler_historico(modalidade: str):
    """Gera (concurso, data, resultado) do mais recente para o mais antigo.

    `resultado` é a lista de campos do sorteio (dezenas, colunas ou prêmios).
    """
    nome = modalidade_valida(modalidade)
    cfg = MODALIDADES[nome]
    inicio, fim = cfg['colunas']
    for linha in read_csv_lines(cfg['arquivo']):
        if not linha or not linha[0].strip().isdigit():
            continue    # cabeçalho e eventuais linhas vazias
        yield int(linha[0]), linha[1], linha[inicio:fim]


def total_concursos(modalidade: str) -> int:
    return sum(1 for _ in ler_historico(modalidade))


# ---------------------------------------------------------------------------
# Validação / normalização da aposta informada pelo usuário
# ---------------------------------------------------------------------------
def _valida_inteiros(valores, quantidade, faixa, rotulo, permite_repetir=False):
    try:
        numeros = [int(str(v).strip()) for v in valores]
    except (TypeError, ValueError):
        raise ValueError(f'{rotulo}: informe apenas números inteiros.')
    if quantidade is not None and len(numeros) != quantidade:
        raise ValueError(f'{rotulo}: são necessários exatamente {quantidade} números '
                         f'(informados {len(numeros)}).')
    if faixa:
        minimo, maximo = faixa
        fora = [n for n in numeros if n < minimo or n > maximo]
        if fora:
            raise ValueError(f'{rotulo}: {fora} fora da faixa permitida ({minimo} a {maximo}).')
    if not permite_repetir and len(set(numeros)) != len(numeros):
        raise ValueError(f'{rotulo}: não pode repetir números.')
    return numeros


def normaliza_aposta(modalidade: str, valores):
    """Valida a aposta do usuário e devolve a representação interna usada na
    conferência. Levanta ValueError com a explicação quando algo está errado."""
    nome = modalidade_valida(modalidade)
    cfg = MODALIDADES[nome]
    tipo = cfg['tipo']

    if tipo == 'bilhete':
        bruto = str(valores[0] if isinstance(valores, (list, tuple)) else valores).strip()
        digitos = ''.join(c for c in bruto if c.isdigit())
        if len(digitos) != 6:
            raise ValueError('Loteria Federal: informe o bilhete com 6 dígitos (ex.: 005349).')
        return digitos.zfill(6)

    if tipo == 'colunas':
        if nome == 'Loteca':
            colunas = []
            for valor in valores:
                chave = str(valor).strip().upper()
                if chave in ('1', 'C1', 'COLUNA 1'):
                    colunas.append('1')
                elif chave in ('2', 'C2', 'COLUNA 2'):
                    colunas.append('2')
                elif chave in ('M', 'MEIO', 'X', '0', 'COLUNA DO MEIO'):
                    colunas.append('M')
                else:
                    raise ValueError(f"Loteca: valor inválido {valor!r}. "
                                     "Use 1 (Coluna 1), 2 (Coluna 2) ou M (Coluna do meio).")
            if len(colunas) != cfg['aposta']:
                raise ValueError(f"Loteca: são necessárias {cfg['aposta']} colunas "
                                 f"(informadas {len(colunas)}).")
            return tuple(colunas)
        return tuple(_valida_inteiros(valores, cfg['aposta'], cfg['faixa'], nome,
                                      cfg.get('permite_repetir', False)))

    # tipo 'dezenas'
    if cfg.get('trevos'):
        total = cfg['aposta'] + cfg['trevos']
        if len(valores) != total:
            raise ValueError(f'{nome}: informe {cfg["aposta"]} dezenas e '
                             f'{cfg["trevos"]} trevos ({total} números no total).')
        dezenas = _valida_inteiros(list(valores)[:cfg['aposta']], cfg['aposta'],
                                   cfg['faixa'], 'Dezenas')
        trevos = _valida_inteiros(list(valores)[cfg['aposta']:], cfg['trevos'],
                                  cfg['trevos_faixa'], 'Trevos')
        return frozenset(dezenas), frozenset(trevos)
    return frozenset(_valida_inteiros(valores, cfg['aposta'], cfg['faixa'], nome))


def normaliza_aposta_milionaria(dezenas, trevos):
    """Caso especial do +Milionária: 6 dezenas (1-50) + 2 trevos (1-6)."""
    return normaliza_aposta('Maismilionaria', list(dezenas) + list(trevos))


def descreve_aposta(modalidade: str, aposta) -> str:
    """Texto legível da aposta normalizada."""
    nome = modalidade_valida(modalidade)
    cfg = MODALIDADES[nome]
    if cfg['tipo'] == 'bilhete':
        return f'bilhete {aposta}'
    if nome == 'Loteca':
        return ' | '.join(LOTECA_TEXTO[c] for c in aposta)
    if nome == 'Maismilionaria' and isinstance(aposta, tuple):
        dezenas, trevos = aposta
        return (f'{", ".join(f"{n:02d}" for n in sorted(dezenas))} '
                f'+ trevos {", ".join(str(t) for t in sorted(trevos))}')
    if cfg['tipo'] == 'colunas':
        return '-'.join(str(c) for c in aposta)
    return ', '.join(f'{n:02d}' for n in sorted(aposta))


# ---------------------------------------------------------------------------
# Conferência
# ---------------------------------------------------------------------------
def conta_acertos(modalidade: str, aposta, resultado) -> tuple:
    """Devolve (acertos, detalhe) de uma aposta contra um resultado do histórico."""
    nome = modalidade_valida(modalidade)
    cfg = MODALIDADES[nome]
    tipo = cfg['tipo']

    if tipo == 'bilhete':
        premios = [str(p).zfill(6) for p in resultado]
        return sum(1 for p in premios if p == aposta), None

    if tipo == 'colunas':
        if nome == 'Loteca':
            sorteado = [LOTECA_COLUNAS.get(str(v).strip(), str(v).strip()) for v in resultado]
        else:
            sorteado = [str(int(v)) for v in resultado]
        return sum(1 for meu, sorte in zip(aposta, sorteado) if str(meu) == sorte), None

    numeros = [int(v) for v in resultado]
    if cfg.get('dois_sorteios'):
        meio = len(numeros) // 2
        primeiro = len(set(numeros[:meio]).intersection(aposta))
        segundo = len(set(numeros[meio:]).intersection(aposta))
        return max(primeiro, segundo), None

    if cfg.get('trevos') and isinstance(aposta, tuple):
        dezenas, meus_trevos = aposta
        acertos = len(set(numeros[:cfg['aposta']]).intersection(dezenas))
        sorteio_trevos = set(numeros[cfg['aposta']:])
        return acertos, f'{len(meus_trevos.intersection(sorteio_trevos))} trevo(s)'

    return len(set(numeros).intersection(aposta)), None


def confere_aposta(modalidade: str, aposta, exemplos: int = 5) -> dict:
    """Confere uma aposta contra TODO o histórico oficial da modalidade.

    :return: dicionário com o resumo da conferência:
        concursos    -> quantos concursos foram conferidos
        melhor       -> maior número de acertos encontrado
        melhores     -> [(concurso, data, acertos, detalhe)] com os melhores
                        resultados, do mais recente para o mais antigo
        total_melhor -> quantos concursos alcançaram o melhor resultado
        premiado     -> True se a aposta alguma vez acertou o prêmio principal
        premiacoes   -> [(concurso, data, acertos)] dos concursos premiados
        contagem     -> {acertos: quantos concursos}
    """
    nome = modalidade_valida(modalidade)
    cfg = MODALIDADES[nome]

    relatorio = dict(modalidade=nome, aposta=descreve_aposta(nome, aposta),
                     concursos=0, melhor=-1, melhores=[], total_melhor=0,
                     premiado=False, premiacoes=[], contagem={},
                     faixas=dict(cfg['faixas']))
    # no +Milionária o prêmio principal exige 6 acertos E os 2 trevos
    exige_trevos = nome == 'Maismilionaria'

    for concurso, data, resultado in ler_historico(nome):
        acertos, detalhe = conta_acertos(nome, aposta, resultado)
        relatorio['concursos'] += 1
        relatorio['contagem'][acertos] = relatorio['contagem'].get(acertos, 0) + 1

        if acertos > relatorio['melhor']:
            relatorio['melhor'] = acertos
            relatorio['melhores'] = [(concurso, data, acertos, detalhe)]
            relatorio['total_melhor'] = 1
        elif acertos == relatorio['melhor']:
            relatorio['total_melhor'] += 1
            if len(relatorio['melhores']) < exemplos:
                relatorio['melhores'].append((concurso, data, acertos, detalhe))

        ganhou = acertos >= cfg['premio']
        if exige_trevos:
            ganhou = ganhou and detalhe == f"{cfg['trevos']} trevo(s)"
        if ganhou:
            relatorio['premiado'] = True
            if len(relatorio['premiacoes']) < exemplos:
                relatorio['premiacoes'].append((concurso, data, acertos))

    return relatorio


def plural_acertos(quantidade: int) -> str:
    """'1 acerto' / '2 acertos'."""
    return 'acerto' if quantidade == 1 else 'acertos'


def relatorio_texto(relatorio: dict) -> list:
    """Formata o relatório da conferência em linhas prontas para impressão."""
    cfg = MODALIDADES[relatorio['modalidade']]
    linhas = [
        f"Aposta conferida: {relatorio['aposta']}",
        f"Modalidade: {relatorio['modalidade']}  |  concursos conferidos: {relatorio['concursos']:,}",
    ]
    rotulo = cfg.get('rotulo_premio', 'Prêmio principal')
    if relatorio['premiado']:
        linhas.append(f'{rotulo.upper()}: sim, esta aposta já foi ganhadora!')
        for concurso, data, acertos in relatorio['premiacoes']:
            linhas.append(f'   concurso {concurso} ({data}) — '
                          f"{acertos} {plural_acertos(acertos)}")
    else:
        linhas.append(f"{rotulo} ({cfg['premio']} {cfg.get('unidade', 'acertos')}): "
                      f"nunca ocorreu nesta aposta.")

    melhor = relatorio['melhor']
    linhas.append(f"Melhor resultado: {melhor} {plural_acertos(melhor)}, "
                  f"em {relatorio['total_melhor']} concurso(s).")
    for concurso, data, acertos, detalhe in relatorio['melhores']:
        extra = f' ({detalhe})' if detalhe else ''
        linhas.append(f'   concurso {concurso} ({data}) — '
                      f"{acertos} {plural_acertos(acertos)}{extra}")

    faixas = cfg['faixas']
    premiadas = {a: n for a, n in sorted(relatorio['contagem'].items(), reverse=True) if a in faixas}
    if premiadas:
        linhas.append('Faixas premiadas alcançadas:')
        for acertos, quantidade in premiadas.items():
            linhas.append(f'   {faixas[acertos]:<12} {quantidade:>6} concurso(s)')
    else:
        linhas.append('Nenhuma faixa premiada foi alcançada.')
    return linhas


def imprime_conferencia(modalidade: str, aposta) -> dict:
    """Confere e imprime o resultado. Devolve o relatório."""
    relatorio = confere_aposta(modalidade, aposta)
    for linha in relatorio_texto(relatorio):
        print(linha)
    return relatorio


def frase_resultado(relatorio: dict) -> str:
    """Frase curta com o veredito da conferência."""
    cfg = MODALIDADES[relatorio['modalidade']]
    if relatorio['premiado']:
        return 'Parabéns: essa aposta já teria sido premiada!'
    if relatorio['modalidade'] == 'Loteriafederal':
        return 'Esse bilhete nunca apareceu entre os prêmios sorteados.'
    return (f"Essa aposta nunca acertou o prêmio principal "
            f"({cfg['premio']} acertos).")


# ---------------------------------------------------------------------------
# Compatibilidade com as funções antigas (uma por modalidade)
# ---------------------------------------------------------------------------
def confere_mega_hist(aposta):
    return imprime_conferencia('Megasena', frozenset(aposta))


def confere_quina_hist(aposta):
    return imprime_conferencia('Quina', frozenset(aposta))


def confere_lotofacil_hist(aposta):
    return imprime_conferencia('Lotofacil', frozenset(aposta))


def confere_diadesorte_hist(aposta):
    return imprime_conferencia('Diadesorte', frozenset(aposta))


def confere_lotomania_hist(aposta):
    return imprime_conferencia('Lotomania', frozenset(aposta))


def confere_timemania_hist(aposta):
    return imprime_conferencia('Timemania', frozenset(aposta))


def confere_duplasena_hist(aposta):
    return imprime_conferencia('Duplasena', frozenset(aposta))


def confere_supersete_hist(aposta):
    return imprime_conferencia('Supersete', tuple(aposta))


def confere_maismilionaria_hist(dezenas, trevos):
    return imprime_conferencia('Maismilionaria',
                               normaliza_aposta_milionaria(dezenas, trevos))


def confere_loteca_hist(aposta):
    return imprime_conferencia('Loteca', normaliza_aposta('Loteca', aposta))


def confere_loteriafederal_hist(bilhete):
    return imprime_conferencia('Loteriafederal', bilhete)


if __name__ == '__main__':
    confere_mega_hist(aposta={1, 5, 6, 15, 22, 28})
    quit(3)
