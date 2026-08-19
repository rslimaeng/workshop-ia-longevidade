#!/usr/bin/env python3
"""
Recorta a capa dos tres videos a partir dos prints que o Rafael tirou da
listagem do YouTube, e grava em _img/.

Por que recortar em vez de usar o print inteiro: o print traz titulo, canal e
contagem de visualizacoes ao lado da capa. O cartao .fonte ja escreve titulo e
canal em texto nitido, entao o print inteiro duplicaria tudo isso em baixa
resolucao. E "18 mil visualizacoes / ha 4 dias" e numero que envelhece sozinho.

Tambem corta a barra vermelha de progresso do rodape da capa: ela e o quanto a
conta do Rafael assistiu do video, nao faz parte da capa.

Rodar:  python3 _build/gera-capas.py
"""

import os
import numpy as np
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "_img")
FONTE = os.path.abspath(os.path.join(RAIZ, "..", "3-material-ai-first", "assets"))

CAPAS = {
    "video-blomfield-ai-native.jpg": (
        "youtube-building-and-structuring-an-ai-native-company",
        "Captura de Tela 2026-08-19 às 07.30.24.png"),
    "video-greg-ai-native.jpg": (
        "youtube-greg-become-ai-native-in-less-than-60-min",
        "Captura de Tela 2026-08-19 às 07.30.40.png"),
    "video-blomfield-self-improving.jpg": (
        "youtube-y-combinator-how-to-build-a-self-improving-company-with-ai",
        "Captura de Tela 2026-08-19 às 07.30.59.png"),
}


def caixa_da_capa(a):
    """Acha a capa: o bloco largo entre o icone de arrastar e o texto."""
    naobranco = a.min(axis=2) < 235
    meia = naobranco[:, :int(a.shape[1] * 0.45)]
    cols = np.where(meia.any(axis=0))[0]
    saltos = np.where(np.diff(cols) > 5)[0]
    assert len(saltos) >= 2, "esperava duas lacunas: icone | capa | texto"
    x0, x1 = int(cols[saltos[0] + 1]), int(cols[saltos[1]]) + 1
    linhas = np.where(naobranco[:, x0:x1].any(axis=1))[0]
    return x0, int(linhas.min()), x1, int(linhas.max()) + 1


def sem_barra_de_progresso(a, y0, y1, x0, x1):
    """Sobe o rodape ate acima da barra vermelha do YouTube, se houver."""
    faixa = a[y0:y1, x0:x1]
    vermelha = ((faixa[:, :, 0] > 150) & (faixa[:, :, 1] < 110)
                & (faixa[:, :, 2] < 130)).mean(axis=1)
    # a barra e continua ate o fim da imagem; anda de baixo para cima
    corte = len(vermelha)
    while corte > 0 and vermelha[corte - 1] > 0.40:
        corte -= 1
    return y0 + corte


def main():
    os.makedirs(SAIDA, exist_ok=True)
    for nome, (pasta, print_) in CAPAS.items():
        origem = os.path.join(FONTE, pasta, print_)
        im = Image.open(origem).convert("RGB")
        a = np.asarray(im).astype(int)
        x0, y0, x1, y1 = caixa_da_capa(a)
        y1 = sem_barra_de_progresso(a, y0, y1, x0, x1)
        corte = im.crop((x0, y0, x1, y1))
        destino = os.path.join(SAIDA, nome)
        corte.save(destino, "JPEG", quality=88, optimize=True, progressive=True)
        kb = os.path.getsize(destino) // 1024
        print(f"{nome:38} {corte.width}x{corte.height}  {kb} KB")


if __name__ == "__main__":
    main()
