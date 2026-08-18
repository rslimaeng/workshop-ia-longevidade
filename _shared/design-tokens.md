# Design tokens · Ideação com AI First

Referência humana dos tokens. A fonte única é `_build/base.css`, que o gerador replica
dentro de cada página, o que mantém cada arquivo autossuficiente e abrível sem servidor.

Base herdada do Workshop Maria Pitanga, com o accent trocado pelo azul institucional que a
proposta e o deck da Longevidade já usavam.

## Cores

```css
/* Fundo e superfícies */
--bg:            #F0EEE6;   /* creme · fundo principal */
--bg-elev:       #FFFFFF;   /* elevação, cards */
--bg-warm:       #E8E6DC;   /* creme mais escuro, chips e cabeçalho de tabela */
--bg-code:       #F5F3EA;   /* fundo de bloco de citação */

/* Texto */
--text:          #141413;
--text-muted:    #3D3D3A;
--text-dim:      #87867F;

/* Bordas */
--border:        rgba(20,20,19,.10);
--border-strong: rgba(20,20,19,.18);

/* Accent · azul institucional, o mesmo da proposta e do deck */
--accent:        #0E3D73;
--accent-dark:   #092A50;   /* hover */
--accent-soft:   #E3EAF2;   /* fundo tingido de chip e callout */
--accent-tinted: #F5F8FB;   /* card accent bem sutil */
--accent-line:   rgba(14,61,115,.20);

/* Semânticas */
--success:       #2E7D32;   --success-soft: #E8F1E9;
--warning:       #B8860B;   --warning-soft: #FBF3DE;
--danger:        #B85C5C;   --danger-soft:  #F5E3E3;
```

## Tipografia

```css
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', 'Menlo', monospace;
```

Carregadas por CDN. Se a rede da sala bloquear, a página cai para a fonte do sistema e
continua legível: nenhum componente depende da fonte carregar.

## Regras de estilo

- **Nunca** borda lateral grossa colorida em card ou callout. Fundo tingido derivado da
  cor semântica mais um ponto pequeno via `::before` no rótulo.
- Emoji só em callout curto e pontual. Nunca em card decorativo.
- Cabeçalho fixo com `backdrop-filter: blur(10px)` sobre `rgba(240,238,230,.92)`.
- Sem gradiente, sem glassmorphism, sem modo escuro.
- `@media (prefers-reduced-motion:reduce)` em toda página.
- Grade responsiva: colapsa em `900px`, onde a navegação lateral vira topo, e em `720px`,
  onde as colunas viram uma.
- `localStorage` sempre com prefixo `ls_`, para não colidir com os outros sites do Rafael.

## Componentes

| Classe | O que mostra |
|---|---|
| `.site-header` · `.brand` · `.chip` | Cabeçalho fixo, em todas as páginas |
| `.crumbs` | Caminho de volta, nas páginas internas |
| `.side-nav` | Navegação lateral com destaque por rolagem. Vira topo no `900px` |
| `.hero` | Bloco de abertura: eyebrow, título e chamada |
| `.card` · `.card-accent` · `.card-highlight` | Card base, tingido e cheio |
| `.card-grid-2` · `-3` · `-4` | Grades de card |
| `.callout` + `.callout-info` / `.callout-warn` | Aviso e regra, com rótulo em mono |
| `.compare` + `.ruim` / `.bom` | Duas colunas lado a lado. Pedido sem contexto e com contexto |
| `.compare-quote` | O texto literal do pedido, em mono |
| `.table-wrap` | Envelope com rolagem lateral para tabela |
| **`.pilar` + `.pilar-n` + `.pilar-onde`** | Um dos cinco pilares, com o selo de onde ele é provado |
| **`.passo` + `.passo-n`** | Etapa numerada de exercício. Número à esquerda, sem minutagem |
| **`.gabarito`** | A resposta do caso, atrás de um `<details>`. **Nunca com `open`** |
| **`.checagem`** | O validador de fim de página: o que confere e como |
| `.agenda` + `.agenda-row` | A divisão das quatro horas. **Só na capa** |
| `.mod-card` | Card de navegação para as outras páginas |
| `.folha` + `.fp` | A folha A4 imprimível dos cinco pilares |
| `.nav-bottom` + `.nav-link` | Anterior e próxima, no pé |
| `.rot` | Rótulo que precisa ser bloco. Usar esta classe, nunca `display:block` numa tag inline |

**Fonte da verdade de conteúdo:** `_build/conteudo/caso-2.html`, que é a página mais
completa, com passo numerado, gabarito, tabela e checagem.

## O `.gabarito` é regra de produto, não de estilo

Ele existe porque o caso é dado em três passos: a sala resolve, depois descobre. Deixar a
resposta visível não é um detalhe de layout, é acabar com o exercício. Conferido pelo gate
**G5**, calibrado injetando `open` numa cópia.

## Impressão

Só a folha dos pilares tem folha de impressão, embutida no próprio fragmento. Sai em uma
página A4 retrato, com o cabeçalho do site, a navegação e os callouts marcados
`.no-print` fora. Os números dos pilares viram preto sólido com `print-color-adjust:exact`,
para não sumirem em impressora monocromática.
