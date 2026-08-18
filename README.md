# Ideação com AI First · site do workshop

Material de apoio do encerramento da Trilha de Cultura de Inteligência Artificial do
**Grupo Longevidade Saudável**. Quatro horas, presencial, turma única. Conduzido por
Rafael Lima, via IEL Ceará.

O site é o que a sala usa no dia **e** o que fica depois. Cada página é um HTML
autossuficiente: abre sem servidor, funciona offline, roda de um pen drive.

## 👉 https://rslimaeng.github.io/workshop-ia-longevidade/

## O que está publicado

| Página | O que é |
|---|---|
| `index.html` | A capa: o fio condutor, os cinco pilares e a divisão das quatro horas |
| `canvas/` | A régua e a ficha, para responder no celular. Gera uma linha para a planilha da sala |
| `ai-first/` | O conceito de AI First e os pilares 1 e 2 |
| `caso-1/` | Conhecimento espalhado e muitas frentes, em três passos |
| `caso-2/` | Informação sensível e prazo curto, em três passos |
| `ficha/` | A ficha dos quatro campos, que é o pilar 5 e o fechamento |
| `pilares/` | Os cinco pilares em uma folha A4, para imprimir |

## A trava dos casos

As páginas de caso mostram **o problema** aberto e escondem **o que de fato aconteceu**
atrás de um bloco fechado. Isso não é decoração: o exercício é a sala desenhar a solução
antes de saber a resposta. Se a resposta estiver visível, o primeiro celular aberto acaba
com o exercício.

O gate **G5** confere que nenhum desses blocos nasce aberto.

## Como editar

O conteúdo de cada página vive em `_build/conteudo/<slug>.html`, como fragmento. O shell
(cabeçalho, tokens de CSS, navegação lateral, rodapé) é montado pelo gerador.

```bash
python3 _build/gerar.py
```

Depois de gerar, sempre:

```bash
python3 _build/gates.py
```

São doze gates. Cada um roda contra as sete páginas **e** contra uma cópia com defeito
injetado. Gate que não acusa o próprio defeito é reportado como cego e derruba o script,
porque gate não testado é gate que você acha que tem.

## Publicar

O repositório é servido por GitHub Pages a partir da raiz. O arquivo `.nojekyll` precisa
existir, senão o Jekyll interfere na entrega.

## Sobre os exemplos

Os números dos exemplos preenchidos da ficha **são inventados**, e a própria página diz
isso. Servem para mostrar o formato. Nenhum dado real de aluno, de paciente ou da
instituição aparece em página nenhuma.
