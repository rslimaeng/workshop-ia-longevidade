# CLAUDE.md · workshop-ia-longevidade/

Site do encerramento da Trilha de Cultura de IA do **Grupo Longevidade Saudável**
(educação médica, Eusébio/CE), contratado via IEL Ceará. **19/08/2026, 4h, turma única,
cerca de 40 pessoas.**

O contexto da frente está em `../00-aqui-paramos.md` e `../CLAUDE.md`. Este arquivo cobre
só o site.

## Quem abre estas páginas

**O participante**, e ninguém mais. Isso decide quase tudo:

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
├── canvas/               a régua e a ficha, no celular
├── ai-first/             o conceito e os pilares 1 e 2
├── caso-1/ caso-2/       os dois casos em três passos
├── ficha/                a ficha dos quatro campos
├── pilares/              a folha A4 imprimível
├── _shared/              os tokens, em referência humana
└── _build/
    ├── base.css          o CSS, fonte única
    ├── gerar.py          monta as páginas a partir dos fragmentos
    ├── gates.py          vinte e oito gates, cada um provado contra defeito injetado
    └── conteudo/         o conteúdo de cada página, em fragmento
```

**Editar conteúdo é editar o fragmento, nunca o `index.html` gerado.** O que estiver no
HTML publicado é sobrescrito na próxima geração.

`canvas/index.html` é a exceção: foi portado de `../1-entregaveis/canvas-ideacao-ai-first.html`
e não passa pelo gerador, porque tem JavaScript próprio. Quando o canvas mudar, copie de
novo e reponha o link de volta para `../`.

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

`python3 _build/gates.py` roda trinta e quatro gates contra as oito páginas. Todo gate é calibrado
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
