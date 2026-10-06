#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atualizar_historico.py
======================

Complementa os arquivos CSV de histórico de sorteios das loterias da Caixa
(pasta ``dados/``) com todos os concursos publicados até a data de execução,
preservando o formato de colunas já existente em cada arquivo.

Fontes (todas oficiais, Caixa Econômica Federal)
------------------------------------------------
1. Planilhas de histórico completo (XLSX), uma por modalidade::

       https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados/download?modalidade=<NOME>

   Esse endpoint é servido por vários nós e nem todos possuem o arquivo, por
   isso a resposta alterna entre ``200`` (XLSX) e ``404`` ("documento não
   encontrado"). O script insiste até obter a planilha válida.

2. API de resultados, concurso a concurso::

       https://servicebus2.caixa.gov.br/portaldeloterias/api/<modalidade>/<concurso>

   Usada para o trecho que ainda não entrou na planilha (a planilha é
   publicada com defasagem) e para preencher eventuais lacunas.

Modalidades cobertas (11): Mega-Sena, Quina, Lotofácil, Lotomania, Timemania,
Dupla Sena, Dia de Sorte, Super Sete, +Milionária, Loteca e Loteria Federal.

Uso
---
    python3 atualizar_historico.py                 # atualiza os CSVs de dados/
    python3 atualizar_historico.py --so-verificar  # não grava nada, só confere
    python3 atualizar_historico.py --modalidade megasena --modalidade quina
    python3 atualizar_historico.py --sem-bulk      # ignora o XLSX (só API, lento)

Os arquivos originais são copiados para ``.cache/backup/<data-hora>/`` antes de
qualquer gravação.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
import time
import zipfile
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

RAIZ = Path(__file__).resolve().parent
DADOS = RAIZ / "dados"
CACHE = RAIZ / ".cache"
DIR_BULK = CACHE / "oficial_bulk"
DIR_API = CACHE / "api_cache"
DIR_BACKUP = CACHE / "backup"

BASE_API = "https://servicebus2.caixa.gov.br/portaldeloterias/api"
URL_DOWNLOAD = BASE_API + "/resultados/download"
CABECALHO_HTTP = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "application/json,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
}

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

# ---------------------------------------------------------------------------
# Configuração das modalidades
# ---------------------------------------------------------------------------
# chave            -> nome usado internamente / nome do arquivo
#   arquivo        -> CSV em dados/
#   api            -> slug na API de resultados
#   xlsx           -> nome do parâmetro `modalidade` no download da planilha
#   cabecalho      -> cabeçalho usado apenas quando o CSV ainda não existe
#   bom            -> grava com BOM UTF-8 (como o megasena.csv original)
#   xlsx_bolas     -> colunas (1-based) da planilha com as dezenas/colunas
#   xlsx_extra     -> colunas extras da planilha (ex.: ganhadores, time)
#   ganhadores     -> coluna do CSV (0-based) que recebe os ganhadores da 1ª faixa
#   zero_preenche  -> largura mínima dos números (Loteria Federal = 6 dígitos)

MODALIDADES: dict[str, dict] = {
    "megasena": dict(
        arquivo="megasena.csv",
        api="megasena",
        xlsx="MEGA_SENA",
        cabecalho=["Conc", "Data", "B1", "B2", "B3", "B4", "B5", "B6", "Gan", "Apostas"],
        bom=True,
        xlsx_bolas=range(3, 9),
        xlsx_extra={"gan": 9},
    ),
    "quina": dict(
        arquivo="quina.csv",
        api="quina",
        xlsx="QUINA",
        cabecalho=["Concurso", "Data"] + [f"b{i}" for i in range(1, 6)],
        bom=False,
        xlsx_bolas=range(3, 8),
    ),
    "lotofacil": dict(
        arquivo="lotofacil.csv",
        api="lotofacil",
        xlsx="LOTOFACIL",
        cabecalho=["Concurso", "Data"] + [f"bola {i}" for i in range(1, 16)],
        bom=False,
        xlsx_bolas=range(3, 18),
    ),
    "diadesorte": dict(
        arquivo="diadesorte.csv",
        api="diadesorte",
        xlsx="DIA_DE_SORTE",
        cabecalho=["Concurso", "Data"] + [f"bola {i}" for i in range(1, 8)],
        bom=False,
        xlsx_bolas=range(3, 10),
    ),
    "lotomania": dict(
        arquivo="lotomania.csv",
        api="lotomania",
        xlsx="LOTOMANIA",
        cabecalho=["Concurso", "Data"] + [f"bola {i}" for i in range(1, 21)],
        bom=False,
        xlsx_bolas=range(3, 23),
    ),
    "timemania": dict(
        arquivo="timemania.csv",
        api="timemania",
        xlsx="TIMEMANIA",
        cabecalho=["Concurso", "Data"] + [f"bola {i}" for i in range(1, 8)] + ["Time Coracao"],
        bom=False,
        xlsx_bolas=range(3, 10),
        xlsx_extra={"time": 10},
        # a planilha trunca o nome do time em concursos antigos ('NACIONALNTINO');
        # a API traz o campo completo, então ela é preferida para esta modalidade
        api_tudo=True,
    ),
    "duplasena": dict(
        arquivo="duplasena.csv",
        api="duplasena",
        xlsx="DUPLA_SENA",
        cabecalho=["Concurso", "Data"] + [f"bola {i}" for i in range(1, 13)],
        bom=False,
        xlsx_bolas=list(range(3, 9)) + list(range(18, 24)),
    ),
    "supersete": dict(
        arquivo="supersete.csv",
        api="supersete",
        xlsx="SUPER_SETE",
        cabecalho=["Concurso", "Data"] + [f"coluna {i}" for i in range(1, 8)],
        bom=False,
        xlsx_bolas=range(3, 10),
    ),
    "maismilionaria": dict(
        arquivo="maismilionaria.csv",
        api="maismilionaria",
        xlsx="MAIS_MILIONARIA",
        cabecalho=["Concurso", "Data"] + [f"bola {i}" for i in range(1, 7)] + ["trevo 1", "trevo 2"],
        bom=False,
        xlsx_bolas=range(3, 9),
        xlsx_extra={"trevos": (9, 10)},
    ),
    "loteca": dict(
        arquivo="loteca.csv",
        api="loteca",
        xlsx="LOTECA",
        cabecalho=["Concurso", "Data"] + [f"jogo {i}" for i in range(1, 15)],
        bom=False,
        xlsx_bolas=range(3, 17),
        literal=True,
    ),
    "loteriafederal": dict(
        arquivo="loteriafederal.csv",
        api="federal",
        xlsx="LOTERIA_FEDERAL",
        cabecalho=["Extracao", "Data"] + [f"premio {i}" for i in range(1, 6)],
        bom=False,
        xlsx_bolas=[3, 5, 7, 9, 11],
        zero_preenche=6,
        posicional=True,
    ),
}


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
def http_get(url: str, timeout: int = 60, tentativas: int = 4, binario: bool = False):
    """GET com repetição e espera crescente. Retorna bytes/str ou None."""
    espera = 0.6
    for tentativa in range(1, tentativas + 1):
        try:
            req = Request(url, headers=CABECALHO_HTTP)
            with urlopen(req, timeout=timeout) as resp:
                dados = resp.read()
            return dados if binario else dados.decode("utf-8", "replace")
        except HTTPError as erro:
            if erro.code in (404, 500, 502, 503) and tentativa == tentativas:
                return None
            if erro.code in (400, 403, 429):
                time.sleep(espera * tentativa)
                continue
        except (URLError, TimeoutError, OSError):
            pass
        time.sleep(espera * tentativa)
        espera *= 2
    return None


def baixa_planilha(nome_xlsx: str, tentativas: int = 40) -> Path | None:
    """Baixa o XLSX oficial de histórico. O endpoint é balanceado entre nós,
    então repete até receber um arquivo XLSX de verdade."""
    DIR_BULK.mkdir(parents=True, exist_ok=True)
    destino = DIR_BULK / f"{nome_xlsx}.xlsx"
    if destino.exists() and zipfile.is_zipfile(destino):
        return destino
    url = URL_DOWNLOAD + "?" + urlencode({"modalidade": nome_xlsx})
    for tentativa in range(1, tentativas + 1):
        dados = http_get(url, timeout=120, tentativas=1, binario=True)
        if dados and dados[:2] == b"PK":
            destino.write_bytes(dados)
            print(f"    planilha {nome_xlsx}.xlsx obtida (tentativa {tentativa}, {len(dados):,} bytes)")
            return destino
        time.sleep(0.4)
    print(f"    !! não foi possível baixar a planilha {nome_xlsx}.xlsx")
    return None


def consulta_api(slug: str, concurso: int) -> dict | None:
    """Consulta um concurso na API oficial, com cache local em disco."""
    pasta = DIR_API / slug
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / f"{concurso}.json"
    if arquivo.exists():
        texto = arquivo.read_text(encoding="utf-8")
        return json.loads(texto) if texto.strip() not in ("", "null") else None
    texto = http_get(f"{BASE_API}/{slug}/{concurso}")
    if texto is None:
        arquivo.write_text("null", encoding="utf-8")
        return None
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError:
        return None
    if not dados or "numero" not in dados:
        arquivo.write_text("null", encoding="utf-8")
        return None
    arquivo.write_text(texto, encoding="utf-8")
    return dados


def ultimo_concurso(slug: str) -> dict | None:
    """Último concurso publicado (endpoint sem número de concurso)."""
    texto = http_get(f"{BASE_API}/{slug}")
    if not texto:
        return None
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError:
        return None
    return dados if dados and "numero" in dados else None


# ---------------------------------------------------------------------------
# Leitura de XLSX sem dependências externas
# ---------------------------------------------------------------------------
def _indice_coluna(ref: str) -> int:
    total = 0
    for caractere in ref:
        total = total * 26 + (ord(caractere) - 64)
    return total


def le_xlsx(caminho: Path) -> list[dict[int, str]]:
    """Lê a primeira planilha de um .xlsx e devolve linhas como {coluna: texto}."""
    with zipfile.ZipFile(caminho) as z:
        compartilhadas: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            raiz = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for item in raiz.findall(NS + "si"):
                compartilhadas.append("".join(t.text or "" for t in item.iter(NS + "t")))
        abas = sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
        linhas: list[dict[int, str]] = []
        for aba in abas:
            for linha in ET.fromstring(z.read(aba)).iter(NS + "row"):
                celulas: dict[int, str] = {}
                posicao = 0
                for celula in linha.findall(NS + "c"):
                    ref = celula.get("r")
                    posicao = _indice_coluna(re.match(r"([A-Z]+)", ref).group(1)) if ref else posicao + 1
                    tipo = celula.get("t")
                    valor = celula.find(NS + "v")
                    inline = celula.find(NS + "is")
                    if tipo == "s" and valor is not None:
                        texto = compartilhadas[int(valor.text)]
                    elif tipo == "inlineStr" and inline is not None:
                        texto = "".join(t.text or "" for t in inline.iter(NS + "t"))
                    elif valor is not None:
                        texto = valor.text or ""
                    else:
                        texto = ""
                    celulas[posicao] = texto
                linhas.append(celulas)
            break  # apenas a primeira aba
    return linhas


# ---------------------------------------------------------------------------
# Normalização: cada linha do CSV vira [concurso, data, *dezenas, *extras]
# ---------------------------------------------------------------------------
def _texto(celulas: dict[int, str], coluna: int) -> str:
    valor = celulas.get(coluna)
    return "" if valor is None else str(valor).strip()


def _inteiro(texto: str) -> str:
    """'09' -> '9'; '0' -> '0'; '' -> ''."""
    if texto == "":
        return ""
    return str(int(float(texto)))


def _limpa_espacos(texto: str) -> str:
    """Remove preenchimento de espaços/tabs e caracteres nulos das fontes oficiais."""
    return " ".join(texto.replace("\x00", " ").split())


def _ganhadores_api(dados: dict) -> str:
    for faixa in dados.get("listaRateioPremio") or []:
        if faixa.get("faixa") == 1:
            return str(faixa.get("numeroDeGanhadores", ""))
    return ""


def _colunas_loteca(dados: dict) -> list[str]:
    """Deriva a coluna apostada (1 / meio / 2) a partir do placar de cada jogo."""
    jogos = sorted(
        dados.get("listaResultadoEquipeEsportiva") or [],
        key=lambda item: item.get("nuSequencial") or 0,
    )
    colunas: list[str] = []
    for jogo in jogos[:14]:
        casa = jogo.get("nuGolEquipeUm")
        fora = jogo.get("nuGolEquipeDois")
        if casa is None or fora is None:
            colunas.append("")
        elif casa > fora:
            colunas.append("Coluna 1")
        elif casa < fora:
            colunas.append("Coluna 2")
        else:
            colunas.append("Coluna do meio")
    return colunas


def linha_da_api(nome: str, dados: dict) -> list[str] | None:
    concurso = dados.get("numero")
    data = dados.get("dataApuracao")
    if concurso is None or not data:
        return None
    base = [str(int(concurso)), data]

    if nome == "megasena":
        bolas = [str(int(x)) for x in sorted(dados["listaDezenas"], key=int)]
        return base + bolas + [_ganhadores_api(dados), ""]

    if nome in ("quina", "lotofacil", "diadesorte", "lotomania", "duplasena", "supersete"):
        bolas = dados.get("dezenasSorteadasOrdemSorteio") or dados.get("listaDezenas") or []
        return base + [str(int(x)) for x in bolas]

    if nome == "timemania":
        bolas = dados.get("dezenasSorteadasOrdemSorteio") or dados.get("listaDezenas") or []
        time_coracao = _limpa_espacos(dados.get("nomeTimeCoracaoMesSorte") or "")
        return base + [str(int(x)) for x in bolas] + [time_coracao]

    if nome == "maismilionaria":
        bolas = [str(int(x)) for x in dados["listaDezenas"]]
        trevos = [str(int(x)) for x in (dados.get("trevosSorteados") or [])]
        return base + bolas + trevos

    if nome == "loteca":
        return base + _colunas_loteca(dados)

    if nome == "loteriafederal":
        premios = [str(x).zfill(6) for x in (dados.get("listaDezenas") or [])]
        return base + premios

    return None


def linha_da_planilha(nome: str, cfg: dict, celulas: dict[int, str]) -> list[str] | None:
    concurso = _texto(celulas, 1)
    data = _texto(celulas, 2)
    if not concurso.isdigit() or not data:
        return None
    base = [str(int(concurso)), data]

    if cfg.get("literal"):
        bolas = [_texto(celulas, coluna) for coluna in cfg["xlsx_bolas"]]
    elif cfg.get("zero_preenche"):
        bolas = [(_texto(celulas, c).zfill(cfg["zero_preenche"]) if _texto(celulas, c) else "")
                 for c in cfg["xlsx_bolas"]]
    else:
        bolas = [_inteiro(_texto(celulas, coluna)) for coluna in cfg["xlsx_bolas"]]

    extras: list[str] = []
    if nome == "megasena":
        extras = [_texto(celulas, cfg["xlsx_extra"]["gan"]), ""]
    elif nome == "timemania":
        extras = [_limpa_espacos(_texto(celulas, cfg["xlsx_extra"]["time"]))]
    elif nome == "maismilionaria":
        extras = [_inteiro(_texto(celulas, c)) for c in cfg["xlsx_extra"]["trevos"]]

    return base + bolas + extras


# ---------------------------------------------------------------------------
# Coleta do histórico oficial
# ---------------------------------------------------------------------------
def coleta_oficial(nome: str, cfg: dict, usar_bulk: bool, trabalhadores: int = 10) -> dict[int, list[str]]:
    oficial: dict[int, list[str]] = {}

    # 1) planilha oficial (histórico completo)
    if usar_bulk:
        caminho = baixa_planilha(cfg["xlsx"])
        if caminho:
            linhas = le_xlsx(caminho)
            for celulas in linhas[1:]:
                linha = linha_da_planilha(nome, cfg, celulas)
                if linha:
                    oficial[int(linha[0])] = linha
            print(f"    planilha: {len(oficial)} concursos (até {max(oficial):,})")

    ultimo = ultimo_concurso(cfg["api"])
    if not ultimo:
        print(f"    !! não foi possível obter o último concurso de {nome}")
        return oficial
    numero_ultimo = int(ultimo["numero"])

    # 2) lacunas internas da planilha (concursos cancelados não retornam nada)
    # 3) trecho final ainda não publicado na planilha
    if cfg.get("api_tudo"):
        lacunas: list[int] = []
        faltantes = list(range(1, numero_ultimo + 1))
    else:
        inicio = (max(oficial) + 1) if oficial else 1
        lacunas = sorted(set(range(1, inicio)) - set(oficial)) if oficial else []
        faltantes = lacunas + list(range(inicio, numero_ultimo + 1))
    print(f"    API: {len(faltantes)} concursos a consultar (lacunas={len(lacunas)}, cauda={len(faltantes) - len(lacunas)})")

    if faltantes:
        def busca(concurso: int):
            return concurso, consulta_api(cfg["api"], concurso)

        with ThreadPoolExecutor(max_workers=trabalhadores) as executor:
            for concurso, dados in executor.map(busca, faltantes):
                if not dados:
                    continue
                linha = linha_da_api(nome, dados)
                if linha:
                    oficial[int(linha[0])] = linha
    return oficial


# ---------------------------------------------------------------------------
# CSV local
# ---------------------------------------------------------------------------
def le_csv(caminho: Path) -> tuple[list[str], list[str], dict[int, list[str]]]:
    """Devolve (cabeçalho, linhas_originais, {concurso: campos})."""
    if not caminho.exists():
        return [], [], {}
    texto = caminho.read_text(encoding="utf-8-sig")
    linhas = [linha for linha in texto.splitlines() if linha.strip()]
    if not linhas:
        return [], [], {}
    cabecalho = next(csv.reader([linhas[0]]))
    corpo = linhas[1:]
    registros: dict[int, list[str]] = {}
    for linha in corpo:
        campos = next(csv.reader([linha]))
        if campos and campos[0].strip().isdigit():
            registros[int(campos[0])] = campos
    return cabecalho, corpo, registros


# colunas do CSV que a fonte oficial não cobre (ficam em branco nas linhas novas)
COLUNAS_IGNORADAS = {"megasena": {9}}  # 'Apostas' (nº de apostas, não publicado pela Caixa)


def compara(nome: str, cfg: dict, local: list[str], oficial: list[str]) -> list[str]:
    """Compara a linha local com a oficial.

    O bloco de dezenas é comparado como multiconjunto, porque os arquivos
    locais guardam a *ordem do sorteio* em parte das linhas e a planilha
    oficial traz as dezenas em ordem crescente — os conjuntos são os mesmos.
    As demais colunas (ganhadores, time do coração, trevos) são comparadas
    posicionalmente e qualquer diferença é uma divergência real.
    """
    divergencias: list[str] = []
    limite = min(len(local), len(oficial))
    ignoradas = COLUNAS_IGNORADAS.get(nome, set())
    n_bolas = len(cfg["xlsx_bolas"])

    if cfg.get("literal") or cfg.get("posicional"):
        for indice in range(2, limite):
            if indice in ignoradas:
                continue
            a, b = local[indice].strip(), oficial[indice].strip()
            if cfg.get("literal"):
                if a.lower() != b.lower():
                    divergencias.append(f"col{indice}: local={a!r} oficial={b!r}")
            elif a != b and not (a.isdigit() and b.isdigit() and int(a) == int(b)):
                divergencias.append(f"col{indice}: local={a!r} oficial={b!r}")
        return divergencias

    blocos = [(2, 2 + n_bolas)]
    if nome == "duplasena":  # dois sorteios independentes de 6 dezenas
        blocos = [(2, 8), (8, 14)]
    for inicio, fim in blocos:
        a = sorted(int(x) for x in local[inicio:fim] if x.strip().isdigit())
        b = sorted(int(x) for x in oficial[inicio:fim] if x.strip().isdigit())
        if a != b:
            divergencias.append(f"dezenas: local={local[inicio:fim]} oficial={oficial[inicio:fim]}")

    for indice in range(2 + n_bolas, limite):
        if indice in ignoradas:
            continue
        a, b = local[indice].strip(), oficial[indice].strip()
        if a == b or (a.isdigit() and b.isdigit() and int(a) == int(b)):
            continue
        divergencias.append(f"col{indice}: local={a!r} oficial={b!r}")
    return divergencias


def corrige_linha(nome: str, cfg: dict, linha_local: str, linha_oficial: list[str]) -> str:
    """Substitui nas linhas antigas apenas as colunas extra (ganhadores, time,
    trevos) pelos valores oficiais, preservando as dezenas e a ordem do arquivo."""
    if cfg.get("literal") or cfg.get("posicional"):
        return linha_local
    campos = next(csv.reader([linha_local]))
    ignoradas = COLUNAS_IGNORADAS.get(nome, set())
    n_bolas = len(cfg["xlsx_bolas"])
    alterou = False
    for indice in range(2 + n_bolas, min(len(campos), len(linha_oficial))):
        if indice in ignoradas:
            continue
        if campos[indice].strip() != linha_oficial[indice].strip():
            campos[indice] = linha_oficial[indice]
            alterou = True
    return ",".join(campos) if alterou else linha_local


def grava_csv(caminho: Path, cabecalho: list[str], novas: list[list[str]], antigas: list[str], bom: bool) -> None:
    codificacao = "utf-8-sig" if bom else "utf-8"
    partes = [",".join(cabecalho)]
    partes += [",".join(linha) for linha in novas]
    partes += antigas
    caminho.write_text("\n".join(partes) + "\n", encoding=codificacao, newline="\n")


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------
def atualiza(nome: str, cfg: dict, args) -> dict:
    caminho = DADOS / cfg["arquivo"]
    cabecalho_local, corpo_local, registros_local = le_csv(caminho)
    total_local = len(registros_local)
    maximo_local = max(registros_local) if registros_local else 0

    print(f"\n== {nome}  ({cfg['arquivo']})")
    print(f"    local: {total_local} concursos, último = {maximo_local if maximo_local else '-'}")

    oficial = coleta_oficial(nome, cfg, usar_bulk=not args.sem_bulk)
    if not oficial:
        print("    !! nenhum dado oficial obtido, nada a fazer")
        return dict(modalidade=nome, erro="sem dados oficiais")

    # conferência do histórico já existente
    comparados = 0
    divergentes: dict[int, list[str]] = {}
    for concurso, linha_local in registros_local.items():
        linha_oficial = oficial.get(concurso)
        if not linha_oficial:
            continue
        comparados += 1
        diferencas = compara(nome, cfg, linha_local, linha_oficial)
        if diferencas:
            divergentes[concurso] = diferencas

    novos = {c: linha for c, linha in oficial.items() if c not in registros_local}
    novos_ordenados = [novos[c] for c in sorted(novos, reverse=True)]

    total_final = total_local + len(novos_ordenados)
    maximo_final = max(oficial) if oficial else maximo_local
    lacunas_finais = sorted(set(range(1, maximo_final + 1)) - (set(registros_local) | set(oficial)))

    print(f"    conferidos: {comparados} concursos | divergências: {len(divergentes)}")
    if divergentes:
        for concurso in list(sorted(divergentes))[:5]:
            print(f"      concurso {concurso}: {'; '.join(divergentes[concurso][:3])}")
    print(f"    novos: {len(novos_ordenados)} concursos -> total {total_final}, último {maximo_final}")

    if args.so_verificar:
        return dict(modalidade=nome, arquivo=cfg["arquivo"], local=total_local,
                    novos=len(novos_ordenados), total=total_final, ultimo=maximo_final,
                    conferidos=comparados, divergencias=len(divergentes),
                    lacunas=lacunas_finais, gravado=False)

    # correção opcional das colunas extra divergentes no histórico antigo
    corrigidas = 0
    if args.corrigir and divergentes:
        corpo_corrigido: list[str] = []
        for linha in corpo_local:
            campos = next(csv.reader([linha]))
            if campos and campos[0].strip().isdigit() and int(campos[0]) in divergentes:
                nova = corrige_linha(nome, cfg, linha, oficial[int(campos[0])])
                if nova != linha:
                    corrigidas += 1
                corpo_corrigido.append(nova)
            else:
                corpo_corrigido.append(linha)
        corpo_local = corpo_corrigido
        print(f"    linhas antigas corrigidas: {corrigidas}")

    if not novos_ordenados and not corrigidas:
        print("    nada novo a gravar")
        return dict(modalidade=nome, arquivo=cfg["arquivo"], local=total_local, novos=0,
                    total=total_local, ultimo=maximo_final, conferidos=comparados,
                    divergencias=len(divergentes), lacunas=lacunas_finais, gravado=False)

    cabecalho = cabecalho_local if cabecalho_local else cfg["cabecalho"]
    if cabecalho_local and len(cabecalho_local) != len(cfg["cabecalho"]):
        print(f"    !! cabeçalho local com {len(cabecalho_local)} colunas "
              f"(esperado {len(cfg['cabecalho'])}), mantido o original")

    if caminho.exists():
        carimbo = datetime.now().strftime("%Y%m%d-%H%M%S")
        destino = DIR_BACKUP / carimbo
        destino.mkdir(parents=True, exist_ok=True)
        shutil.copy2(caminho, destino / cfg["arquivo"])

    grava_csv(caminho, cabecalho, novos_ordenados, corpo_local, cfg["bom"])
    print(f"    gravado: {caminho}  (+{len(novos_ordenados)} linhas no topo)")
    return dict(modalidade=nome, arquivo=cfg["arquivo"], local=total_local,
                novos=len(novos_ordenados), total=total_final, ultimo=maximo_final,
                conferidos=comparados, divergencias=len(divergentes),
                corrigidas=corrigidas, lacunas=lacunas_finais, gravado=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Atualiza os históricos das loterias da Caixa em dados/.")
    parser.add_argument("--modalidade", action="append", choices=sorted(MODALIDADES),
                        help="atualiza apenas estas modalidades (pode repetir)")
    parser.add_argument("--sem-bulk", action="store_true",
                        help="não usa as planilhas XLSX oficiais (somente API, bem mais lento)")
    parser.add_argument("--so-verificar", action="store_true",
                        help="não grava os CSVs, apenas confere contra a fonte oficial")
    parser.add_argument("--corrigir", action="store_true",
                        help="também corrige, no histórico antigo, colunas divergentes "
                             "(ganhadores/time/trevos) em relação à fonte oficial")
    parser.add_argument("--trabalhadores", type=int, default=10,
                        help="consultas simultâneas à API (padrão 10)")
    args = parser.parse_args()

    DADOS.mkdir(exist_ok=True)
    CACHE.mkdir(exist_ok=True)

    selecionadas = args.modalidade or list(MODALIDADES)
    inicio = time.time()
    print("Atualização dos históricos das loterias da Caixa")
    print(f"Data: {datetime.now():%d/%m/%Y %H:%M}  |  modalidades: {', '.join(selecionadas)}")

    relatorio = []
    for nome in selecionadas:
        relatorio.append(atualiza(nome, MODALIDADES[nome], args))

    print("\n" + "=" * 78)
    print(f"{'modalidade':<16}{'local':>8}{'novos':>8}{'total':>8}{'último':>9}{'diverge':>9}")
    print("-" * 78)
    for item in relatorio:
        if item.get("erro"):
            print(f"{item['modalidade']:<16}{'ERRO':>8}  {item['erro']}")
            continue
        print(f"{item['modalidade']:<16}{item['local']:>8}{item['novos']:>8}{item['total']:>8}"
              f"{item['ultimo']:>9}{item['divergencias']:>9}")
    print("-" * 78)
    print(f"Tempo total: {time.time() - inicio:.1f}s")

    destino = CACHE / "relatorio_atualizacao.json"
    destino.write_text(json.dumps({"quando": datetime.now().isoformat(timespec="seconds"),
                                   "resultados": relatorio}, ensure_ascii=False, indent=2),
                       encoding="utf-8")
    print(f"Relatório: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
