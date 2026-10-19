
RODADAS = 16
MASCARA = 0xFFFFFFFF  # mantém os números em 32 bits


def gerar_subchaves(chave):
    """Gera 16 subchaves de 32 bits misturando os bytes da chave."""
    subchaves = []
    for i in range(RODADAS):
        k = i
        for byte in chave.encode():
            k = (k * 31 + byte) & MASCARA
        subchaves.append(k)
    return subchaves


def f(R, k):
    """Função da rodada (simples): soma com a subchave e XOR com ela."""
    return ((R + k) & MASCARA) ^ k


def processar_bloco(bloco, subchaves):
    """Aplica as 16 rodadas a um bloco de 8 bytes."""
    L = int.from_bytes(bloco[:4], "big")
    R = int.from_bytes(bloco[4:], "big")

    for k in subchaves:
        L, R = R, L ^ f(R, k)   # rodada de Feistel

    L, R = R, L                 # troca final (permite reusar o código ao decriptar)
    return L.to_bytes(4, "big") + R.to_bytes(4, "big")


def encriptar(texto, chave):
    """Encripta bytes: completa o último bloco (padding) e cifra bloco a bloco."""
    n = 8 - len(texto) % 8
    texto += bytes([n] * n)     # padding: n bytes com valor n
    subchaves = gerar_subchaves(chave)
    return b"".join(processar_bloco(texto[i:i + 8], subchaves)
                    for i in range(0, len(texto), 8))


def decriptar(cifrado, chave):
    """Decripta bytes: mesmo processo, com as subchaves em ordem inversa."""
    subchaves = gerar_subchaves(chave)[::-1]
    texto = b"".join(processar_bloco(cifrado[i:i + 8], subchaves)
                     for i in range(0, len(cifrado), 8))
    if not 1 <= texto[-1] <= 8:  # padding inválido -> chave errada
        raise ValueError
    return texto[:-texto[-1]]   # remove o padding



# Menu interativo
while True:
    opcao = input("\n1 - Encriptar | 2 - Decriptar | 0 - Sair: ").strip()

    if opcao == "1":
        texto = input("Mensagem: ")
        chave = input("Chave: ")
        print("Texto cifrado (hex):", encriptar(texto.encode(), chave).hex())

    elif opcao == "2":
        try:
            cifrado = bytes.fromhex(input("Texto cifrado (hex): ").strip())
            chave = input("Chave: ")
            print("Texto decifrado:", decriptar(cifrado, chave).decode())
        except ValueError:  # hex inválido ou chave errada (UnicodeDecodeError herda de ValueError)
            print("Erro: hexadecimal inválido ou chave incorreta.")

    elif opcao == "0":
        break

    else:
        print("Opção inválida.")