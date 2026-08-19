#!/usr/bin/env python3
"""
Gerador das páginas do site do workshop da Longevidade.

O conteúdo de cada página vive em _build/conteudo/<slug>.html como fragmento
(só as <section class="block">). Este script monta o shell: <head>, tokens de
CSS, header, nav lateral com scroll-spy, hero, rodapé e a navegação de pé.

Rodar:  python3 _build/gerar.py
"""

import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = open(os.path.join(RAIZ, "_build", "base.css"), encoding="utf-8").read()

SITE = "Ideação com AI First"
CLIENTE = "Grupo Longevidade Saudável"

# slug -> configuração da página. slug "" é a capa.
PAGINAS = {
    "": dict(
        titulo="Ideação com AI First · Grupo Longevidade Saudável",
        eyebrow="Encerramento da Trilha de Cultura de IA · 4 horas · presencial",
        h1="Não é qual IA a empresa usa. É como a informação circula.",
        lead="Este é o material do dia. Cada página fica no ar depois do workshop, "
             "para você consultar e aplicar na sua área sem precisar de mim.",
        chips=["4 horas", "Turma única", "Todas as áreas"],
        nav=False,
        anterior=None,
        proxima=("ai-first/", "O que muda com AI First"),
    ),
    "ai-first": dict(
        titulo="O que muda com AI First · Ideação com AI First",
        eyebrow="Bloco 2 · Pilares 1 e 2",
        h1="O que muda com AI First",
        lead="A diferença entre usar a inteligência artificial no fim do trabalho e "
             "colocá-la no desenho desde o começo. E os dois pilares que sustentam isso.",
        chips=["Pilar 1 · Registro", "Pilar 2 · Contexto"],
        nav=True,
        anterior=("../", "A capa do dia"),
        proxima=("../caso-1/", "Caso 1 · Conhecimento espalhado"),
    ),
    "caso-1": dict(
        titulo="Caso 1 · Conhecimento espalhado · Ideação com AI First",
        eyebrow="Bloco 3 · Caso em três passos",
        h1="Conhecimento espalhado e muitas frentes ao mesmo tempo",
        lead="Doze frentes de trabalho ao mesmo tempo, cada uma com um papel diferente, "
             "e a resposta boa guardada com quem estava presente.",
        chips=["Prova os pilares 1 e 2", "Trabalho em grupo"],
        nav=True,
        anterior=("../ai-first/", "O que muda com AI First"),
        proxima=("../caso-2/", "Caso 2 · Informação sensível"),
    ),
    "caso-2": dict(
        titulo="Caso 2 · Informação sensível e prazo curto · Ideação com AI First",
        eyebrow="Bloco 4 · Caso em três passos",
        h1="Análise com informação sensível e prazo curto",
        lead="Seis entrevistas de uma hora, trezentas páginas de transcrição, três dias "
             "até a entrega. E alguém vai investir dinheiro com base no resultado.",
        chips=["Prova os pilares 3 e 4", "Trabalho em grupo"],
        nav=True,
        anterior=("../caso-1/", "Caso 1 · Conhecimento espalhado"),
        proxima=("../ficha/", "A ficha dos quatro campos"),
    ),
    "ficha": dict(
        titulo="A ficha dos quatro campos · Ideação com AI First",
        eyebrow="Bloco 5 · Pilar 5",
        h1="A ficha dos quatro campos",
        lead="O filtro que separa a iniciativa que chega à produção da que morre na "
             "demonstração. São quatro perguntas, e nenhuma delas é sobre tecnologia.",
        chips=["Pilar 5 · Escopo com métrica", "Individual"],
        nav=True,
        anterior=("../caso-2/", "Caso 2 · Informação sensível"),
        proxima=("../pilares/", "Os cinco pilares em uma folha"),
    ),
    "pilares": dict(
        titulo="Os cinco pilares em uma folha · Ideação com AI First",
        eyebrow="O que fica com você",
        h1="Os cinco pilares em uma folha",
        lead="A folha para imprimir e deixar à vista. Cada pilar tem o que é, o que você "
             "passa a fazer e a pergunta que você faz para saber se está aplicando.",
        chips=["Imprimível", "Uma folha A4"],
        nav=False,
        anterior=("../ficha/", "A ficha dos quatro campos"),
        proxima=None,
    ),
}


# ----------------------------------------------------------------- quebra de linha
# O Rafael reprovou duas vezes a quebra feia: linha que termina em "na sua" e
# joga "área." para a linha de baixo. text-wrap:pretty não resolve, porque ele
# só evita palavra órfã na ÚLTIMA linha. text-wrap:balance resolve parte. O que
# fecha a conta é colar a palavra-função na palavra seguinte com espaço rígido,
# do jeito que uma gráfica faz: aí a quebra procura outro lugar, e costuma achar
# a fronteira da frase.
#
# Só nos blocos curtos e em evidência (títulos e as chamadas), porque é neles
# que a quebra é visível. Parágrafo corrido de seis linhas ninguém repara, e
# colar lá tiraria do navegador a liberdade de achar a melhor linha.
PALAVRAS_QUE_COLAM = {
    # artigo e possessivo
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "seu", "sua", "seus", "suas", "meu", "minha", "nosso", "nossa",
    # preposicao curta e contracao
    "de", "da", "do", "das", "dos", "em", "na", "no", "nas", "nos",
    "por", "pelo", "pela", "com", "sem", "ao", "aos", "\u00e0", "\u00e0s",
    "para", "pra", "num", "numa", "dum", "duma",
    # preposicao longa: "durante a atividade" quebrando em "durante" foi o caso
    # que sobrou na primeira medicao
    "sobre", "entre", "durante", "at\u00e9", "desde", "ap\u00f3s", "contra", "sob",
    "perante", "conforme", "mediante",
    # conjuncao e relativo, que pedem complemento na mesma linha
    "e", "ou", "mas", "se", "que", "quando", "onde", "enquanto", "porque",
    "n\u00e3o", "j\u00e1", "s\u00f3",
}
# Nenhum trecho colado passa disso: unidade indivisível maior que a linha do
# celular vira rolagem lateral, que é o defeito que a correção deveria evitar.
# 24 foi calibrado medindo: em 20 sobrava "sobre onde a / informação fica",
# porque a corrente já tinha gasto o limite. Em 24 sobra zero, e nenhuma das
# 7 páginas estoura a largura em nenhuma das 5 larguras medidas.
LIMITE_DO_GRUDADO = 24

# Medido no navegador em 5 larguras x 5 paginas: colar so em titulo e chamada
# nao mudou nada (57 antes, 57 depois), porque quase toda quebra ruim mora em
# paragrafo. Cobrindo paragrafo de ate 400 caracteres a conta cai de 169 para
# 17, e nenhuma pagina passa a estourar a largura em nenhuma das 5 larguras.
LIMITE_DO_PARAGRAFO = 400

# label entra por causa do canvas: as alternativas da régua são
# <label class="op"><input><span>texto</span></label>, e é a página que a turma
# abre no celular. Medido lá: 13 quebras ruins em 375px antes de colar.
# <li> entrou na terceira medicao: 8 das 9 linhas que ainda terminavam em
# preposicao moravam em item de lista, seis delas na nav lateral de 232px, que
# a cola nunca tinha coberto. Nenhuma lista do site tem lista dentro, entao o
# .*? nao-guloso fecha no </li> certo.
BLOCO_QUE_COLA = re.compile(
    r'(<h[1-4]\b[^>]*>)(.*?)(</h[1-4]>)'
    r'|(<label\b[^>]*>)(.*?)(</label>)'
    r'|(<p\b[^>]*>)(.*?)(</p>)'
    r'|(<li\b[^>]*>)(.*?)(</li>)',
    re.S,
)
SEM_TAG = re.compile(r"<[^>]+>")


# Estes ja recebem text-wrap:balance por classe propria. Marcar de novo so
# poluiria o atributo, e mexer no class= de um bloco que outro gate procura pelo
# nome exato foi o que deixou o G21 cego na primeira tentativa.
JA_TEM_BALANCE = ("hero-lead", "block-lead", "fig-leg", "lp-perda")


def _marca_curto(abertura):
    """Poe a classe que liga o text-wrap:balance so nos paragrafos colados."""
    if "p-curto" in abertura or any(c in abertura for c in JA_TEM_BALANCE):
        return abertura
    m = re.search(r'class="([^"]*)"', abertura)
    if m:
        return abertura[:m.start(1)] + (m.group(1) + " p-curto").strip() + abertura[m.end(1):]
    return abertura[:-1].rstrip() + ' class="p-curto">' 
PECA = re.compile(r'(<[^>]+>|\s+|[^<\s]+)')


def _cola_no_trecho(interno):
    pecas = PECA.findall(interno)
    saida, grudado = [], 0
    for i, p in enumerate(pecas):
        if p and not p.strip():
            anterior = next((x for x in reversed(saida)
                             if x.strip() and not x.startswith("<")), "")
            palavra = re.sub(r"[^\w\u00c0-\u00ff]", "", anterior, flags=re.U).lower()
            seguinte = next((pecas[j] for j in range(i + 1, len(pecas))
                             if pecas[j].strip() and not pecas[j].startswith("<")), "")
            if (palavra in PALAVRAS_QUE_COLAM and seguinte
                    and grudado + len(anterior) + len(seguinte) + 1 <= LIMITE_DO_GRUDADO):
                grudado += len(anterior) + 1
                saida.append("&nbsp;")
                continue
            grudado = 0
        saida.append(p)
    return "".join(saida)


def cola_quebra_de_linha(html):
    """Idempotente: rodar de novo no resultado não muda nada."""
    def troca(m):
        if m.group(1):                                   # titulo
            return m.group(1) + _cola_no_trecho(m.group(2)) + m.group(3)
        if m.group(4):                                   # label, sem marcar classe
            return m.group(4) + _cola_no_trecho(m.group(5)) + m.group(6)
        abre, interno, fecha = ((m.group(7), m.group(8), m.group(9)) if m.group(7)
                                else (m.group(10), m.group(11), m.group(12)))
        visivel = SEM_TAG.sub("", interno).replace("&nbsp;", " ").strip()
        if len(visivel) > LIMITE_DO_PARAGRAFO:
            return m.group(0)          # bloco longo fica com pretty, intocado
        return _marca_curto(abre) + _cola_no_trecho(interno) + fecha
    return BLOCO_QUE_COLA.sub(troca, html)


# ---------------------------------------------------------------------------
# UMA FRASE POR LINHA
#
# Medido no navegador, 7 páginas a 1280px: 283 das 491 frases do site quebravam
# no meio. A causa não é a coluna ser estreita. A frase mediana ocupa 497px de
# uma medida de 720px, e 3 de cada 4 frases já cabem inteiras numa linha. Elas
# quebram porque não COMEÇAM no início da linha: começam no resto que a frase
# anterior deixou, e o resto não dá. Alargar a medida de 720 para 920 resolveria
# só mais 13% e daria 122 caracteres por linha, que ninguém lê.
#
# O conserto é dar a cada frase a sua própria linha. Duas decisões importam:
#
# 1. Quem decide ONDE isso vale é o container query, não uma lista de seletores
#    escrita à mão. Medido por faixa de largura, a fatia de frases que cabem
#    numa linha é 10% até 300px, 54% entre 400 e 500, e 77% a partir de 600.
#    Abaixo de 600 metade das frases quebraria do mesmo jeito, e meia correção
#    parece acidente. Daí o corte em 600px.
#
# 2. O corte acontece na SUPERFÍCIE de qualquer elemento, não só de <p> e <li>.
#    A primeira versão só cobria esses dois e deixou ~180 frases de prosa de
#    fora, porque um terço do texto do site mora em <div> e <span> de bloco
#    (.ex-tx, .fp-v, .fl-d, .checagem-como). Cobrir isso com regex é impossível:
#    <div>(.*?)</div> fecha na primeira tag de fechamento, não na certa. Daí a
#    varredura com pilha.
FIM_DE_FRASE = re.compile(r'[.!?…]["\')”]?$')
COMECO_DE_FRASE = re.compile(r'^["“(]?[A-ZÀ-Ü]')
SPAN_FRASE = '<span class="fr">'
FECHA_SPAN = "</span>"

TAG = re.compile(r'<!--.*?-->|<(?P<fecha>/?)(?P<tag>[a-zA-Z][\w-]*)(?P<attrs>[^>]*)>', re.S)
PALAVRA_CRUA = re.compile(r'[^ \t\n\r]+')

VAZIA = {"br", "img", "input", "hr", "wbr", "source", "col", "meta", "link",
         "area", "base", "embed", "param", "track"}
# Dentro destes o conteúdo não é marcação: um "<" ali é texto, e deixar a
# varredura interpretar isso desmonta a pilha.
LITERAL = {"script", "style", "textarea"}
# Elemento que tem filho de bloco nao e folha de texto: ali as "frases" sao os
# proprios filhos, e envolve-los num span nao quer dizer nada.
BLOCO = {"div", "p", "ul", "ol", "li", "section", "article", "table", "tbody",
         "tr", "td", "figure", "figcaption", "blockquote", "header", "footer",
         "nav", "main", "aside", "form", "dl", "dt", "dd", "details", "hr",
         "h1", "h2", "h3", "h4", "h5", "h6"}
# Onde não se corta: o que não é prosa, e o que é inline por natureza. O
# container query só vale em elemento que estabelece bloco, então marcar um
# <strong> não faria nada além de sujar o HTML.
TAG_SEM_CORTE = LITERAL | {
    "pre", "code", "title", "option", "select", "head", "svg", "path",
    "a", "strong", "em", "b", "i", "u", "s", "small", "abbr", "cite", "q",
    "sub", "sup", "mark", "kbd", "samp", "var", "time", "label", "button",
    "summary", "th", "caption",
}
# .prompt-conteudo é a fonte do .md que o participante baixa, conferida byte a
# byte pelo G15. .fonte é o cartão de vídeo, que já tem layout próprio. Vale
# para a ÁRVORE inteira: proibir só o elemento deixou a cola entrar no
# .fonte-cta lá dentro, e o G25 cegou porque o literal que ele procurava tinha
# ganhado um espaço rígido no meio.
CLASSE_SEM_CORTE = {"prompt-conteudo", "fonte", "fonte-txt"}
# Dentro de <svg> um <span> não desenha nada: um corte ali apagaria texto da
# figura na tela sem apagar nada do HTML, que é o pior tipo de defeito.
TAG_SEM_CORTE_NA_ARVORE = {"svg"}


def _classes_de_container(css):
    """Classes que viram flex ou grid: ali o texto solto é item de layout, e
    cortá-lo em blocos põe as frases lado a lado em vez de uma por linha."""
    fora = set()
    for bloco in css.split("}"):                 # fatiar, porque regex de bloco
        sel, chave, corpo = bloco.partition("{")  # trava num CSS deste tamanho
        if not chave or not re.search(r"display\s*:\s*(inline-)?(flex|grid)", corpo):
            continue
        fora.update(re.findall(r"\.([a-zA-Z][\w-]*)", sel))
    return fora


def _classes_de(attrs):
    m = re.search(r'class\s*=\s*"([^"]*)"', attrs)
    return m.group(1).split() if m else []


def _poe_classe(abertura, classe):
    m = re.search(r'(class\s*=\s*")([^"]*)(")', abertura)
    if m:
        nova = (m.group(2) + " " + classe).strip()
        return abertura[:m.start(2)] + nova + abertura[m.end(2):]
    corte = re.match(r"<[a-zA-Z][\w-]*", abertura).end()
    return abertura[:corte] + ' class="' + classe + '"' + abertura[corte:]


def _descortar(html):
    """Tira todo <span class="fr"> com o seu par, e a marca fr-host. É o que faz
    o passo ser idempotente de verdade: ele sempre recalcula do zero."""
    remover, pilha = [], []
    pos = 0
    while True:
        m = TAG.search(html, pos)
        if not m:
            break
        pos = m.end()
        if m.group(0).startswith("<!--"):
            continue
        tag = m.group("tag").lower()
        if tag in LITERAL and not m.group("fecha"):
            f = re.search(r"</\s*%s\s*>" % tag, html[pos:], re.I)
            if f:
                pos += f.end()
            continue
        if tag in VAZIA:
            continue
        if m.group("fecha"):
            fundo = next((k for k in range(len(pilha) - 1, -1, -1)
                          if pilha[k][0] == tag), None)
            if fundo is None:
                continue                       # fechamento sem abertura: ignora
            del pilha[fundo + 1:]              # descarta o que ficou sem fechar
            _, ehFrase, ini = pilha.pop()
            if ehFrase:
                remover.append((m.start(), m.end()))
                remover.append(ini)
        else:
            pilha.append((tag, m.group(0) == SPAN_FRASE, (m.start(), m.end())))
    saida, ult = [], 0
    for a, b in sorted(remover):
        saida.append(html[ult:a])
        ult = b
    saida.append(html[ult:])
    limpo = "".join(saida)
    # tira a marca; se a classe ficar vazia, o atributo inteiro sai
    limpo = re.sub(r'(class\s*=\s*")([^"]*)(")',
                   lambda m: (m.group(1) + " ".join(c for c in m.group(2).split()
                                                    if c != "fr-host") + m.group(3)),
                   limpo)
    limpo = re.sub(r'\s+class\s*=\s*""', "", limpo)
    return limpo


def _cortar(html, fora_de_alcance):
    ins = []

    def onde_vai_o_container(q):
        """container-type:inline-size zera a largura de quem se dimensiona pelo
        conteúdo. Num item de flex isso faz o bloco virar 0px e o texto sair
        uma palavra por linha: aconteceu, e só a medição no navegador pegou.
        Então a marca sobe até o primeiro ancestral de largura definida."""
        abre = q["abre"]
        i = len(pilha) - 1
        while i >= 1 and (pilha[i]["classes"] & fora_de_alcance):
            abre = pilha[i]["abre"]
            i -= 1
        return abre

    def fecha_quadro(q):
        itens = q["itens"]
        cortes = [i for i in range(len(itens) - 1)
                  if FIM_DE_FRASE.search(itens[i]["txt"])
                  and COMECO_DE_FRASE.match(itens[i + 1]["txt"])]
        if q["corta"] and cortes:
            ini = 0
            for fim in [c + 1 for c in cortes] + [len(itens)]:
                # na MESMA posicao, fechar tem de vir antes de abrir: o fim de
                # um trecho e o comeco do seguinte caem no mesmo caractere
                ins.append((itens[ini]["ini"], 1, SPAN_FRASE))
                ins.append((itens[fim - 1]["fim"], 0, FECHA_SPAN))
                ini = fim
            ins.append((None, 2, ("HOST", onde_vai_o_container(q))))

    def texto_do_quadro(q):
        return " ".join(x["txt"] for x in q["itens"])

    raiz = {"tag": None, "itens": [], "corta": False, "abre": (0, 0), "classes": set()}
    pilha = [raiz]
    pos = 0
    while True:
        m = TAG.search(html, pos)
        fim_texto = m.start() if m else len(html)
        if fim_texto > pos:
            for p in PALAVRA_CRUA.finditer(html, pos, fim_texto):
                pilha[-1]["itens"].append({"txt": p.group(0), "ini": p.start(), "fim": p.end()})
        if not m:
            break
        pos = m.end()
        if m.group(0).startswith("<!--"):
            continue
        tag = m.group("tag").lower()
        if tag in LITERAL and not m.group("fecha"):
            f = re.search(r"</\s*%s\s*>" % tag, html[pos:], re.I)
            if f:
                pos += f.end()
            continue
        if tag in VAZIA:
            # <br> é quebra que o autor escolheu à mão: não disputar com ela
            pilha[-1]["corta"] = False
            continue
        if m.group("fecha"):
            fundo = next((k for k in range(len(pilha) - 1, 0, -1)
                          if pilha[k]["tag"] == tag), None)
            if fundo is None:
                continue                       # fechamento sem abertura: ignora
            while len(pilha) > fundo + 1:      # o que ficou sem fechar sai antes
                fecha_quadro(pilha.pop())
            q = pilha.pop()
            fecha_quadro(q)
            if tag in BLOCO:
                pilha[-1]["corta"] = False
            pilha[-1]["itens"].append(
                {"txt": texto_do_quadro(q), "ini": q["abre"][0], "fim": m.end()})
        else:
            classes = _classes_de(m.group("attrs"))
            proibido = (pilha[-1].get("proibido", False)
                        or tag in TAG_SEM_CORTE_NA_ARVORE
                        or bool(set(classes) & CLASSE_SEM_CORTE))
            pilha.append({
                "tag": tag, "itens": [], "abre": (m.start(), m.end()),
                "classes": set(classes),
                "proibido": proibido,
                "corta": (not proibido and tag not in TAG_SEM_CORTE
                          and not (set(classes) & fora_de_alcance)),
            })
    while len(pilha) > 1:
        fecha_quadro(pilha.pop())

    if not ins:
        return html
    vistos, limpos = set(), []
    for p, ordem, o in ins:
        if ordem == 2:
            if o[1] in vistos:
                continue                       # dois filhos, um contêiner só
            vistos.add(o[1])
            p = o[1][0]
        limpos.append((p, ordem, o))
    saida, ult = [], 0
    for p, ordem, o in sorted(limpos, key=lambda x: (x[0], x[1])):
        if ordem == 2:
            a, b = o[1]
            saida.append(html[ult:a])
            saida.append(_poe_classe(html[a:b], "fr-host"))
            ult = b
        else:
            saida.append(html[ult:p])
            saida.append(o)
            ult = p
    saida.append(html[ult:])
    return "".join(saida)


FORA_DE_ALCANCE = _classes_de_container(
    io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.css"),
            encoding="utf-8").read())
ESTILO = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
# cola_quebra_de_linha alcança estes por regex; o resto do texto mora em <div> e
# <span> de bloco, onde regex não fecha na tag certa. Medido: com a cola só
# nestes, sobravam linhas terminando em artigo dentro de .loop-volta-txt e
# .agenda-d, que são justamente prosa larga.
JA_COLADO = {"h1", "h2", "h3", "h4", "label", "p", "li"}


def _cola_em_folhas(html, fora_de_alcance):
    """Cola espaço rígido nas folhas de texto que a regex da cola não alcança."""
    faixas = []
    raiz = {"tag": None, "classes": set(), "corta": False, "filho": False, "ini": 0}
    pilha = [raiz]
    pos = 0
    while True:
        m = TAG.search(html, pos)
        if not m:
            break
        pos = m.end()
        if m.group(0).startswith("<!--"):
            continue
        tag = m.group("tag").lower()
        if tag in LITERAL and not m.group("fecha"):
            f = re.search(r"</\s*%s\s*>" % tag, html[pos:], re.I)
            if f:
                pos += f.end()
            continue
        if tag in VAZIA:
            pilha[-1]["corta"] = False           # <br> é quebra escolhida à mão
            continue
        if m.group("fecha"):
            fundo = next((k for k in range(len(pilha) - 1, 0, -1)
                          if pilha[k]["tag"] == tag), None)
            if fundo is None:
                continue
            del pilha[fundo + 1:]
            q = pilha.pop()
            # só a folha: se tem descendente colável, quem cola é ele, e colar
            # duas vezes na mesma faixa gastaria o limite do trecho grudado
            if q["corta"] and not q["filho"] and q["tag"] not in JA_COLADO:
                interno = html[q["ini"]:m.start()]
                if len(SEM_TAG.sub("", interno).replace("&nbsp;", " ").strip()) \
                        <= LIMITE_DO_PARAGRAFO:
                    faixas.append((q["ini"], m.start()))
                    pilha[-1]["filho"] = True
            elif q["corta"] or q["filho"] or q["proibido"]:
                # "proibido" tambem sobe: colar na faixa inteira do pai levaria
                # espaco rigido para dentro do <svg> e do prompt que o G15 confere
                pilha[-1]["filho"] = True
            continue
        classes = set(_classes_de(m.group("attrs")))
        proibido = (pilha[-1].get("proibido", False)
                    or tag in TAG_SEM_CORTE_NA_ARVORE
                    or bool(classes & CLASSE_SEM_CORTE))
        pilha.append({"tag": tag, "classes": classes, "ini": m.end(), "filho": False,
                      "proibido": proibido,
                      "corta": (not proibido and tag not in TAG_SEM_CORTE
                                and not (classes & fora_de_alcance))})
    if not faixas:
        return html
    saida, ult = [], 0
    for a, b in sorted(faixas):
        saida.append(html[ult:a])
        saida.append(_cola_no_trecho(html[a:b]))
        ult = b
    saida.append(html[ult:])
    return "".join(saida)


def uma_frase_por_linha(html):
    """Sempre recalcula do zero, então rodar de novo devolve o mesmo arquivo."""
    # .folha-pe e outras vivem num <style> dentro do fragmento, não no base.css.
    # Ler só o base.css deixaria de fora metade dos contêineres flex.
    fora = FORA_DE_ALCANCE | _classes_de_container("\n".join(ESTILO.findall(html)))
    return _cortar(_cola_em_folhas(_descortar(html), fora), fora)


def extrai_nav(fragmento):
    """Monta a nav lateral a partir dos <section class="block" id="..."> do fragmento."""
    itens = []
    padrao = re.compile(
        r'<section class="block" id="(?P<id>[^"]+)"[^>]*>\s*'
        r'<div class="block-num">(?P<num>.*?)</div>\s*'
        r'<h2>(?P<h2>.*?)</h2>',
        re.S,
    )
    for m in padrao.finditer(fragmento):
        num = re.sub(r"<[^>]+>", "", m.group("num")).strip()
        titulo = re.sub(r"<[^>]+>", "", m.group("h2")).strip()
        itens.append((m.group("id"), num, titulo))
    return itens


def monta(slug, cfg, fragmento):
    prof = "" if slug == "" else "../"
    itens = extrai_nav(fragmento) if cfg["nav"] else []

    nav_html = ""
    if itens:
        li = "\n".join(
            '      <li class="side-nav-item"><a href="#{i}">'
            '<span class="side-nav-num">{n}</span>{t}</a></li>'.format(
                i=i, n=n.split("·")[0].strip() or n, t=t
            )
            for i, n, t in itens
        )
        nav_html = (
            '  <nav class="side-nav" aria-label="Seções desta página">\n'
            '    <div class="side-nav-label">Nesta página</div>\n'
            '    <ul class="side-nav-list">\n' + li + "\n    </ul>\n  </nav>\n"
        )

    chips = "\n".join(
        '        <span class="chip">{}</span>'.format(c) for c in cfg["chips"]
    )

    crumbs = ""
    if slug:
        crumbs = (
            '      <div class="crumbs"><a href="../">Ideação com AI First</a>'
            " &nbsp;›&nbsp; {}</div>\n".format(cfg["eyebrow"].split("·")[0].strip())
        )

    rodape_nav = ""
    if cfg["anterior"] or cfg["proxima"]:
        a = cfg["anterior"]
        p = cfg["proxima"]
        esq = (
            '<a class="nav-link prev" href="{h}"><span class="nav-link-label">← Anterior</span>'
            '<span class="nav-link-title">{t}</span></a>'.format(h=a[0], t=a[1])
            if a
            else "<span></span>"
        )
        dir_ = (
            '<a class="nav-link next" href="{h}"><span class="nav-link-label">Próxima →</span>'
            '<span class="nav-link-title">{t}</span></a>'.format(h=p[0], t=p[1])
            if p
            else "<span></span>"
        )
        rodape_nav = (
            '      <div class="nav-bottom">\n        {e}\n        {d}\n      </div>\n'.format(
                e=esq, d=dir_
            )
        )

    # Copiar prompt. navigator.clipboard só existe em contexto seguro (https),
    # então em file:// e http:// o ramo alternativo com execCommand assume.
    copiador = ""
    if 'class="prompt-box"' in fragmento:
        copiador = """
<script>
(function(){
  'use strict';
  var aviso = document.createElement('div');
  aviso.className = 'aviso-copia';
  document.body.appendChild(aviso);
  function fala(t){
    aviso.textContent = t;
    aviso.classList.add('aparece');
    setTimeout(function(){ aviso.classList.remove('aparece'); }, 2200);
  }
  function porTextarea(txt){
    var ta = document.createElement('textarea');
    ta.value = txt;
    ta.setAttribute('readonly','');
    ta.style.position = 'fixed';
    ta.style.top = '-1000px';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch(e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }
  Array.prototype.forEach.call(document.querySelectorAll('[data-copia]'), function(btn){
    btn.addEventListener('click', function(){
      var alvo = document.getElementById(btn.getAttribute('data-copia'));
      if(!alvo){ fala('Não achei o texto para copiar'); return; }
      var txt = alvo.textContent;
      if(navigator.clipboard && window.isSecureContext){
        navigator.clipboard.writeText(txt).then(function(){
          fala('Prompt copiado');
        }, function(){
          fala(porTextarea(txt) ? 'Prompt copiado' : 'Selecione e copie na mão');
        });
      } else {
        fala(porTextarea(txt) ? 'Prompt copiado' : 'Selecione e copie na mão');
      }
    });
  });
})();
</script>
"""

    script = ""
    if itens:
        script = """
<script>
(function(){
  'use strict';
  var links = document.querySelectorAll('.side-nav-item a');
  var alvos = Array.prototype.map.call(links, function(a){
    return document.querySelector(a.getAttribute('href'));
  }).filter(Boolean);
  if(!alvos.length) return;
  function atualiza(){
    var y = window.pageYOffset + 130;
    var atual = alvos[0];
    for(var i=0;i<alvos.length;i++){ if(alvos[i].offsetTop <= y) atual = alvos[i]; }
    Array.prototype.forEach.call(links, function(l){
      l.classList.toggle('is-active', l.getAttribute('href') === '#'+atual.id);
    });
  }
  window.addEventListener('scroll', atualiza, {passive:true});
  window.addEventListener('resize', atualiza, {passive:true});
  atualiza();
})();
</script>
"""

    corpo_abre = '<div class="layout">\n' + nav_html + "  <main>\n" if itens else '<main class="wrap" style="padding-top:32px;padding-bottom:80px">\n'
    corpo_fecha = "  </main>\n</div>" if itens else "</main>"

    return """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titulo}</title>
<meta name="description" content="Material do workshop de encerramento da Trilha de Cultura de IA do {cliente}. Facilitação de Rafael Lima.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>

<header class="site-header">
  <div class="site-header-inner">
    <a href="{prof}" class="brand">
      <div class="brand-mark">LS</div>
      <div class="brand-text">
        <span class="brand-title">Ideação com AI First</span>
        <span class="brand-sub">{cliente} · Rafael Lima</span>
      </div>
    </a>
    <div class="header-meta"><span class="chip">4h · presencial</span></div>
  </div>
</header>

{abre}
{crumbs}      <div class="hero">
        <div class="hero-eyebrow">{eyebrow}</div>
        <h1>{h1}</h1>
        <p class="hero-lead">{lead}</p>
        <div class="hero-meta">
{chips}
        </div>
      </div>

{fragmento}
{rodape_nav}{fecha}

<footer class="site-footer">
  <p><strong>{cliente}</strong> · Ideação com AI First · Facilitação de Rafael Lima · IEL Ceará</p>
</footer>
{script}{copiador}
</body>
</html>
""".format(
        titulo=cfg["titulo"],
        cliente=CLIENTE,
        css=CSS.strip(),
        prof=prof if prof else "./",
        abre=corpo_abre,
        crumbs=crumbs,
        eyebrow=cfg["eyebrow"],
        h1=cfg["h1"],
        lead=cfg["lead"],
        chips=chips,
        fragmento=fragmento.strip(),
        rodape_nav=rodape_nav,
        fecha=corpo_fecha,
        script=script,
        copiador=copiador,
    )


def grava_prompts(slug, fragmento):
    """Grava cada .prompt-conteudo como .md ao lado da página.

    O arquivo sai do mesmo texto que a tela mostra: é a garantia de que baixar
    e copiar entregam a mesma coisa. E é o caminho que funciona quando a área
    de transferência do aparelho recusa, que acontece mais no celular do que
    se imagina.
    """
    import html as _html
    saidas = []
    for m in re.finditer(
        r'<div class="prompt-conteudo" id="([^"]+)">(.*?)</div>',
        fragmento, flags=re.S,
    ):
        nome = m.group(1).replace("prompt-", "") + ".md"
        texto = _html.unescape(m.group(2))
        destino = os.path.join(RAIZ, slug, nome) if slug else os.path.join(RAIZ, nome)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        open(destino, "w", encoding="utf-8").write(texto.strip() + "\n")
        saidas.append((os.path.relpath(destino, RAIZ), len(texto)))
    return saidas


def main():
    gerados = []
    for slug, cfg in PAGINAS.items():
        frag_path = os.path.join(RAIZ, "_build", "conteudo", (slug or "index") + ".html")
        if not os.path.exists(frag_path):
            print("  falta o conteúdo: " + frag_path)
            continue
        fragmento = open(frag_path, encoding="utf-8").read()
        html = uma_frase_por_linha(cola_quebra_de_linha(monta(slug, cfg, fragmento)))
        for rel_md, n in grava_prompts(slug, fragmento):
            print("  prompt:  {:45s} {} caracteres".format(rel_md, n))
        destino = os.path.join(RAIZ, slug, "index.html") if slug else os.path.join(RAIZ, "index.html")
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "w", encoding="utf-8") as f:
            f.write(html)
        gerados.append((destino, len(html)))
        print("  gravado: {:<44} {:>7} bytes".format(
            os.path.relpath(destino, RAIZ), len(html)))
    # O canvas não passa pelo molde (é standalone, com JS e sem casca do site),
    # mas os dois passos de texto valem para ele igual: os gates G28 e G29
    # conferem o arquivo publicado, e enquanto isso era trabalho manual toda
    # edição no canvas quebrava os dois.
    canvas = os.path.join(RAIZ, "canvas", "index.html")
    if os.path.exists(canvas):
        cru = open(canvas, encoding="utf-8").read()
        tratado = uma_frase_por_linha(cola_quebra_de_linha(cru))
        if tratado != cru:
            with open(canvas, "w", encoding="utf-8") as f:
                f.write(tratado)
            print("  tratado: {:<44} {:>7} bytes".format("canvas/index.html", len(tratado)))
        gerados.append((canvas, len(tratado)))

    if not gerados:
        sys.exit("nenhuma página gerada")
    print("\n  {} páginas".format(len(gerados)))


if __name__ == "__main__":
    main()
