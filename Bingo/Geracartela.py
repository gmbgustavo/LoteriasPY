# GERADOR DE CARTELAS DE BINGO EM PDF
#
# Cada cartela ocupa uma página, com a grade de 5x5, o cabeçalho B I N G O e o
# número da cartela. A lista de dezenas chega na ordem coluna a coluna
# (indice = coluna * 5 + linha), a mesma usada na impressão no terminal.

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

LETRAS = ['B', 'I', 'N', 'G', 'O']

# geometria da página (coordenadas da figura, de 0 a 1)
TITULO_Y = 0.935
SUBTITULO_Y = 0.885
GRADE_ESQUERDA, GRADE_DIREITA = 0.12, 0.88
GRADE_TOPO, GRADE_BASE = 0.845, 0.09
LINHAS_GRADE = 6          # 1 de cabeçalho + 5 de dezenas
COLUNAS_GRADE = 5


class Geracartela:
    @staticmethod
    def salva_pdf(cartelas, nome_arquivo="cartelas_bingo.pdf", titulo="BINGO DA AMIZADE"):
        """
        Salva todas as cartelas em um PDF, uma por página.

        Args:
            cartelas: lista de cartelas; cada cartela é uma lista de 25 dezenas
                      na ordem coluna a coluna
            nome_arquivo: nome do arquivo PDF a ser gerado
            titulo: título exibido no alto de cada página

        :return: caminho do arquivo gerado (ou None se não houver cartelas)
        """
        quantidade = len(cartelas)
        if not quantidade:
            print("⚠️ Nenhuma cartela para salvar: o PDF não foi gerado.")
            return None

        largura_celula = (GRADE_DIREITA - GRADE_ESQUERDA) / COLUNAS_GRADE
        altura_celula = (GRADE_TOPO - GRADE_BASE) / LINHAS_GRADE

        with PdfPages(nome_arquivo) as pdf:
            for indice, dezenas in enumerate(cartelas):
                fig = plt.figure(figsize=(4, 5))
                ax = fig.add_axes((0, 0, 1, 1))
                ax.axis('off')
                # limites explícitos: sem eles o matplotlib ajusta o eixo ao
                # conteúdo e as linhas da grade acabam cortadas
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                fig.patch.set_facecolor('white')

                ax.text(0.5, TITULO_Y, titulo, ha='center', va='center',
                        fontsize=20, fontweight='bold')

                # linhas horizontais (7 linhas delimitam as 6 linhas de células)
                for linha in range(LINHAS_GRADE + 1):
                    y = GRADE_TOPO - linha * altura_celula
                    ax.hlines(y, GRADE_ESQUERDA, GRADE_DIREITA, colors='black', linewidth=2)

                # linhas verticais (6 linhas delimitam as 5 colunas)
                for coluna in range(COLUNAS_GRADE + 1):
                    x = GRADE_ESQUERDA + coluna * largura_celula
                    ax.vlines(x, GRADE_BASE, GRADE_TOPO, colors='black', linewidth=2)

                # letras B I N G O na primeira linha da grade
                for coluna, letra in enumerate(LETRAS):
                    ax.text(GRADE_ESQUERDA + (coluna + 0.5) * largura_celula,
                            GRADE_TOPO - 0.5 * altura_celula, letra,
                            ha='center', va='center', fontsize=24,
                            fontweight='bold', color='darkblue')

                # dezenas nas 5 linhas seguintes da grade
                for linha in range(5):
                    for coluna in range(COLUNAS_GRADE):
                        posicao = coluna * 5 + linha
                        dezena = dezenas[posicao]
                        ax.text(GRADE_ESQUERDA + (coluna + 0.5) * largura_celula,
                                GRADE_TOPO - (linha + 1.5) * altura_celula,
                                f"{dezena:2d}", ha='center', va='center',
                                fontsize=16, fontweight='bold')

                # sem bbox_inches='tight': a página inteira é mantida e o título
                # não é cortado nas laterais
                pdf.savefig(fig, dpi=300)
                plt.close(fig)

        print(f"{quantidade} cartela(s) salva(s) com sucesso em '{nome_arquivo}'!")
        return nome_arquivo
