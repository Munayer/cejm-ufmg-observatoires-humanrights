# BR-MG-ObservatoriumHumanitarium — Observatório de Direitos Humanos

**`index.html` é o produto.** Um único arquivo, zero rede, zero build,
zero dependência — abre offline, imprime, pode ser hospedado como está
(GitHub Pages, qualquer host estático). Todo o resto neste repositório é
evidência ou documentação que sustenta o que está dentro dele; nada
precisa ser processado para o site funcionar.

Recorte principal: **Estado de Minas Gerais**. Brasil e demais unidades da
federação aparecem como remissão opcional dentro de cada indicador, não
como página geral.

*(Nome anterior deste projeto: Astreia — renomeado a pedido. O pacote
Python interno do motor de dados real, quando reintegrado, segue `odh`;
nome de marca fica fora dos identificadores de código.)*

## O que tem em `index.html`

- **Barra lateral de Temáticas** — outline fluida (expandir/colapsar por
  transição de grade, sem JS medindo altura — inspirado na sensação de
  navegação do Logseq), paleta e tipografia do padrão institucional
  Jean Monnet/Erasmus+ (azul-escuro, azul, dourado como acento pontual,
  serifada só em destaque). Três temáticas:
  - **Execução Penal** — implementada. Três indicadores sintéticos
    (taxa de ocupação, déficit de vagas, cobertura de informação) mais
    um indicador com **dado real**: "Direitos penitenciários de mulheres
    — Minas Gerais", a partir do SISDEPEN 2025/2 (ver `dados/sisdepen/`).
  - **Direitos Humanos no Meio Ambiente Urbano** — `candidato`: sem
    fonte registrada, sem indicador.
  - **Direitos Humanos no Meio Ambiente Rural** — `candidato`, mesma
    situação.
  Cada temática tem sua própria seção Objeto / Ressalvas / Indicadores /
  Fontes / Evidência.
- **Minas Gerais em primeiro plano** — cada indicador comparativo abre
  com um destaque do valor de MG; a lista completa (Brasil + 27 estados)
  fica dentro de um `<details>` recolhido.
- **Citação normativa linkada à fonte oficial** — Planalto para lei e
  decreto federal, portal do STF para jurisprudência, Corte IDH/CNJ para
  supervisão de cumprimento. Uma citação sem par verificado fica sem
  link e ganha o selo "fonte oficial: a localizar" em vez de apontar
  para qualquer coisa. Lista completa com a razão de cada escolha de
  portal em `LINKS_OFICIAIS.md`.
- **Advertência de dados sintéticos** — os três indicadores originais de
  Execução Penal usam base sintética (gerada por função determinística,
  não descreve nenhum estabelecimento real); isso está declarado na
  própria página. O indicador de mulheres é a exceção: dado real,
  selo "dado real" para não se confundir com os outros três.

## Estrutura do repositório

```
index.html                 -- o produto. Editar direto; não há passo de build.
README.md                  -- este arquivo
LINKS_OFICIAIS.md          -- fonte oficial de cada citação normativa, com a razão da escolha
INTEGRACAO_WORDPRESS.md    -- caminho recomendado para publicar isto num WordPress já hospedado
dados/sisdepen/             -- evidência do único indicador com dado real
  sisdepen_mg_bruto.csv                       -- MG, ~1.780 colunas, 19 ciclos (2016/2-2025/2)
  sisdepen_mg_direitos_femininos_2025-2.csv   -- recorte curado, ciclo mais recente
  sisdepen_mg_direitos_femininos_serie.csv    -- mesmo recorte, agregado MG por ciclo
  sisdepen_mg_resumo.json                     -- números-resumo, hash SHA-256 do .xlsx original, metodologia
  sisdepen_mg_direitos_femininos.py           -- script que regenera os quatro arquivos acima a partir
                                                  de um novo .xlsx do SISDEPEN, quando o próximo ciclo sair
```

Removido nesta limpeza (cumpriram o papel de migração e não sobrevivem
como arquivo à parte — o conteúdo de todos já está dentro de
`index.html`): `base.html`, `estilo.css`, `modelo_html.py`,
`montar_previa.py`, `previa-redesign-sidebar.html`. Se precisar
recuperar algum, está no histórico do git.

## O que falta para isto virar o painel real (motor de dados completo)

Este pacote **não inclui** `odh/core`, `odh/sources` nem
`odh/data/*.toml` — o motor Python que geraria `index.html` a partir de
dado real, ciclo a ciclo, vive no repositório `observatorio-dh` e não
faz parte deste envio. Para devolver o que está aqui a esse repositório:

1. Adicionar um campo `tema` (`execucao_penal` / `ambiente_urbano` /
   `ambiente_rural`) a `IndicatorSpec` e a `SourceSpec`.
2. Mapear ao menos um sistema candidato para cada tema novo em
   `docs/sistemas.md` antes de qualquer indicador — nenhum dado foi
   inventado aqui para essas duas temáticas, de propósito.
3. Adicionar um campo `fonte_oficial_url` a `Obligation` (em
   `odh/core/normative.py`) e usar `LINKS_OFICIAIS.md` como ponto de
   partida para popular `odh/data/normative/*.toml`.
4. Portar `dados/sisdepen/sisdepen_mg_direitos_femininos.py` para um
   adaptador de `odh/sources`, para que o indicador de mulheres deixe de
   ser um recorte manual e passe a atualizar sozinho a cada novo ciclo
   do SISDEPEN.

## Licença

Pretendida: AGPL-3.0-or-later — mesma decisão do repositório original.
