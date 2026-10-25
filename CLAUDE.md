# CLAUDE.md

Notas para sessões do Claude Code neste repositório. As regras gerais da
pasta de desenvolvimento estão em `C:\bmm\dev\CLAUDE.md`; o que segue é
específico deste projeto.

## O que é

Observatório de Direitos Humanos do Centro de Excelência Jean Monnet da
UFMG, recorte Minas Gerais. **`site/index.html` é o produto**: um único
arquivo com CSS e JS embutidos, sem passo de build. O resto do repositório
é evidência e documentação. Ver `README.md` para o conteúdo do painel.

Publicado pelo Netlify a partir de `site/` (`netlify.toml`, cabeçalhos em
`site/_headers`); `dados/` e a documentação ficam no GitHub, fora do ar.
Repositório público: `github.com/Munayer/cejm-ufmg-observatoires-humanrights`.

## Comandos

Não há build, linter nem testes. Para ver o site localmente:

```
python -m http.server 8000 --directory site     # http://localhost:8000
```

(`.claude/launch.json` tem a mesma configuração, para o navegador do app.)
O mapa precisa de rede (Leaflet no cdnjs, tiles da CARTO); o resto abre
offline e deve continuar abrindo.

Scripts de dados (Python 3, só biblioteca padrão), em `dados/sisdepen/`:

```
python dados/sisdepen/sisdepen_mg_direitos_femininos.py   # regenera os 4 arquivos de recorte a partir do .xlsx do SISDEPEN
python dados/sisdepen/gerar_dados_mapa.py > municipios_mapa.js.txt   # array MUNICIPIOS da barra de mapa
```

- `FONTE_XLSX` no primeiro script ainda aponta para `/mnt/user-data/...`
  (sessão em que rodou pela primeira vez); trocar pelo caminho local do
  `.xlsx` baixado antes de rodar. O `.xlsx` (71 MB) não vai para o git.
- A saída de `gerar_dados_mapa.py` é colada à mão no array `MUNICIPIOS` de
  `index.html`; não versionar o `.txt` intermediário.

## Estrutura de `index.html`

- `<style>` no topo; paleta institucional Jean Monnet/Erasmus+ em `:root`.
  A regra de tela estreita fica **no fim** da folha (perdia por ordem de
  fonte quando estava antes do layout de três colunas).
- Três colunas: barra de Temáticas (esquerda), painéis
  `section.tema-painel#tema-*` (centro), barra de mapa `.mapa-lateral`
  com `#mapa-mg` (direita).
- Cada temática tem as mesmas seções, com ids `objeto-*`, `ressalvas-*`,
  `indicadores-*`, `fontes-*`, `evidencia-*`. Uma temática nova segue esse
  padrão e entra também no índice de busca do primeiro `<script>`.
- Segundo `<script>`: Leaflet, dentro de `try/catch` para degradar sem rede.

## Regras de conteúdo

- **Nada é inventado.** Temática sem fonte fica como `candidato`, sem
  indicador. Citação normativa sem fonte oficial verificada fica sem link,
  com o selo "fonte oficial: a localizar"; cada link novo entra também em
  `LINKS_OFICIAIS.md`, com a razão da escolha do portal.
- **Dado sintético é sempre declarado.** Os três indicadores originais do
  sistema penitenciário são sintéticos; só o indicador de mulheres
  (SISDEPEN 2025/2) tem o selo "dado real". Não misturar os dois.
- Minas Gerais primeiro; Brasil e demais UFs em `<details>` recolhido.
- Coordenadas do mapa são aproximadas (sede do município) e isso está
  declarado na barra; não inventar coordenada para município novo.

## Convenções

- Texto do site, documentação e mensagens de commit em **português**,
  no estilo do `git log` (título no imperativo, corpo com a lista do que
  mudou e por quê).
- Nome de marca fora dos identificadores de código; o pacote do motor de
  dados, quando voltar, se chama `odh`.
- `INTEGRACAO_WORDPRESS.md` é anterior à mudança para o Netlify (fala em
  GitHub Pages e num nome antigo do repositório); o raciocínio do iframe
  continua valendo, mas a URL a embutir agora é a do Netlify.
- Licença pretendida: AGPL-3.0-or-later (ainda sem arquivo `LICENSE`).
