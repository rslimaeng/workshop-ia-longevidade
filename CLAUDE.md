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
    ├── gates.py          doze gates, cada um provado contra defeito injetado
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

`python3 _build/gates.py` roda dezesseis gates contra as sete páginas. Todo gate é calibrado
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

## Armadilhas já pagas nesta pasta

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
- **Altura de campo não se resolve por altura de linha.** O navegador dá ao
  seletor uma altura interna própria, de 20px contra 23px do campo de texto.
  Só piso explícito iguala. Provado com defeito injetado no DOM vivo.
