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

`python3 _build/gates.py` roda doze gates contra as sete páginas. Todo gate é calibrado
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

**Exit code sozinho nunca é prova.** Leia a saída: ela imprime achado por gate e diz
quais gates não se provaram.

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
