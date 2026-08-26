# GitHub → WordPress: gargalos e caminhos

Pergunta: lançar este painel no GitHub e depois integrar a um WordPress já
hospedado. Levantamento feito em 24/08/2026.

## O gargalo central

O painel é **um único arquivo HTML autocontido** — `<!doctype>`, `<head>`,
`<style>` inteiro, `<body>`, `<script>` de busca e de abas. O editor de
blocos do WordPress (Gutenberg) não aceita um documento inteiro colado
dentro de uma página ou post: ele espera um *fragmento* de conteúdo, e o
bloco que mais se aproxima — **HTML Personalizado** — só libera os painéis
de CSS e de JavaScript (desde o WordPress 7.0) para quem tem a capacidade
`unfiltered_html`. Por padrão:

- Administrador em instalação **single-site**: tem essa capacidade.
- Qualquer papel abaixo de Administrador, e **qualquer papel em
  multisite** (exceto Super Admin): não tem, e o WordPress remove
  `<script>`, `<style>` e `<iframe>` ao salvar — silenciosamente, sem
  aviso claro na hora.
- Hospedagens gerenciadas (WordPress.com, alguns planos de hosts
  gerenciados) costumam restringir isso ainda mais, independente de papel,
  por política de segurança da própria hospedagem.

Ou seja: colar o HTML inteiro num bloco pode funcionar hoje e quebrar
amanhã com uma atualização de plugin de segurança ou mudança de papel —
gargalo real, não hipotético.

Há um segundo gargalo, menor mas certo: **CSS vaza**. `estilo.css` usa
seletores genéricos por design (`a{...}`, `table{...}`, `h2{...}`) porque
foi pensado para uma página sozinha. Colado dentro do WordPress, essas
regras passam a competir com o CSS do tema inteiro — link, tabela e
cabeçalho do resto do site podem mudar de aparência sem querer, e o
inverso também: o CSS do tema pode sobrescrever o que o painel espera.

## Três caminhos, em ordem de robustez

### 1. `<iframe>` apontando para o GitHub Pages (recomendado para começar)

GitHub Pages serve o `index.html` do repositório publicamente, de graça,
sem servidor próprio. Na página do WordPress, um bloco HTML Personalizado
com uma única linha:

```html
<iframe src="https://SEU-USUARIO.github.io/br-mg-observatoriumhumanitarium/" style="width:100%;height:1400px;border:0"></iframe>
```

- **Não depende de `unfiltered_html` para o conteúdo do painel** — só
  precisa que o `<iframe>` em si não seja removido, o que é bem mais
  comum de ser permitido do que `<script>`/`<style>` arbitrários.
- **Zero risco de vazamento de CSS** — o iframe é um documento à parte,
  isolado por definição.
- Atualizar o painel = fazer `git push`; o GitHub Pages publica sozinho.
  Nada para copiar e colar de novo no WordPress.
- Contras: altura fixa (ou JS extra para redimensionar), rolagem
  duplicada em telas pequenas, e o conteúdo dentro do iframe não é
  indexado como parte da página do WordPress para SEO.

### 2. Template de página dedicado no tema (mais integrado, exige acesso ao tema)

Um arquivo `page-observatorium.php` no tema (ou tema-filho) que lê o HTML
publicado — por `file_get_contents()` de um arquivo enviado para
`wp-content/uploads/`, ou de um endpoint do próprio GitHub Pages via
`wp_remote_get()` com cache em transient — e devolve o `<body>` dentro do
layout do WordPress.

- Sem bloco de editor no meio, então sem `wp_kses()` mexendo no HTML.
- URL de verdade no domínio do WordPress, boa para SEO.
- Contras: exige FTP/SFTP ou gerenciador de arquivos do host para subir o
  template; se buscar do GitHub em tempo de requisição, cada visita paga
  uma chamada de rede a mais — cachear (transient de algumas horas) evita
  isso. E ainda existe o gargalo de CSS: as regras genéricas de
  `estilo.css` precisam ser prefixadas (ex.: `#observatorium-app a{...}` em vez
  de `a{...}`) antes de conviver na mesma página que o tema.

### 3. Colar direto no bloco HTML Personalizado (não recomendado como padrão)

Funciona só se a conta que edita tiver `unfiltered_html` — em site único,
geralmente só Administrador — e só até a próxima atualização de segurança
mudar isso. Mesmo funcionando, herda o gargalo de CSS do caminho 2, sem
nenhuma das vantagens dele. Deixar como plano B, não como rota principal.

## Recomendação prática

Publicar o repositório com **GitHub Pages ligado** (Settings → Pages →
Deploy from a branch, servindo `/` ou `/docs`) e embutir via `<iframe>`
(caminho 1) para já ter algo publicado e estável. Se depois vier a
necessidade de SEO ou de layout mais integrado ao resto do site, migrar
para o template de página (caminho 2) — nessa hora, prefixar
`estilo.css` é o primeiro passo, não o último.
