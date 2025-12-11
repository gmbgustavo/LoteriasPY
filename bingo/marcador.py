#MARCA O BINGO EM TEMPO REAL

def cria_cartela(quantidade: int):
    newcard=[]
    for x in range(1, quantidade + 1):
        newcard.append(input('Digite os números da sua cartela: '))
    print(f' Sua cartela: {newcard}')
    resp=input('Confirma? [S/N]')
    if resp.upper()=='S':
        return newcard
    else:
        quit(1)

def conferir(card):
    pontos = 0
    for y in range(1, 76):
        print(f'Você tem {pontos} acertos. \n')
        sorteado = input('Digite o número que foi cantado: ')
        if sorteado in card:
            pontos += 1
        else:
            continue


if __name__ == '__main__':
    qtd = input('Quantos números na cartela? ')
    cartela = cria_cartela(int(qtd))
    conferir(cartela)


