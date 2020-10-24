import cv2
import numpy as np

imagemOriginal = "imagem.png"
imagemConvertida = "imagemconvertida.png"

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]


def gerar_mensagem(mensagem):
    lista = []
    for m in mensagem:
        val = ord(m)
        bits = bitfield(val)

        if len(bits) < 8:
            for a in range(8-len(bits)):
                bits.insert(0,0)
        lista.append(bits)
    arr = np.array(lista)
    arr = arr.flatten()
    return arr

def converter_mensagem(saida):
    bits = np.array(saida)
    mensagem_out = ''
    bits = bits.reshape((int(len(saida)/8), 8))
    for b in bits:
        sum = 0
        for i in range(8):
            sum += b[i]*(2**(7-i))
        mensagem_out += chr(sum)
    return mensagem_out


def esconde_mensagem(mensagem):
    img = cv2.imread(imagemOriginal)
    imgAltera = img.copy()
    altura, largura, x = img.shape
    array = gerar_mensagem(mensagem)
    print("mensagem em binario = " + str(array))
    tamanho_mensagem = len(array)
    print("tamanho da mensagem = "+str(tamanho_mensagem))
    pos = 0

    for i in range(altura):
        for j in range(largura):
            if tamanho_mensagem > pos:
                p = img[i][j][0]
                valor = ((p // 10) * 10) + array[pos]
                imgAltera[i][j][0] = valor
            elif tamanho_mensagem == pos:
                imgAltera[i][j][0] = ((p // 10) * 10) + 2
            pos = pos + 1

    cv2.imwrite(imagemConvertida, imgAltera)
    cv2.imshow("image", img)
    cv2.waitKey(0)


def encontra_mensagem():
    img2 = cv2.imread(imagemConvertida)
    altura, largura, x = img2.shape
    mensagem = []
    for i in range(altura):
        for j in range(largura):
            p = img2[i][j][0]
            # print(p)
            if (p % 10) < 2:
                mensagem.append(p % 10)
            elif (p % 10) >= 2:
                print("Mensagem encontrada: ")
                print(converter_mensagem(mensagem))
                return mensagem


esconde_mensagem("lyra for president")
encontra_mensagem()
