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
        lead="As duas folhas para imprimir e distribuir. Servem quando o celular não "
             "ajuda, e servem para quem prefere caneta.",
        chips=["Imprimível", "Duas folhas A4"],
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
        html = monta(slug, cfg, fragmento)
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
