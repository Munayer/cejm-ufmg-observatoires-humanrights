# BR-MG-ObservatoriumHumanitarium — Observatório de Direitos Humanos

Recorte principal: **Estado de Minas Gerais**. Brasil e demais unidades da
federação aparecem como remissão opcional dentro de cada indicador, não como
página geral.

Este diretório contém a **prévia de uma mudança de escopo** sobre o painel
HTML que já existia (`base.html` / `estilo.css`), não o motor de dados
completo. O núcleo Python que gera o painel a partir de dado real
(`odh/core`, `odh/sources`, `odh/data/*.toml`) vive no repositório
`observatorio-dh` e não faz parte deste pacote — ver "O que falta" abaixo.

*(Nome anterior deste projeto: Astreia — renomeado a pedido. O pacote
Python interno segue `odh`; nome de marca continua fora dos
identificadores de código, mesma lógica já adotada antes para não forçar
refatoração.)*

## O que mudou nesta prévia

1. **Minas Gerais em primeiro plano.** Cada indicador agora abre com um
   destaque do valor de MG; a lista completa (Brasil + 27 estados) fica
   dentro de um `<details>` recolhido — "Ver Minas Gerais ao lado do Brasil
   e das demais unidades da federação".
2. **Menu de Temáticas.** Uma barra lateral fixa (outline, inspirada na
   fluidez de navegação do Logseq — expandir/colapsar por transição de
   grade, sem JS medindo altura) substitui a página única. Três
   temáticas:
   - **Execução Penal** — implementada, com os três indicadores que já
     existiam (taxa de ocupação, déficit de vagas, cobertura de informação).
   - **Direitos Humanos no Meio Ambiente Urbano** — `candidato`: sem fonte
     registrada, sem indicador. Mesma convenção de `docs/sistemas.md`.
   - **Direitos Humanos no Meio Ambiente Rural** — `candidato`, mesma
     situação.
   Cada temática tem sua própria seção Objeto / Ressalvas / Indicadores /
   Fontes / Evidência.
3. **Citação normativa linkada à fonte oficial.** Toda citação (`CADH`,
   `CF/88`, `Lei 7.210/1984`, `STF`, `Corte IDH`, `ONU`) que tem par
   verificado vira link para o documento oficial — ver
   `LINKS_OFICIAIS.md` para a lista completa e a data de conferência. Uma
   citação sem par verificado fica sem link e ganha o selo visual
   "fonte oficial: a localizar" em vez de apontar para qualquer coisa.
   **Importante:** nem toda fonte oficial é o Planalto — só lei e decreto
   federal moram lá. Jurisprudência do STF mora no portal do próprio STF;
   resolução da Corte IDH mora em `corteidh.or.cr` (ou no índice que o CNJ
   mantém sobre medidas provisórias relativas ao Brasil).

## O que **não** mudou

- O texto de cada indicador, pergunta, método e recusas — reaproveitado
  literalmente do painel anterior.
- Os dados continuam **sintéticos** (a mesma advertência grave aparece).
- `estilo.css` original não foi editado — as regras novas (abas, destaque
  MG, `<details>`, selo de citação pendente) vivem à parte, documentadas em
  `modelo_html.py`, para facilitar a mesclagem de volta ao repositório real.

## Como gerar a prévia

```bash
python3 montar_previa.py
```

Lê `base.html` + `estilo.css`, aplica as transformações e escreve
`index.html` — um único arquivo, zero rede, abre offline, imprime.
Nenhuma dependência fora da biblioteca padrão do Python.

## O que falta para isto virar o painel real de novo

Este pacote **não inclui** `odh/core`, `odh/sources` nem
`odh/data/*.toml` — só o que dá para reconstruir a partir do que foi
enviado (o painel renderizado, a folha de estilo e o módulo de render). Para
devolver a mudança de escopo ao repositório `observatorio-dh` real:

1. Adicionar um campo `tema` (`execucao_penal` / `ambiente_urbano` /
   `ambiente_rural`) a `IndicatorSpec` e a `SourceSpec`, e agrupar por tema
   em `dashboard/render.py` em vez de listar tudo em sequência única.
2. Mapear ao menos um sistema candidato para cada tema novo em
   `docs/sistemas.md` antes de qualquer indicador — nenhum dado foi
   inventado aqui para essas duas temáticas, de propósito.
3. Adicionar um campo `fonte_oficial_url` a `Obligation` (em
   `odh/core/normative.py`) e usar o mapa de `LINKS_OFICIAIS.md` como
   ponto de partida para popular `odh/data/normative/*.toml`.
4. Mudar a ordenação padrão de cada série de indicador para priorizar MG,
   com o resto da federação atrás de um elemento recolhível — mesma lógica
   de `montar_previa.py`, portada para `dashboard/render.py`.

## Licença

Pretendida: AGPL-3.0-or-later — mesma decisão do repositório original.
