def gerar_resumo(texto, num_frases=2):
    frases = texto.split('.')
    frases = [f.strip() for f in frases if f.strip()]
    return '. '.join(frases[:num_frases]) + '.'