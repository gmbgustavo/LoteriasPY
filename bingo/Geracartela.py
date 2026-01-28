# GERADOR DE CARTELAS DE BINGO EM PDF

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class Geracartela:
    @staticmethod
    def salva_pdf(cartelas, nome_arquivo="cartelas_bingo.pdf", titulo="BINGO DA AMIZADE"):
        """
        Salva todas as cartelas em um PDF, uma por página.
        Letras B I N G O na primeira linha da grade.
        5 linhas de números perfeitamente dentro da grade.
        
        Args:
            cartelas: Lista de cartelas (cada cartela é uma lista de números)
            nome_arquivo: Nome do arquivo PDF a ser gerado
            titulo: Título a ser exibido acima de cada cartela
        """
        quantidade = len(cartelas)
        
        with PdfPages(nome_arquivo) as pdf:
            for i in range(quantidade):
                # Ordena a cartela atual
                if isinstance(cartelas[i], list):
                    cartelas[i].sort()

                # Cria a figura menor
                fig = plt.figure(figsize=(4, 5))
                ax = fig.add_axes((0, 0, 1, 1))
                ax.axis('off')
                fig.patch.set_facecolor('white')

                # Título acima da cartela
                ax.text(0.5, 0.82, titulo, ha='center', va='center',
                        fontsize=34, fontweight='bold')

                # Define margens e tamanho das células - grid mais compacto
                left, right = 0.20, 0.80
                top, bottom = 0.77, 0.30  # Grid começa ~1.5cm abaixo do título e margem maior inferior
                cell_width = (right - left) / 5
                cell_height = (top - bottom) / 7  # 7 linhas totais: header + 5 linhas de números + linha extra

                # Desenha as 7 linhas horizontais primeiro para definir a altura total
                for j in range(7):
                    y = top - j * cell_height
                    ax.hlines(y, left, right, colors='black', linewidth=2)

                # Desenha as 6 linhas verticais terminando exatamente na última linha horizontal
                last_horizontal_y = top - 6 * cell_height  # Posição da 7ª linha horizontal (índice 6)
                for j in range(6):
                    x = left + j * cell_width
                    ax.vlines(x, last_horizontal_y, top, colors='black', linewidth=2)

                # Letras B I N G O na primeira linha (índice 0)
                letras = ['B', 'I', 'N', 'G', 'O']
                for coluna, letra in enumerate(letras):
                    x_centro = left + (coluna + 0.5) * cell_width
                    y_centro = top - 0.5 * cell_height  # centro da primeira célula
                    ax.text(x_centro, y_centro, letra,
                            ha='center', va='center',
                            fontsize=40, fontweight='bold', color='darkblue')

                # Números nas linhas 1 a 5 da grade (índices 1 a 5)
                for linha in range(5):  # linha 0..4 → corresponde às linhas 1..5 da grade
                    for coluna in range(5):
                        indice = coluna * 5 + linha
                        numero = cartelas[i][indice]

                        x_centro = left + (coluna + 0.5) * cell_width
                        # Centro da linha atual (começando da linha 1 da grade, após o header)
                        y_centro = top - (linha + 1.5) * cell_height

                        ax.text(x_centro, y_centro, f"{numero:2d}",
                                ha='center', va='center',
                                fontsize=16, fontweight='bold')

                # Salva a página no PDF
                pdf.savefig(fig, bbox_inches='tight', dpi=300)
                plt.close(fig)

        print(f"{quantidade} cartela(s) salva(s) com sucesso em '{nome_arquivo}'!")