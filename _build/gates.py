#!/usr/bin/env python3
"""
Gates de auditoria do site do workshop da Longevidade.

Cada gate roda contra todos os .html publicados E é provado contra um defeito
injetado numa cópia em memória. Gate que não acusa o próprio defeito é gate que
não existe, e o script falha por isso, não só por achar problema no site.

Rodar:  python3 _build/gates.py
Saída:  FALHA por gate + exit code. Exit code sozinho nunca é prova: leia a saída.
"""

import os
import re
import sys
import glob

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A capa pode falar de tempo: a agenda é o que foi contratado. As páginas de
# conteúdo são material do participante e não carregam minutagem.
PAGINAS_COM_AGENDA = {"index.html"}


def paginas():
    """Todo .html publicado, com caminho relativo à raiz do site."""
    achados = []
    for p in glob.glob(os.path.join(RAIZ, "**", "*.html"), recursive=True):
        rel = os.path.relpath(p, RAIZ)
        if rel.startswith("_build" + os.sep):
            continue
        achados.append((rel, open(p, encoding="utf-8").read()))
    return sorted(achados)


def linhas_com(texto, padrao, flags=re.I):
    """Devolve (nº da linha, trecho) de cada linha inteira que casa. Nunca recorta
    antes de filtrar: recortar antes é como o gate de 'pede nome' deu falso
    positivo em cima de 'Não escreva seu nome'."""
    saida = []
    for n, linha in enumerate(texto.split("\n"), 1):
        if re.search(padrao, linha, flags):
            saida.append((n, linha.strip()[:150]))
    return saida


# Só tags de bloco. strong, em, span e a são inline: quebrar neles partiria a
# frase ao meio e faria o gate de "a fonte está na mesma frase" acusar sozinho.
BLOCOS = ("p", "div", "li", "h1", "h2", "h3", "h4", "td", "th", "tr",
          "section", "summary")


def texto_visivel(html):
    """Só o que o participante lê: sem <style>, <script>, comentários e tags.

    Preserva a quebra entre blocos. Colapsar tudo numa linha só faz o gate
    perder a noção de 'na mesma frase' e devolve a página inteira como
    mensagem de erro, que foi como o G11 nasceu cego.
    """
    s = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.S)
    s = re.sub(r"<script[^>]*>.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    # Colapsa ANTES de marcar bloco: quebra de linha no arquivo-fonte não é
    # quebra na tela, e tratar as duas como iguais partia a frase da Capgemini.
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"</(" + "|".join(BLOCOS) + r")>", "\n", s)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    linhas = [re.sub(r"[ \t]+", " ", l).strip() for l in s.split("\n")]
    return "\n".join(l for l in linhas if l)


# ----------------------------------------------------------------- os gates

def g1_travessao(rel, html):
    """Travessão é proibido em todo material do Rafael."""
    falhas = []
    for n, l in linhas_com(texto_visivel(html), r"—"):
        falhas.append("linha com travessão: " + l)
    return falhas


VOCAB_INTERNO = [
    r"\bonda \d", r"\bgate\b", r"\bhandoff\b", r"\bspec\b", r"\bcanonical\b",
    r"\bsubsistema\b", r"\bfio[s]? em aberto\b", r"\bsubagente\b",
    r"\bclaude code\b", r"\bPCTFL\b", r"\bPOC-1\b", r"\bcommit\b",
    r"\bprompt de sistema\b", r"\bmarkdown\b", r"\bfrontmatter\b",
    # projetos e pessoas de outras frentes do Rafael
    r"\bmaria pitanga\b", r"\bmallory\b", r"\bpouchain\b", r"\bbumpai\b",
    r"\birede\b", r"\btracemat\b", r"\bporanga\b", r"\bcirilo\b",
    r"\bclineu\b", r"\bsamuel\b", r"\baurora\b",
]


def g2_vocabulario_interno(rel, html):
    """Vocabulário interno e nome de outra frente não vão para a tela."""
    vis = texto_visivel(html)
    falhas = []
    for termo in VOCAB_INTERNO:
        for n, l in linhas_com(vis, termo):
            falhas.append("vocabulário interno {}: {}".format(termo, l))
    return falhas


# Premissa que o cliente deu. Devolver isso ocupa espaço sem informar.
PREMISSA_DO_CLIENTE = [
    r"banco de ideias", r"\broadmap\b", r"\bdiretoria\b",
    r"vocês (já )?constru", r"vocês (já )?fizeram", r"que vocês (já )?levantaram",
    r"plataforma de gestão integrada", r"\bgemini\b",
    r"as prioridades que vocês", r"os setores que vocês",
    r"o diagnóstico que vocês", r"as ferramentas que vocês",
    # nomes de dentro do cliente e dos instrutores anteriores
    r"\bizadora\b", r"\bisaac\b", r"\balef\b", r"\bdiego\b",
]


def g3_premissa_devolvida(rel, html):
    """Não devolver ao cliente premissa que ele mesmo deu."""
    vis = texto_visivel(html)
    falhas = []
    for termo in PREMISSA_DO_CLIENTE:
        for n, l in linhas_com(vis, termo):
            falhas.append("premissa devolvida {}: {}".format(termo, l))
    return falhas


def g4_classe_sem_css(rel, html):
    """Toda classe usada no HTML tem regra no CSS da própria página."""
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S))
    definidas = set(re.findall(r"\.([A-Za-z][\w-]*)", css))
    usadas = set()
    for attr in re.findall(r'class="([^"]+)"', html):
        for c in attr.split():
            usadas.add(c)
    orfas = sorted(usadas - definidas)
    return ["classe sem CSS: ." + c for c in orfas]


def g5_gabarito_fechado(rel, html):
    """A resposta do caso nunca nasce aberta: quebraria o exercício de 3 passos."""
    falhas = []
    for m in re.finditer(r"<details[^>]*>", html):
        tag = m.group(0)
        if "gabarito" in tag and re.search(r"\bopen\b", tag):
            falhas.append("gabarito nasce aberto: " + tag[:100])
    return falhas


def g6_links_resolvem(rel, html):
    """Todo link relativo aponta para arquivo que existe no disco."""
    base = os.path.dirname(os.path.join(RAIZ, rel))
    falhas = []
    for href in re.findall(r'href="([^"#]+)"', html):
        if href.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        alvo = os.path.normpath(os.path.join(base, href))
        if os.path.isdir(alvo):
            alvo = os.path.join(alvo, "index.html")
        if not os.path.exists(alvo):
            falhas.append("link quebrado: {} (procurei em {})".format(
                href, os.path.relpath(alvo, RAIZ)))
    return falhas


def g7_nav_bate_com_secoes(rel, html):
    """A nav lateral aponta 1:1 para as seções que existem, sem sobra dos dois lados."""
    nav = re.findall(r'<li class="side-nav-item"><a href="#([^"]+)"', html)
    secoes = re.findall(r'<section class="block" id="([^"]+)"', html)
    if not nav:
        return []
    falhas = []
    for i in nav:
        if i not in secoes:
            falhas.append("nav aponta para seção inexistente: #" + i)
    for s in secoes:
        if s not in nav:
            falhas.append("seção fora da nav: #" + s)
    return falhas


DIRECAO_DE_CENA = [
    r"pergunte à sala", r"pergunte para a sala", r"a sala responde",
    r"espere o silêncio", r"aguarde o silêncio", r"plano b",
    r"o que apontar", r"roteiro de palco", r"dê um tempo",
    r"circule pela sala", r"anote no quadro", r"projete a tela",
]


def g8_direcao_de_cena(rel, html):
    """Página é do participante, não roteiro do instrutor."""
    vis = texto_visivel(html)
    falhas = []
    for termo in DIRECAO_DE_CENA:
        for n, l in linhas_com(vis, termo):
            falhas.append("direção de cena {}: {}".format(termo, l))
    return falhas


def g9_minutagem_fora_da_capa(rel, html):
    """Minutagem é controle de condução. Só a capa carrega, porque lá é o contrato."""
    if rel in PAGINAS_COM_AGENDA:
        return []
    vis = texto_visivel(html)
    falhas = []
    # A regra protegida é "quanto tempo dura o bloco da aula", que é condução.
    # A duração de um MATERIAL (uma gravação de 48 minutos) é fato do insumo, do
    # mesmo tipo que "sete páginas", e não diz nada sobre como conduzir o dia.
    material = re.compile(
        r"(transcri\u00e7\u00e3o|entrevista|grava\u00e7\u00e3o|\u00e1udio|v\u00eddeo|convers[ao])",
        re.I,
    )
    for padrao in [r"\d+\s*min\b", r"\b\d+h\d{2}\b", r"\b\d+\s*minutos\b"]:
        for n, l in linhas_com(vis, padrao):
            if material.search(l):
                continue
            falhas.append("minutagem fora da capa: " + l)
    return falhas


def g13_botao_copia_tem_alvo(rel, html):
    """Botão de copiar aponta para um id que existe na mesma página.

    Se o id não bate, o botão não faz nada e ninguém percebe: a página abre,
    o botão aparece, e a falha só existe no clique.
    """
    falhas = []
    ids = set(re.findall(r'id="([^"]+)"', html))
    for alvo in re.findall(r'data-copia="([^"]+)"', html):
        if alvo not in ids:
            falhas.append("botão de copiar aponta para id inexistente: " + alvo)
    return falhas


def g14_cem_pontos_batem_com_o_texto(rel, html):
    """A figura dos cem quadrados tem que contar a mesma coisa que a frase.

    A figura é a prova visual do número. Se a frase diz 13 e a figura acende
    outro tanto, a página mente em dois lugares ao mesmo tempo.
    """
    if 'class="cem-grade"' not in html:
        return []
    falhas = []
    grade = re.search(r'<div class="cem-grade"[^>]*>(.*?)</div>', html, flags=re.S)
    if not grade:
        return ["figura dos cem pontos sem grade legível"]
    corpo = grade.group(1)
    acesos = len(re.findall(r'class="cem-p aceso"', corpo))
    total = len(re.findall(r'class="cem-p', corpo))
    if total != 100:
        falhas.append("a figura tem {} quadrados, e deveria ter 100".format(total))
    vis = texto_visivel(html)
    declarado = re.search(r"(\d+)%\s*dos projetos", vis)
    if declarado and int(declarado.group(1)) != acesos:
        falhas.append(
            "a frase diz {}% e a figura acende {} quadrados".format(
                declarado.group(1), acesos))
    if not declarado:
        falhas.append("figura dos cem pontos sem o número declarado no texto")
    return falhas


def g15_prompt_baixado_bate_com_a_tela(rel, html):
    """O .md que a pessoa baixa é igual ao prompt que ela lê na tela.

    Baixar e copiar têm que entregar a mesma coisa. Se divergirem, quem baixou
    trabalha com uma versão que ninguém revisou.
    """
    import html as _html
    falhas = []
    base = os.path.dirname(os.path.join(RAIZ, rel))
    for m in re.finditer(
        r'<div class="prompt-conteudo" id="([^"]+)">(.*?)</div>', html, flags=re.S
    ):
        nome = m.group(1).replace("prompt-", "") + ".md"
        caminho = os.path.join(base, nome)
        if not os.path.exists(caminho):
            falhas.append("prompt sem arquivo para baixar: " + nome)
            continue
        na_tela = _html.unescape(m.group(2)).strip()
        no_arquivo = open(caminho, encoding="utf-8").read().strip()
        if na_tela != no_arquivo:
            falhas.append(
                "o {} baixado difere do que está na tela ({} contra {} caracteres)".format(
                    nome, len(no_arquivo), len(na_tela)))
    return falhas


def g16_campos_do_canvas_com_piso(rel, html):
    """As caixas lado a lado do canvas têm piso de altura.

    Sem o piso o seletor sai 3px mais baixo que o campo de texto ao lado, porque
    o navegador dá ao seletor uma altura interna própria. Medido: 47 e 44 antes,
    47 e 47 depois. Rafael apontou isso olhando a tela, antes de qualquer gate.
    """
    if "canvas" not in rel:
        return []
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S))
    if not re.search(r"input\.txt\s*,\s*select\.txt\s*\{[^}]*min-height", css):
        return ["campos do canvas sem piso de altura: as caixas lado a lado saem diferentes"]
    return []


# Os cinco pilares são vocabulário fechado: a régua do celular, a folha impressa
# e a proposta aprovada usam exatamente estes rótulos.
PILARES = [
    "O que não vira registro não existe",
    "Resultado ruim é falta de contexto, não de capacidade",
    "Quebrar em fases e conferir entre elas",
    "Toda correção vira regra",
    "Nada começa sem quatro campos preenchidos",
]


# Onde o rótulo de um pilar é AFIRMADO. Perguntar "existe na página?" deixava
# passar a paráfrase enquanto sobrasse uma cópia certa em qualquer outro canto:
# quando a capa ganhou o ciclo, o rótulo passou a aparecer duas vezes e o gate
# parou de acusar o defeito injetado. Presença não é conferência.
ROTULOS_DE_PILAR = ("pilar-t", "loop-no-t", "fp-t")


def g10_pilares_literais(rel, html):
    """Cada lugar que nomeia um pilar usa o rótulo canônico, sem paráfrase."""
    if rel not in ("index.html", "pilares/index.html"):
        return []
    falhas = []
    achados = []
    for classe in ROTULOS_DE_PILAR:
        for m in re.finditer(
            r'<div class="' + classe + r'">(.*?)</div>', html, flags=re.S
        ):
            t = re.sub(r"<[^>]+>", "", m.group(1))
            t = re.sub(r"\s+", " ", t).strip()
            achados.append((classe, t))

    for classe, t in achados:
        if t not in PILARES:
            falhas.append(
                "rótulo de pilar reescrito em .{}: {!r}".format(classe, t[:80]))

    # e os cinco continuam tendo que existir na página
    vis = texto_visivel(html)
    for pilar in PILARES:
        if pilar not in vis:
            falhas.append("pilar ausente: " + pilar)
    return falhas


def g11_capgemini_com_fonte(rel, html):
    """Número de terceiro entra com a fonte colada, nunca solto."""
    vis = texto_visivel(html)
    falhas = []
    for n, l in linhas_com(vis, r"\b13%|\b87 de cada"):
        if not re.search(r"capgemini", l, re.I):
            falhas.append("número de terceiro sem a fonte na mesma frase: " + l)
    return falhas


def g12_contagem_dos_pilares(rel, html):
    """Onde o texto diz cinco pilares, existem cinco blocos de pilar."""
    if rel != "index.html":
        return []
    falhas = []
    # A capa mostra os pilares como ciclo. Os blocos soltos saíram porque
    # repetiam o que o ciclo já diz, então quem conta agora são as etapas.
    ciclo = len(re.findall(r'<div class="loop-no">', html))
    if ciclo != 5:
        falhas.append("a capa diz cinco pilares e o ciclo desenha {} etapas".format(ciclo))
    # cada etapa aponta onde o pilar é provado: sem isso a capa deixa de ser índice
    selos = len(re.findall(r'<span class="loop-no-onde">', html))
    if selos != ciclo:
        falhas.append("{} etapas no ciclo e {} selos de onde é provado".format(ciclo, selos))
    return falhas


# id, o que confere, função, defeito que prova o gate, onde injetar o defeito

# ---------------------------------------------------------------- G17
# Caractere de outro alfabeto que renderiza parecido com o latino. Eu escrevi
# "потencial" com dois caracteres cirílicos e o texto passou por cima de todos
# os outros gates: na tela ele é indistinguível. Só a checagem do alfabeto pega.
NAO_LATINO = re.compile(r"[\u0400-\u04FF\u0370-\u03FF\u0500-\u052F]")


def g17_alfabeto(rel, html):
    falhas = []
    for n, l in linhas_com(texto_visivel(html), NAO_LATINO.pattern, flags=0):
        achados = NAO_LATINO.findall(l)
        falhas.append("caractere de outro alfabeto ({}) na linha {}: {}".format(
            "".join(sorted(set(achados))), n, l[:90]))
    return falhas


# ---------------------------------------------------------------- G18
# Os sete números "X de 22" vêm do diagnóstico prévio que o cliente respondeu.
# Se a planilha ganhar respostas, a página mente e ninguém percebe: o insumo é
# a fonte da verdade, e quem descreve o insumo tem que ser conferido contra ele.
PLANILHA = os.path.join(
    os.path.dirname(RAIZ), "2-insumos-do-cliente", "briefing",
    "Diagnóstico prévio — IA no Back Office (respostas).xlsx")

OPCOES_DIAGNOSTICO = [
    "Organizar e resumir grandes volumes de informação",
    "Interpretar documentos, contratos e legislações",
    "Apoiar decisões com mais agilidade e embasamento",
    "Montar relatórios e apresentações para gestores",
    "Analisar dados, planilhas e indicadores de resultado",
    "Fazer cálculos e simular cenários (custos, impostos, margens)",
    "Automatizar tarefas repetitivas e rotinas administrativas",
]


def _contagem_real():
    """Lê a planilha do cliente e devolve {opção: quantas marcaram}, e o total.
    Devolve None se a planilha não estiver acessível: gate que depende de insumo
    externo tem que dizer que não conferiu, e não passar calado."""
    try:
        import openpyxl
    except ImportError:
        return None
    if not os.path.exists(PLANILHA):
        return None
    w = openpyxl.load_workbook(PLANILHA, data_only=True)
    s = w[w.sheetnames[0]]
    linhas = [r for r in list(s.iter_rows(values_only=True))[1:] if r[0]]
    cont = {}
    for o in OPCOES_DIAGNOSTICO:
        cont[o] = sum(1 for r in linhas if o in str(r[3] or ""))
    return cont, len(linhas)


def g18_numeros_do_diagnostico(rel, html):
    if rel != "ai-first/index.html":
        return []
    real = _contagem_real()
    if real is None:
        return ["não foi possível conferir os números contra a planilha do cliente"]
    cont, total = real
    falhas = []
    vis = texto_visivel(html)

    # premissa: a página afirma o total de respondentes por extenso
    if "Vinte e duas pessoas" not in vis and str(total) not in vis:
        falhas.append("a página não diz quantas pessoas responderam o diagnóstico")

    # cada rótulo "N de M" tem que bater com a contagem real daquela atividade
    for m in re.finditer(r'<span class="ex-area">(\d+) de (\d+)</span>\s*'
                         r'<span class="ex-t">([^<]+)</span>', html):
        n, m_tot, titulo = int(m.group(1)), int(m.group(2)), m.group(3).strip()
        if m_tot != total:
            falhas.append("{!r} diz de {}, e a planilha tem {} respostas".format(
                titulo, m_tot, total))
        casada = [o for o in OPCOES_DIAGNOSTICO if o.startswith(titulo[:28])]
        if not casada:
            falhas.append("atividade que não existe no diagnóstico: " + titulo)
            continue
        if cont[casada[0]] != n:
            falhas.append("{!r} diz {}, e a planilha conta {}".format(
                titulo, n, cont[casada[0]]))
    return falhas


# ---------------------------------------------------------------- G19
# A régua mede a mesma coisa nas duas pontas. Se a abertura e o fechamento
# divergirem em número de alternativas ou no texto delas, a comparação de
# antes e depois compara coisas diferentes e a demonstração ao vivo mente.
def g19_regua_simetrica(rel, html):
    if rel != "canvas/index.html":
        return []
    falhas = []

    def alts(nome):
        return re.findall(
            r'<input type="radio" name="' + nome + r'" value="(\d+)"><span>([^<]*)</span>',
            html)

    for i in range(1, 6):
        a, f = alts("a%d" % i), alts("f%d" % i)
        if len(a) != 3:
            falhas.append("pergunta a{} tem {} alternativas, e a régua é de 3".format(i, len(a)))
        if len(f) != 3:
            falhas.append("pergunta f{} tem {} alternativas, e a régua é de 3".format(i, len(f)))
        if [t for _, t in a] != [t for _, t in f]:
            falhas.append("a pergunta {} tem texto diferente na abertura e no fechamento".format(i))
        if [v for v, _ in a] != ["1", "2", "3"]:
            falhas.append("os valores de a{} não são 1,2,3: {}".format(i, [v for v, _ in a]))
    return falhas


# ---------------------------------------------------------------- G20
# O passo a passo herdado do outro workshop só acrescenta alguma coisa se cada
# passo disser QUEM faz. Passo sem ator vira lista comum, e o participante lê
# sem saber se aquilo é trabalho dele ou da máquina.
def g20_passo_tem_ator(rel, html):
    falhas = []
    for m in re.finditer(r'<div class="fl">(.*?)</div>\s*</div>', html, flags=re.S):
        bloco = m.group(1)
        if 'class="fl-ator' not in bloco:
            t = re.search(r'<div class="fl-t">([^<]*)', bloco)
            falhas.append("passo sem ator nomeado: " + (t.group(1)[:70] if t else "?"))
    return falhas


# ---------------------------------------------------------------- G21
# A legenda da figura afirma que as caixas iniciais dos dois loops são iguais,
# e é essa igualdade que faz o argumento: o que muda é só a volta. Se alguém
# editar um lado, a legenda passa a mentir sobre a própria figura.
def g21_loops_comecam_igual(rel, html):
    if rel != "index.html":
        return []
    # Fatiar por posição, e não por regex com .*?: "lp-rot" também começa com
    # "lp", então o não-guloso fechava o bloco na primeira linha e devolvia
    # zero etapas num HTML correto.
    ini_aberto = html.find('<div class="lp">')
    ini_fechado = html.find('<div class="lp fechado">')
    fim = html.find('<p class="fig-leg">', ini_fechado if ini_fechado > 0 else 0)
    if ini_aberto < 0 or ini_fechado < 0 or fim < 0:
        return ["não achei os dois loops desenhados na capa"]
    if not (ini_aberto < ini_fechado < fim):
        return ["os dois loops estão fora de ordem na capa"]

    def etapas(t):
        return re.findall(r'<span class="lp-et">([^<]+)</span>', t)

    aberto = etapas(html[ini_aberto:ini_fechado])
    fechado = etapas(html[ini_fechado:fim])
    if len(aberto) != 3:
        return ["o loop aberto tem {} etapas, e a legenda fala de três".format(len(aberto))]
    if fechado[:3] != aberto:
        return ["as três primeiras etapas dos dois loops divergem: {} contra {}".format(
            aberto, fechado[:3])]
    if len(fechado) <= len(aberto):
        return ["o loop fechado não tem etapa a mais que o aberto"]
    return []


# ---------------------------------------------------------------- G22
# A folha em papel e a régua da tela medem a mesma coisa, e a demonstração ao
# vivo compara as duas na mesma planilha. Se alguém mexer numa e não na outra,
# a comparação passa a somar coisas diferentes sem nenhum erro aparecer.
def g22_papel_bate_com_a_tela(rel, html):
    if rel != "papel/index.html":
        return []
    canvas = os.path.join(RAIZ, "canvas", "index.html")
    if not os.path.exists(canvas):
        return ["não achei a régua da tela para comparar com o papel"]
    c = open(canvas, encoding="utf-8").read()

    da_tela = []
    for i in range(1, 6):
        alts = re.findall(
            r'<input type="radio" name="a%d" value="\d"><span>([^<]+)</span>' % i, c)
        rot = re.findall(r'class="item-t">([^<]+)</p>', c)
        da_tela.append(alts)
    if any(len(a) != 3 for a in da_tela):
        return ["a régua da tela não tem três alternativas em toda pergunta"]

    do_papel = []
    for m in re.finditer(r'<div class="pl-ops">(.*?)</div>', html, flags=re.S):
        do_papel.append(re.findall(r'<span class="pl-tx">([^<]+)</span>', m.group(1)))

    falhas = []
    if len(do_papel) != 10:
        falhas.append("o papel tem {} blocos de pergunta, e a régua tem cinco em cada ponta".format(
            len(do_papel)))
        return falhas
    import html as _h
    for i in range(5):
        tela = [t.strip() for t in da_tela[i]]
        for ponta, bloco in (("abertura", do_papel[i]), ("fechamento", do_papel[i + 5])):
            papel = [_h.unescape(t).strip() for t in bloco]
            if papel != tela:
                falhas.append("pergunta {} na {} do papel diverge da tela: {} contra {}".format(
                    i + 1, ponta, papel, tela))
    # o teto impresso tem que bater com três alternativas e cinco perguntas
    vis = texto_visivel(html)
    if "de 5 a 15" not in vis:
        falhas.append("o papel não diz a faixa do total, ou ela não é de 5 a 15")
    return falhas


# ---------------------------------------------------------------- G23
# A numeração das seções virou "04, 05, 06, 04" quando duas seções novas
# entraram no meio com rótulo de texto. O leitor usa esses números para se
# localizar na navegação lateral, e dois "04" na mesma página quebram isso.
# O G7 não pega: para ele a nav e as seções continuavam batendo uma a uma.
def g23_numeracao_das_secoes(rel, html):
    rotulos = re.findall(r'<div class="block-num">([^<]*)</div>', html)
    numerados = [r for r in rotulos if re.match(r"^\d+\s*·", r.strip())]
    if not numerados:
        return []          # página de rótulo textual, como a capa
    if len(numerados) != len(rotulos):
        return ["a página mistura seção numerada com seção sem número: {}".format(
            [r for r in rotulos if r not in numerados])]
    nums = [int(re.match(r"^(\d+)", r.strip()).group(1)) for r in numerados]
    falhas = []
    vistos = set()
    for n in nums:
        if n in vistos:
            falhas.append("número de seção repetido: {:02d} ({})".format(n, nums))
        vistos.add(n)
    if nums != list(range(1, len(nums) + 1)):
        falhas.append("a numeração das seções não é sequencial: {}".format(nums))
    return falhas


# ---------------------------------------------------------------- G24
# A página do papel afirma quantas folhas saem, em dois lugares: o chip do
# topo e a caixa "para imprimir". Quando a régua virou frente e verso, o chip
# continuou dizendo duas. Número que a página afirma sobre ela mesma é
# conteúdo, e conteúdo tem que bater com o que ela tem.
NUMERO_POR_EXTENSO = {"uma": 1, "duas": 2, "três": 3, "quatro": 4, "cinco": 5}


def g24_folhas_declaradas(rel, html):
    if rel not in ("papel/index.html", "pilares/index.html"):
        return []
    reais = len(re.findall(r'<div class="folha">', html))
    if not reais:
        return ["a página não tem nenhuma folha"]
    vis = texto_visivel(html)
    falhas, achou = [], 0
    padrao = r"\b(uma|duas|três|quatro|cinco)\s+(?:folhas?|páginas?)\s*A4"
    for m in re.finditer(padrao, vis, re.I):
        achou += 1
        dito = NUMERO_POR_EXTENSO[m.group(1).lower()]
        if dito != reais:
            falhas.append("a página diz {} folha(s) A4 e tem {}".format(dito, reais))
    if not achou:
        falhas.append("a página imprimível não declara quantas folhas A4 saem")
    return falhas


GATES = [
    ("G1", "travessão", g1_travessao,
     lambda h: h.replace("<h2>", "<h2>defeito — injetado ", 1), None),
    ("G2", "vocabulário interno na tela", g2_vocabulario_interno,
     lambda h: h.replace("<h2>", "<h2>a onda 3 do handoff ", 1), None),
    ("G3", "premissa do cliente devolvida", g3_premissa_devolvida,
     lambda h: h.replace("<h2>", "<h2>como o banco de ideias que vocês construíram ", 1), None),
    ("G4", "classe sem CSS", g4_classe_sem_css,
     lambda h: h.replace('class="card', 'class="classe-inventada card', 1), None),
    ("G5", "gabarito nasce fechado", g5_gabarito_fechado,
     lambda h: h.replace('<details class="gabarito">', '<details class="gabarito" open>', 1),
     "caso-1/index.html"),
    ("G6", "links resolvem", g6_links_resolvem,
     lambda h: h.replace('href="./canvas/"', 'href="./pagina-que-nao-existe/"', 1),
     "index.html"),
    ("G7", "nav bate com as seções", g7_nav_bate_com_secoes,
     lambda h: h.replace('<section class="block" id="s1"', '<section class="block" id="s1-renomeada"', 1),
     "caso-1/index.html"),
    ("G8", "direção de cena", g8_direcao_de_cena,
     lambda h: h.replace("<h2>", "<h2>pergunte à sala e espere o silêncio ", 1), None),
    ("G9", "minutagem fora da capa", g9_minutagem_fora_da_capa,
     lambda h: h.replace("<h2>", "<h2>bloco de 15 min ", 1), "caso-1/index.html"),
    ("G10", "pilares com o rótulo canônico", g10_pilares_literais,
     lambda h: h.replace("Toda correção vira regra", "Correções viram regras", 1),
     "index.html"),
    ("G11", "número de terceiro com a fonte", g11_capgemini_com_fonte,
     lambda h: h.replace("Segundo pesquisa da Capgemini, <strong>13%", "<strong>13%", 1),
     "ficha/index.html"),
    ("G16", "as caixas do canvas têm piso", g16_campos_do_canvas_com_piso,
     lambda h: h.replace("input.txt, select.txt { min-height: 47px; }", "", 1),
     "canvas/index.html"),
    ("G15", "o prompt baixado bate com a tela", g15_prompt_baixado_bate_com_a_tela,
     lambda h: h.replace("# PAPEL", "# PAPEL ALTERADO", 1), "caso-1/index.html"),
    ("G13", "botão de copiar tem alvo", g13_botao_copia_tem_alvo,
     lambda h: h.replace('data-copia="prompt-caso-1"', 'data-copia="prompt-sumiu"', 1),
     "caso-1/index.html"),
    ("G14", "a figura dos cem bate com o texto", g14_cem_pontos_batem_com_o_texto,
     lambda h: h.replace('<span class="cem-p aceso"></span>', '<span class="cem-p"></span>', 1),
     "ficha/index.html"),
    ("G17", "alfabeto latino na tela", g17_alfabeto,
     lambda h: h.replace("potencial", "\u043fotencial", 1),
     "ai-first/index.html"),
    ("G18", "os números batem com o diagnóstico", g18_numeros_do_diagnostico,
     lambda h: h.replace('<span class="ex-area">15 de 22</span>',
                         '<span class="ex-area">19 de 22</span>', 1),
     "ai-first/index.html"),
    ("G19", "a régua é simétrica e de três", g19_regua_simetrica,
     lambda h: h.replace('<input type="radio" name="f1" value="3"><span>Fica onde outra pessoa acha sozinha.</span>',
                         '<input type="radio" name="f1" value="3"><span>Fica registrado em algum lugar.</span>', 1),
     "canvas/index.html"),
    ("G20", "todo passo diz quem faz", g20_passo_tem_ator,
     lambda h: h.replace('<span class="fl-ator pessoa">Ryan</span>', '<span class="fl-nada">Ryan</span>', 1),
     "ai-first/index.html"),
    ("G21", "os dois loops começam iguais", g21_loops_comecam_igual,
     lambda h: h.replace('<span class="lp-et">Alguém executa</span>\n              <span class="lp-seta"></span>\n              <span class="lp-et">Entrega</span>\n              <span class="lp-seta"></span>\n              <span class="lp-et">Mede o que saiu</span>',
                         '<span class="lp-et">Alguem executa</span>\n              <span class="lp-seta"></span>\n              <span class="lp-et">Entrega</span>\n              <span class="lp-seta"></span>\n              <span class="lp-et">Mede o que saiu</span>', 1),
     "index.html"),
    ("G22", "o papel bate com a régua da tela", g22_papel_bate_com_a_tela,
     lambda h: h.replace('<span class="pl-tx">Fica na minha cabeça.</span>',
                         '<span class="pl-tx">Fica só na minha cabeça.</span>', 1),
     "papel/index.html"),
    ("G23", "as seções são numeradas em ordem", g23_numeracao_das_secoes,
     lambda h: h.replace('<div class="block-num">07 · O limite</div>',
                         '<div class="block-num">04 · O limite</div>', 1),
     "ai-first/index.html"),
    ("G24", "as folhas declaradas batem", g24_folhas_declaradas,
     lambda h: h.replace("Três páginas A4", "Duas páginas A4", 1),
     "papel/index.html"),
    ("G12", "contagem dos pilares", g12_contagem_dos_pilares,
     lambda h: h.replace('<div class="loop-no">', '<div class="loop-no-removido">', 1),
     "index.html"),
]


def main():
    docs = paginas()
    if not docs:
        sys.exit("nenhuma página encontrada em " + RAIZ)

    print("Auditoria do site · {} páginas\n".format(len(docs)))
    print("  " + " · ".join(rel for rel, _ in docs) + "\n")

    total_falhas = 0
    total_checagens = 0
    gates_cegos = []

    for gid, nome, fn, defeito, alvo_defeito in GATES:
        falhas = []
        for rel, html in docs:
            total_checagens += 1
            for f in fn(rel, html):
                falhas.append("{}: {}".format(rel, f))

        # calibração: o gate acusa o próprio defeito?
        alvo = alvo_defeito or docs[0][0]
        html_alvo = dict(docs).get(alvo)
        if html_alvo is None:
            gates_cegos.append("{} · alvo de calibração não existe: {}".format(gid, alvo))
            acusou = False
        else:
            sujo = defeito(html_alvo)
            if sujo == html_alvo:
                gates_cegos.append("{} · o defeito não mudou nada em {}".format(gid, alvo))
                acusou = False
            else:
                acusou = len(fn(alvo, sujo)) > len(fn(alvo, html_alvo))
        if not acusou and html_alvo is not None and dict(docs).get(alvo) is not None:
            if "{} ·".format(gid) not in " ".join(gates_cegos):
                gates_cegos.append("{} · não acusou o defeito injetado em {}".format(gid, alvo))

        marca = "FALHA " if falhas else ("CEGO  " if not acusou else "ok    ")
        print("{} {:<4} {:<38} {} achado(s) · calibrado: {}".format(
            marca, gid, nome, len(falhas), "sim" if acusou else "NÃO"))
        for f in falhas[:12]:
            print("        " + f)
        if len(falhas) > 12:
            print("        ... e mais {}".format(len(falhas) - 12))
        total_falhas += len(falhas)

    print("\n{} checagens · {} achados".format(total_checagens, total_falhas))

    if gates_cegos:
        print("\nGATES QUE NÃO SE PROVARAM (não valem como verificação):")
        for g in gates_cegos:
            print("  " + g)

    if total_falhas or gates_cegos:
        print("\nRESULTADO: FALHA")
        sys.exit(1)
    print("\nRESULTADO: passou")


if __name__ == "__main__":
    main()
