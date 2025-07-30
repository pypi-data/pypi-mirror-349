def contar_palavras(texto):
    palavras = texto.split()
    return len(palavras)

def contar_caracteres(texto):
    return len(texto)

def palavra_mais_longa(texto):
    palavras = texto.split()
    return max(palavras, key=len)