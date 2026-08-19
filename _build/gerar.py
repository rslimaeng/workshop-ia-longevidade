#!/usr/bin/env python3
"""
Gerador das páginas do site do workshop da Longevidade.

O conteúdo de cada página vive em _build/conteudo/<slug>.html como fragmento
(só as <section class="block">). Este script monta o shell: <head>, tokens de
CSS, header, nav lateral com scroll-spy, hero, rodapé e a navegação de pé.

Rodar:  python3 _build/gerar.py
"""

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
    "papel": dict(
        titulo="A régua e a ficha em papel · Ideação com AI First",
        eyebrow="Se a internet falhar",
        h1="A régua e a ficha em papel",
        lead="As folhas para imprimir e distribuir. Servem quando o celular não "
             "ajuda, e servem para quem prefere caneta.",
        chips=["Imprimível", "Três páginas A4"],
        nav=False,
        anterior=("../pilares/", "Os cinco pilares em uma folha"),
        proxima=None,
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
        proxima=("../papel/", "A régua e a ficha em papel"),
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
BLOCO_QUE_COLA = re.compile(
    r'(<h[1-4]\b[^>]*>)(.*?)(</h[1-4]>)'
    r'|(<label\b[^>]*>)(.*?)(</label>)'
    r'|(<p\b[^>]*>)(.*?)(</p>)',
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
        interno = m.group(8)                             # paragrafo
        visivel = SEM_TAG.sub("", interno).replace("&nbsp;", " ").strip()
        if len(visivel) > LIMITE_DO_PARAGRAFO:
            return m.group(0)          # paragrafo longo fica com pretty, intocado
        return _marca_curto(m.group(7)) + _cola_no_trecho(interno) + m.group(9)
    return BLOCO_QUE_COLA.sub(troca, html)


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
        html = cola_quebra_de_linha(monta(slug, cfg, fragmento))
        for rel_md, n in grava_prompts(slug, fragmento):
            print("  prompt:  {:45s} {} caracteres".format(rel_md, n))
        destino = os.path.join(RAIZ, slug, "index.html") if slug else os.path.join(RAIZ, "index.html")
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "w", encoding="utf-8") as f:
            f.write(html)
        gerados.append((destino, len(html)))
        print("  gravado: {:<44} {:>7} bytes".format(
            os.path.relpath(destino, RAIZ), len(html)))
    if not gerados:
        sys.exit("nenhuma página gerada")
    print("\n  {} páginas".format(len(gerados)))


if __name__ == "__main__":
    main()
