# Cifra de Feistel com 16 rodadas

Implementação didática de uma **Cifra de Feistel** em Python, com encriptação e decriptação e um menu interativo no terminal.

## Requisitos

- Python 3.6 ou superior

## Como executar

No terminal, na pasta do arquivo:

```bash
python feistel.py
```

O programa mostra um menu que se repete até você sair:

```
1 - Encriptar | 2 - Decriptar | 0 - Sair:
```

| Opção | O que faz |
|-------|-----------|
| `1` | Pede a mensagem e a chave, e mostra o texto cifrado em hexadecimal |
| `2` | Pede o texto cifrado (hex) e a chave, e mostra a mensagem original |
| `0` | Encerra o programa |

### Exemplo de uso

```
1 - Encriptar | 2 - Decriptar | 0 - Sair: 1
Mensagem: Olá mundo, teste de Feistel!
Chave: abc
Texto cifrado (hex): 6f1e91ff206f051410e894ec74725584454478c6205c7a295299cc6521e2e611

1 - Encriptar | 2 - Decriptar | 0 - Sair: 2
Texto cifrado (hex): 6f1e91ff206f051410e894ec74725584454478c6205c7a295299cc6521e2e611
Chave: abc
Texto decifrado: Olá mundo, teste de Feistel!
```

Se a chave estiver errada ou o hexadecimal for inválido, o programa mostra uma mensagem de erro. Em casos raros, uma chave errada pode passar pela verificação do padding e gerar um texto sem sentido.

## Como funciona

### 1. Estrutura de Feistel

A mensagem é dividida em blocos de **64 bits (8 bytes)**. Cada bloco é separado em duas metades de 32 bits: **L** (esquerda) e **R** (direita).

A cada uma das **16 rodadas**, o bloco passa por esta transformação:

```
L_novo = R
R_novo = L XOR f(R, subchave)
```

```
        L              R
        │              │
        │      ┌───────┴───────┐
        │      │  f(R, chave)  │
        │      └───────┬───────┘
        └───────⊕──────┘
        │              │
    L_novo = R     R_novo = L ⊕ f(R, k)
```

Depois da 16ª rodada, as metades são trocadas uma última vez e juntadas de volta em um bloco de 8 bytes.


### 3. Geração das subchaves

A função `gerar_subchaves` cria **16 subchaves de 32 bits**, uma por rodada. Para cada rodada `i`, ela parte de `k = i` e, para cada byte da chave, calcula:

```
k = (k * 31 + byte) mod 2^32
```

Assim, cada rodada recebe uma subchave diferente, derivada da chave digitada.

### 4. Função da rodada `f`

```python
def f(R, k):
    return ((R + k) & MASCARA) ^ k
```

Soma `R` com a subchave (módulo 2³²) e faz XOR com a subchave. É uma função simples.

### 5. Padding

O tamanho da mensagem nem sempre é múltiplo de 8 bytes, então o último bloco é completado antes de cifrar: adicionam-se `n` bytes, cada um com valor `n` (de 1 a 8). Na decriptação, esse padding é lido e removido.

## Estrutura do código

| Função | Responsabilidade |
|--------|------------------|
| `gerar_subchaves(chave)` | Deriva as 16 subchaves a partir da chave |
| `f(R, k)` | Função da rodada |
| `processar_bloco(bloco, subchaves)` | Aplica as 16 rodadas a um bloco de 8 bytes |
| `encriptar(texto, chave)` | Adiciona padding e cifra bloco a bloco |
| `decriptar(cifrado, chave)` | Decifra bloco a bloco (subchaves invertidas) e remove o padding |
| Menu (fim do arquivo) | Interação com o usuário |


