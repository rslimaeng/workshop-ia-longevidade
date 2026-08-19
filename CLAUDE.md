# CLAUDE.md · workshop-ia-longevidade/

Site do encerramento da Trilha de Cultura de IA do **Grupo Longevidade Saudável**
(educação médica, Eusébio/CE), contratado via IEL Ceará. **19/08/2026, 4h, turma única,
cerca de 40 pessoas.**

O contexto da frente está em `../00-aqui-paramos.md` e `../CLAUDE.md`. Este arquivo cobre
só o site.

## Quem abre estas páginas

**O participante**, com uma exceção declarada: a `/analise/`, que é da facilitação e
fica de propósito fora da lista de cards da capa. Nela mora o passo a passo da planilha
e o prompt que o Rafael cola no dia. Gate **G39**, que também confere que ela não virou
card. Em todas as outras, o leitor é o participante, e isso decide quase tudo:

- Não é roteiro de instrutor. Nada de *pergunte à sala*, *espere o silêncio*, *plano B*.
  A direção de cena vive fora do repositório. Gate **G8**.
- Não é o deck de aprovação. O deck fala com a gestão em ganho de negócio e método; estas
  páginas falam com quem vai executar na segunda-feira.
- Minutagem é controle de condução e **só a capa carrega**, porque lá ela é o contrato do
  que foi vendido. Gate **G9**.

## Estrutura

```
workshop-ia-longevidade/
├── index.html            a capa
├── canvas/               a régua, respondida no começo e no fim, mais a ficha
├── ai-first/             o conceito e os pilares 1 e 2
├── caso-1/ caso-2/       os dois casos em três passos
├── ficha/                a ficha dos quatro campos
├── pilares/              a folha A4 imprimível
├── analise/              a facilitação: o prompt da análise ao vivo
├── _shared/              os tokens, em referência humana
└── _build/
    ├── base.css          o CSS, fonte única
    ├── gerar.py          monta as páginas, e trata o canvas com os passos de texto
    ├── gates.py          trinta e nove gates, cada um provado contra defeito injetado
    └── conteudo/         o conteúdo de cada página, em fragmento
```

**Editar conteúdo é editar o fragmento, nunca o `index.html` gerado.** O que estiver no
HTML publicado é sobrescrito na próxima geração.

`canvas/index.html` é a exceção parcial: ele é standalone, com JavaScript próprio, e não
tem casca do site. Mas **passa pelo gerador** para receber os dois passos de texto (a cola
de quebra de linha e o corte em frases). Enquanto isso era trabalho manual, toda edição
nele derrubava o G28 e o G29.

**A régua exporta duas linhas, e o esquema é contrato.** Nove colunas para a régua, iguais
nas duas rodadas e separadas pela coluna `momento`; sete para a ficha. Os nomes estão em
`REGUA_COLS` e `FICHA_COLS` no `gates.py`, e três coisas dependem deles: o JS do canvas, o
esquema desenhado na página e o prompt da `/analise/`. Gates **G38** e **G39**.

A planilha da sala e o ensaio saem de `../3-material-ai-first/gerar-planilhas.py`, e os
dois relatórios de ensaio de `../3-material-ai-first/simular-analise.py`.

## Base visual

Herdada do `maria-pitanga-issac/workshop-ia-mp/`, com o accent trocado pelo azul
institucional que a proposta e o deck já usam (`#0E3D73`). Creme `#F0EEE6` de fundo,
Inter e JetBrains Mono. Tokens em `_shared/design-tokens.md`.

Sem gradiente, sem glassmorphism, sem modo escuro. Nunca borda lateral grossa colorida:
fundo tingido mais um ponto pequeno no rótulo.

## Vocabulário fechado

Os cinco pilares têm rótulo canônico, e ele é o mesmo na proposta aprovada, na régua do
celular e na folha impressa. Paráfrase quebra a comparação de antes e depois. Gate **G10**.

1. O que não vira registro não existe
2. Resultado ruim é falta de contexto, não de capacidade
3. Quebrar em fases e conferir entre elas
4. Toda correção vira regra
5. Nada começa sem quatro campos preenchidos

## O que os gates cobrem

`python3 _build/gates.py` roda trinta e nove gates contra as oito páginas. Todo gate é calibrado
contra um defeito injetado numa cópia em memória, e um gate que não acusa o próprio
defeito derruba o script como **cego**.

| Gate | Confere |
|---|---|
| G1 | Travessão, que é proibido em todo material do Rafael |
| G2 | Vocabulário interno e nome de outra frente na tela |
| G3 | Premissa que o cliente mesmo deu, devolvida a ele |
| G4 | Classe usada no HTML sem regra no CSS |
| G5 | A resposta do caso nascendo aberta |
| G6 | Link relativo que não resolve no disco |
| G7 | Navegação lateral e seções, um para um, sem sobra dos dois lados |
| G8 | Direção de cena em página de participante |
| G9 | Minutagem fora da capa |
| G10 | Pilar com rótulo reescrito |
| G11 | Número de terceiro sem a fonte na mesma frase |
| G12 | A capa diz cinco pilares e tem cinco blocos |
| G13 | Botão de copiar apontando para um id que não existe |
| G14 | A figura dos cem quadrados contando diferente do texto |
| G15 | O prompt baixado divergindo do que está na tela |
| G16 | As caixas lado a lado do canvas sem piso de altura |
| G17 | Caractere de outro alfabeto que renderiza igual ao latino |
| G18 | Os números da turma conferidos contra a planilha do cliente |
| G19 | A régua com três alternativas e simétrica nas duas pontas |
| G20 | Passo do fluxo sem dizer quem faz |
| G21 | Os dois loops da capa começando com etapas diferentes |
| G22 | A folha em papel divergindo da régua da tela |
| G23 | Numeração de seção repetida ou fora de ordem |
| G24 | A página imprimível declarando um número de folhas que não tem |
| G25 | Cartão de vídeo incompleto, ou com número que envelhece sozinho |
| G26 | Imagem referenciada que não existe no disco |
| G27 | Página que não cabe num celular de 375px |
| G28 | O passo de quebra de linha que deixou de rodar sobre a página |
| G29 | Frase que não ganhou a sua linha, e o container query que faz isso valer |
| G30 | Número de auxiliares escrito que não bate com o que está listado |
| G31 | Barra da régua por fase cuja altura contradiz o número que ela diz |
| G32 | Lista de papéis que não bate com a frase que a anuncia |
| G33 | Referência a "seção NN" que aponta para bloco inexistente ou para o bloco errado |
| G34 | Degrau da escada cuja altura não cresce, ou que não apoia na mesma base |
| G35 | Callout sem variante de cor, que nasce sem caixa |
| G36 | Seta do ciclo que, empilhada, estica uma linha por cima dos cartões |
| G37 | Pergunta do bloco em grupo sem as três perguntas de destrave e o "não conta" |
| G38 | Esquema das duas abas da planilha divergindo do que o JS do canvas monta |
| G39 | Prompt da análise citando coluna que a planilha não tem, ou perdendo a regra de anonimato |

**Exit code sozinho nunca é prova.** Leia a saída: ela imprime achado por gate e diz
quais gates não se provaram.

## Os desenhos são conteúdo, não enfeite

Rafael reprovou a primeira versão por ser parede de texto: *"senti falta de
criatividade para criar referências visuais"*. O conserto não foi decorar, foi
**desenhar o conceito que a frase só descrevia**.

| Figura | Onde | O que ela prova |
|---|---|---|
| `.vias` | conceito, pilar 2 | O mesmo trabalho com a IA no fim e no desenho. À direita o processo encolhe de cinco passos para três |
| `.tela` | pilar 2 | O que volta do pedido sem contexto e do pedido com contexto, lado a lado |
| `.camadas` | caso 1 | Os três níveis empilhados. Era tabela, e tabela não comunica camada |
| `.esteira` | caso 2 | Cinco fases e **quatro portões**. O portão é o pilar 3: é ele que segura o trabalho, não a caixa |
| `.funil` | caso 2 | Seis entrevistas, trezentas páginas, três dias, uma decisão. A largura encolhe junto |
| `.ciclo` | caso 2 | A correção que vira regra, e a etapa 4 onde quase todo mundo para |
| `.cem-grade` | ficha | Cem quadrados, treze acesos. O número da Capgemini que se vê em vez de ler |
| `.quadro` | ficha | A ficha preenchida, no formato em que ela existe |
| `.loops` | capa | Loop aberto e loop fechado. As três primeiras caixas são iguais nos dois: o que muda é a volta. G21 |
| `.fluxo` | conceito | Passo a passo com **ator nomeado**. Sem a etiqueta de quem faz, o participante não sabe se aquilo é trabalho dele ou da máquina. G20 |
| `.ex` | conceito | As sete rotinas que a turma apontou no diagnóstico, cada uma como está hoje, como fecharia e o primeiro passo |
| `.tipos` | conceito, pilar 1 | As três gavetas de registro: o que é fato, como aqui se faz, o passo a passo |

**Figura que afirma número tem gate em cima.** A grade dos cem quadrados é
conferida contra o número escrito no texto (G14): se a frase disser 13 e a
figura acender outro tanto, a página mente em dois lugares.

## Os casos entregam prompt e insumo

Cada caso termina com o que o participante leva embora: um `.docx` fictício para
baixar e o pedido pronto, no padrão de passos numerados herdado do outro
workshop. O `.prompt-conteudo` é a fonte, e o gerador grava o `.md` ao lado a
partir dele, então **baixar e copiar entregam sempre a mesma coisa** (G15).

O botão de copiar tem ramo alternativo: `navigator.clipboard` só existe em
contexto seguro, e mesmo lá recusa sem foco. Quando os dois caminhos falham a
página diz *"selecione e copie na mão"* em vez de mentir que copiou. É por isso
que o arquivo para baixar existe: ele é o caminho que não depende de permissão.

## A quebra de linha é tratada no gerador, não à mão

Rafael reprovou duas vezes a quebra feia: a linha termina em *"na sua"* e joga
*"área."* para a linha de baixo. Três coisas importam aqui:

1. **`text-wrap:pretty` não resolve.** Ele só evita palavra órfã na última linha.
2. **`text-wrap:balance` resolve parte.** Vale nos blocos curtos e em evidência.
3. **O que fecha a conta é colar a palavra-função na seguinte com espaço rígido**,
   do jeito que uma gráfica faz. Aí a quebra procura outro lugar, e costuma achar
   a fronteira da frase.

O passo vive em `gerar.py` (`cola_quebra_de_linha`) e cobre título, `<label>` e
parágrafo de até 400 caracteres. Parágrafo longo fica com `pretty`: ninguém repara
numa quebra ruim no meio de seis linhas, e colar lá tiraria do navegador a
liberdade de achar a melhor linha.

**Nenhum trecho colado passa de 24 caracteres.** Acima disso a unidade indivisível
fica maior que a linha do celular e vira rolagem lateral, que é justamente o
defeito que a correção deveria evitar.

**O canvas não passa pelo gerador**, então a cola foi aplicada nele uma vez e está
gravada no arquivo. Se alguém recopiar de `../1-entregaveis/`, a cola some e o
**G28 acusa**.

Medido no navegador, 8 páginas por 8 larguras, de 1400px a 375px: **0 quebras
ruins publicadas, 369 com a cola desfeita**, nenhuma página estourando a largura.

Linha terminando no verbo *"é"* não conta como defeito: o que incomoda, e o que
os prints mostravam, é artigo e preposição separados do seu substantivo.

## Uma frase por linha, e por que não é a mesma coisa que a cola

O Rafael reclamou **três vezes** da quebra de linha, e as duas primeiras eu consertei o
sintoma errado. A queixa dele, nas palavras dele: *"era sobrar o espaço para continuar a
frase e vc quebrar ela"*.

**Não é a linha terminar em preposição. É a frase quebrar quando ainda sobra coluna.**
Medido: 283 das 491 frases quebravam no meio, e a frase mediana ocupa 497px numa medida de
720px. Três de cada quatro já cabiam numa linha. Elas quebram porque **não começam no
início da linha**.

**Alargar a coluna não resolve:** de 720 para 920 ganha 13% e dá 122 caracteres por linha.

O conserto é `uma_frase_por_linha` em `gerar.py`: cada frase vira `<span class="fr">`, e o
**container query** decide onde isso vira bloco. O corte é 600px, e ele veio de medição:
a fatia de frases que cabem numa linha é 10% até 300px, 54% entre 400 e 500, e 77% a
partir de 600. Abaixo disso, meia correção parece acidente.

**O passo é varredura com pilha, não regex.** Um terço do texto do site mora em `<div>` e
`<span>` de bloco, e `<div>(.*?)</div>` fecha na tag errada. A cola de espaço rígido ganhou
a mesma varredura (`_cola_em_folhas`), porque ela só alcançava `h1-4`, `label`, `<p>` e
`<li>`.

Medido nas 8 páginas: **241 → 139 frases partidas, 25 → 8 linhas em preposição, e 0
frases que caberiam e quebraram assim mesmo.**

## Armadilhas já pagas nesta pasta

- **Acrescentar uma classe ao `<p>` deixou dois gates cegos.** O G21 procurava
  `<p class="fig-leg">` como literal e o G11 casava a frase da Capgemini com
  espaço comum. Gate que casa atributo ou frase por literal quebra quando o
  gerador ganha um passo novo: procurar pelo **efeito**, com regex tolerante.
- **`\s` em JavaScript inclui o espaço rígido.** A sonda que media o maior trecho
  colado devolveu 0 porque partia justamente o que devia medir. Separar por
  `[ \t\n\r]` quando o espaço rígido é o objeto da medida.
- **O painel do navegador reporta `clientWidth: 0`** para arquivos fora da pasta do
  projeto. Toda medida derivada disso vira lixo com cara de número. Assertar a premissa no
  próprio retorno antes de acreditar em qualquer medição.
- **Para provar que o gabarito esconde a resposta**, injetar `open` no DOM vivo e conferir
  limpo → sujo → restaurado. Medir altura não funciona ali, porque a largura zerada
  destrói o layout.
- **Quebra de linha no arquivo-fonte não é quebra de linha na tela.** O extrator de texto
  colapsa o espaço antes de marcar bloco. Sem isso, o gate da fonte colada acusa a si
  mesmo e nasce cego.
- **O painel do navegador serve cache mesmo depois de o arquivo já estar no ar.**
  O `curl` confirmava a regra publicada e a folha de estilo carregada não a
  tinha. Furar com `?v=alguma-coisa` na URL, e **assertar no retorno que a regra
  está na folha servida** antes de acreditar na medida.
- **Conferir propagação por presença de texto dá falso positivo.** O laço que
  esperava `line-height: 1.5` passou de primeira porque a string já existia em
  quatro outros pontos do arquivo. Procurar no contexto exato, ou comparar a
  contagem do publicado com a do local.
- **`<style>` injetado no `<head>` não vence o `<style>` da própria página**, que
  vive no corpo do fragmento e vem depois. A primeira medição de impressão disse
  144% porque as regras não pegavam. Injetar no fim do `body` e **assertar que a
  regra mudou o valor computado** antes de acreditar em qualquer medida.
- **A página imprimível não cabia na A4 que ela promete.** A folha dos pilares
  dava 114% e afirmava em três lugares que saía em uma folha. Medir, e não
  estimar por contagem de linhas.
- 🔴 **`container-type:inline-size` zera a largura de quem se dimensiona pelo conteúdo.**
  Num item de flex o bloco foi para 0px e o texto saiu **uma palavra por linha**. O gate
  estático não vê isso, e a página parecia normal no HTML. A marca do contêiner sobe até o
  primeiro ancestral de largura definida, e o **G29 acusa** quem estiver em item de flex.
- 🔴 **Seis gates cegaram de uma vez** quando o gerador ganhou o passo de frases: os
  injetores casavam literal com espaço comum, e o espaço rígido entrou no meio. Todo
  injetor passou a usar `como_escrito()`, e o **G10 compara o que se lê**, não os bytes.
- **Constante com o mesmo nome em dois gates.** `NUMERO_POR_EXTENSO` já existia no G24 sem
  acento e o G30 redefiniu com acento, quebrando o G24. Nome de constante nova confere
  antes.
- **`requestAnimationFrame` não dispara com o painel do navegador escondido.** Toda sonda
  que redimensiona iframe trava em 30s. Usar `setTimeout` e forçar reflow lendo
  `offsetHeight`.
- 🔴 **Direção de cena não é só fala de palco: condução de dinâmica também é.** "Um grupo
  por vez, dois minutos cada", "leia só até o fim da seção 02" e "escutem os outros" são
  instrução para o instrutor, e estavam nas duas páginas de caso. O G8 ganhou esses termos.
- **`<div class="callout` casa também `<div class="callout-title`.** Um script de remoção
  cortou a abertura do callout e deixou o parágrafo órfão na página. Prefixo de classe
  precisa do delimitador: `<div class="callout(?=[ "])`.
- **Remoção de bloco se faz por balanceamento, e se confere contando as tags.** Antes e
  depois: `<div>` contra `</div>`, e o texto removido tem que sumir do arquivo. Sem essa
  conferência o corte parece ter dado certo e sobrou meio bloco.
- **Página com vários grupos e um instrutor só precisa responder a dúvida antes dela
  virar mão levantada.** Toda pergunta de trabalho em grupo carrega três perguntas menores
  que destravam e um exemplo do que NÃO conta como resposta. G37 confere que o padrão vale
  para todas, e não para algumas.

- 🔴 **`transform:rotate` num elemento largo estica tudo que ele desenha.** A seta do ciclo,
  empilhada no celular, virava uma **barra vertical de 669px cortando os cartões** de cima
  e de baixo, porque a linha do `::before` ia de `left:0` a `right:0`. Estava no ar na capa
  e só apareceu quando o componente foi repetido numa página mais estreita. **Girar o
  glifo, não o contêiner.**
- **`.callout` sem variante não pinta nada.** A cor e a borda vêm de `callout-info` ou
  `callout-warn`; sozinho, o texto sai solto no meio da página. G35 confere.
- **Regex de palavra com plural opcional erra o singular.** `[Pp]ilares?` exige "ilare", e
  a palavra é "Pilar": o gate acusou os sete cards de não nomearem pilar nenhum. O certo é
  `[Pp]ilar(?:es)?`. **Quando um gate acusa tudo de uma vez, o defeito costuma ser dele.**
- **Insumo que descreve outra turma não vai para a tela.** O levantamento prévio era de
  outra trilha e de outro momento; citá-lo prometia à sala uma pesquisa que não foi feita
  para ela. O gate mudou de mecanismo: em vez de conferir número na tela, confere
  **proveniência** (as atividades continuam vindo do insumo) e **coerência interna** (o
  rótulo de cada card bate com o pilar que o corpo dele nomeia).

- 🔴 **Inserir uma seção renumera as seguintes, e as referências cruzadas ficam para trás.**
  Duas frases mandavam "releia a seção 04" e "o exercício da seção 05" apontando para
  blocos de outro assunto, **e estavam no ar**. O G33 confere que a referência existe **e
  que o assunto citado é o daquele bloco**. Referência por número é frágil por natureza:
  quando der, referir pelo nome.
- **A janela de contexto do gate não pode atravessar a quebra de bloco.** O G33 procurava
  o assunto nos 60 caracteres anteriores e pegava o rótulo do próprio bloco acima,
  acusando a si mesmo. Cortar na última quebra de linha.
- **O painel serve cache também em `file://`.** Uma medição disse que a fonte não tinha
  mudado quando o arquivo no disco já estava certo. Furar com `?v=algo` na URL do arquivo,
  e **assertar no retorno que a versão medida é a nova** (contar um elemento que só existe
  nela) antes de acreditar em qualquer número.

- 🔴 **Figura que é prova se confere pela geometria, não pelo texto ao lado.** A régua
  por fase afirma que a exigência sobe e depois cai. Se a altura de uma barra deixar de
  acompanhar o número que ela diz, a figura passa a dizer o contrário do parágrafo e
  **nenhum gate de texto vê**. O G31 compara altura contra número, número contra
  `aria-label`, e o teto citado no texto contra o teto da figura.
- **`\b` casa antes do hífen.** `r"\bpapel\b"` acertou também `papel-nome` e `papel-d`,
  e o gate contou 16 linhas onde havia 5. Classe se casa como classe inteira, com o
  helper `CL()`: delimitada por espaço ou pela aspa.
- **Terceira recorrência do injetor literal, agora no próprio gate.** O G32 nasceu cego
  procurando `class="papeis"` porque o gerador acrescenta `fr-host` na mesma tag. Não é só
  o injetor que precisa ser tolerante: **o gate também**.
- **Dicionário de número por extenso que para em dezessete é gate que para em dezessete.**
  `dezenove itens` não acusava nada. `NUM_ALTO` cobre até trinta.
- **Fonte dentro de SVG se mede depois de escalada.** A figura renderiza a 860px de um
  `viewBox` de 1160, então toda fonte encolhe 26%: `font-size="11"` chega ao celular com
  8,2px. O piso do que já está no ar é 7,8px; medir, e não estimar.

- **Dentro de `<svg>` um `<span>` não desenha nada.** Cortar frase ali apagaria texto da
  figura na tela sem apagar nada do HTML. O gerador proíbe pela **árvore**, não pelo
  elemento: proibir só o elemento deixou a cola entrar no `.fonte-cta` lá dentro.
- **Altura de campo não se resolve por altura de linha.** O navegador dá ao
  seletor uma altura interna própria, de 20px contra 23px do campo de texto.
  Só piso explícito iguala. Provado com defeito injetado no DOM vivo.

### Da leva de 19/08 · o canvas vira régua de duas rodadas

**Artefato com JS não se confere por leitura: se preenche, se clica e se lê a saída.**
O canvas passou nos gates estáticos copiando uma linha **sem a área**, e o relatório do
dia é por área. Nenhum gate estático veria isso, porque o defeito estava no que o
`click` produz, não no que o HTML diz.

**A premissa do teste funcional também precisa ser assertada.** As quatro travas do
canvas deram "VAZOU" na primeira rodada, e o motivo era que o navegador restaura os
campos de formulário ao recarregar: o código já estava preenchido antes do teste
começar. Limpe à mão e **asserte o estado limpo no próprio retorno** antes de clicar.

**`localStorage` não existe em `data:` URL.** O painel serve arquivo local como
`data:text/html`, e ali toda gravação levanta `SecurityError`. Rascunho, sessão e
qualquer coisa persistida só se testa em `http(s)://`, ou seja, **depois de publicar**.

**Duas barras sobrepostas não comunicam duas medidas.** A do fim tapava a do começo e o
olho lia um tom só. Vire uma barra em duas partes (onde estava, o que andou) e **meça a
geometria no DOM vivo**: a base tem de encostar no ganho e a soma tem de valer a média
do fim.

**Empate em média é caso real, e ele aparece na tela como incoerência.** Dois pilares
com 1,56 deixavam duas barras idênticas com cores diferentes. Todo `min()`/`max()` que
escolhe "o mais fraco" precisa de critério de desempate declarado, e o critério tem de
estar também no prompt, porque o Claude do dia faz a mesma escolha.

**Gate que acopla dois artefatos acha lacuna que a revisão não acha.** O G39 nasceu para
impedir divergência entre o prompt e as colunas, e a primeira coisa que ele acusou foi
que o prompt descrevia a aba da régua coluna por coluna e deixava a aba das iniciativas
sem esquema nenhum. O gate leu o que eu escrevi melhor do que eu.

**Página gerada por script precisa entrar no pipeline, ou os gates de texto quebram.**
O canvas era tratado à mão com os dois passos de quebra de linha, então toda edição nele
derrubava o G28 e o G29. Passou a ser tratado pelo `gerar.py`.
