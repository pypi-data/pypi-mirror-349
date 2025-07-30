import unicodedata
import string

def remover_acentos(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def limpar_texto(texto):
    texto = remover_acentos(texto.lower())
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    return texto.replace(" ", "")

def eh_palindromo(texto):
    texto_limpo = limpar_texto(texto)
    return texto_limpo == texto_limpo[::-1]