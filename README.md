# BR-MG-ObservatoriumHumanitarium — Observatório de Direitos Humanos

**`site/index.html` é o produto.** Um único arquivo, publicado pelo
Codeberg Pages em <https://observatoriodhcejm.com> a partir da pasta
`site/`; serve também em qualquer host estático. Repositório principal no
[Codeberg](https://codeberg.org/Munayer/cejm-ufmg-observatoires-humanrights),
com espelho no GitHub. Quase tudo funciona
offline — a única exceção é o mapa interativo na barra direita, que
precisa de rede para os tiles (ver ressalva abaixo). Todo o resto neste
repositório é evidência ou documentação que sustenta o que está dentro
dele; nada precisa ser processado para o site funcionar.

Recorte principal: **Estado de Minas Gerais**. Brasil e demais unidades da
federação aparecem como remissão opcional dentro de cada indicador, não
como página geral.

*(Nome anterior deste projeto: Astreia — renomeado a pedido. O pacote
Python interno do motor de dados real, quando reintegrado, segue `odh`;
nome de marca fica fora dos identificadores de código.)*

## Ressalva de rede: o mapa não é offline

Todo o resto do documento é texto e CSS embutidos — abre sem internet.
A barra de mapa (`.mapa-lateral`, direita) é a exceção deliberada: ela
carrega a biblioteca Leaflet de um CDN (cdnjs) e os tiles do próprio
OpenStreetMap (`tile.openstreetmap.org`), passados para cinza claro por
um filtro CSS. Sem rede, o mapa mostra um aviso e o resto da página
segue funcionando normalmente — o `try/catch` em torno da inicialização
do Leaflet garante essa degradação graciosa, no mesmo padrão do
protótipo `minerva-map` que serviu de referência para esta barra.

O fundo vinha antes da CARTO (`basemaps.cartocdn.com`, estilo light).
Em 29 de outubro de 2026 todo tile da CARTO chegava com a marca
"API KEY REQUIRED", também no site publicado: a CARTO passou a exigir
chave de API nos basemaps (termos de 29 de setembro de 2026), e sem
chave devolve essa imagem, qualquer que seja o `Referer`. Chave no
código não serve, porque o repositório é público e ela iria junto para
o ar. Os tiles do OpenStreetMap dispensam chave, mas seguem a
[política de uso](https://operations.osmfoundation.org/policies/tiles/)
dos servidores da OSMF: crédito visível no mapa e cabeçalho `Referer` em
cada pedido. Por isso o mapa só funciona com a página servida por
http(s) — aberta direto do disco (`file://`), o navegador não manda
`Referer` e o OSM devolve tiles de "Access blocked" — e a
`Referrer-Policy` de `site/_headers` não pode ficar mais restrita que
`strict-origin-when-cross-origin`.

## O que tem em `index.html`

- **Barra lateral esquerda de Temáticas** — outline fluida
  (expandir/colapsar por transição de grade, sem JS medindo altura —
  inspirado na sensação de navegação do Logseq), paleta e tipografia do
  padrão institucional Jean Monnet/Erasmus+ (azul-escuro, azul, dourado
  como acento pontual, serifada só em destaque). Três temáticas:
  - **Manutenção do Sistema Penitenciário Brasileiro** — implementada.
    Três indicadores sintéticos (taxa de ocupação, déficit de vagas,
    cobertura de informação) mais um indicador com **dado real**:
    "Direitos penitenciários de mulheres — Minas Gerais", a partir do
    SISDEPEN 2025/2 (ver `dados/sisdepen/`).
  - **Direitos Humanos no Meio Ambiente Urbano** — `candidato`: sem
    fonte registrada, sem indicador.
  - **Direitos Humanos no Meio Ambiente Rural** — `candidato`, mesma
    situação.
  Cada temática tem sua própria seção Objeto / Ressalvas / Indicadores /
  Fontes / Evidência.
- **Barra lateral direita de mapa** — Leaflet + OpenStreetMap em cinza,
  46 municípios de MG com mulheres em custódia física (SISDEPEN 2025/2),
  círculo proporcional à população feminina, destaque dourado para o
  único município (Vespasiano) com qualquer infraestrutura materna
  declarada. Cada popup linka de volta ao indicador de mulheres na
  coluna central (troca de temática + rolagem automática). Três achados
  fixos abaixo do mapa; coordenadas são aproximadas (sede do município),
  não conferidas contra uma fonte cartográfica única — ressalva
  declarada na própria barra.
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
  Manutenção do Sistema Penitenciário Brasileiro usam base sintética
  (gerada por função determinística, não descreve nenhum estabelecimento
  real); isso está declarado na própria página. O indicador de mulheres
  é a exceção: dado real, selo "dado real" para não se confundir com os
  outros três.
- **Parágrafos justificados** (`text-align:justify` + `hyphens:auto`) em
  todo texto corrido — miolo dos indicadores, deveres normativos, cartões
  vazios das temáticas candidatas.
- **Rodapé de cofinanciamento da União Europeia** — emblema oficial
  "Cofinanciado pela União Europeia" (`site/assets/eu/co-funded-pt-pos.png`,
  sem modificação, 56 px de altura) e, ao lado, a marca do Centro de
  Excelência Jean Monnet (`site/assets/cejm/cejm-pt-pos.png`) na mesma
  altura, nunca maior que o emblema; aviso da EACEA e menção às Ações Jean
  Monnet do programa Erasmus+, como pedem as orientações da Comissão
  Europeia para beneficiários de financiamento da UE. Mesmo texto do
  rodapé do Observatório SOMA, com as marcas ao lado do aviso (acima dele
  quando a coluna fica estreita). As duas marcas são os únicos arquivos
  locais que a página carrega além de si mesma.

## Estrutura do repositório

```
site/index.html            -- o produto. Editar direto; não há passo de build.
site/assets/eu/            -- emblema oficial "Cofinanciado pela União Europeia" do rodapé, sem modificação
site/assets/cejm/          -- marca do Centro de Excelência Jean Monnet do rodapé, recortada e reduzida
site/_headers              -- cabeçalhos HTTP do site (formato Netlify, lido pelo Codeberg Pages)
site/_redirects            -- www.observatoriodhcejm.com redireciona para o domínio principal
netlify.toml               -- resto da hospedagem anterior no Netlify; sai quando o site lá for apagado
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
  gerar_dados_mapa.py                         -- regenera o array de dados da barra de mapa a partir
                                                  de sisdepen_mg_bruto.csv (mesma lógica, por município)
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

1. Adicionar um campo `tema` (`manutencao_sistema_penitenciario` /
   `ambiente_urbano` / `ambiente_rural`) a `IndicatorSpec` e a
   `SourceSpec`.
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

O emblema em `site/assets/eu/` não entra na licença do projeto: é o
arquivo oficial da Comissão Europeia (o mesmo do Observatório SOMA, só
redimensionado), e o seu uso segue as orientações da Comissão para
beneficiários de financiamento da UE e o acordo administrativo com o
Conselho da Europa (JO C 271 de 8.9.2012). A marca em `site/assets/cejm/`
também fica fora da licença: é do Centro de Excelência Jean Monnet da
UFMG.
