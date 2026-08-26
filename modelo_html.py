EXTRA_CSS = """
/* ============================================================
   Adições da prévia — menu de Temáticas e Minas Gerais em
   primeiro plano. Vive à parte de estilo.css original porque é
   específica desta mudança de escopo; ao integrar de volta ao
   repositório real, mesclar aqui dentro de dashboard/estilo.css.
   ============================================================ */

.barra-temas{
  margin:1.8rem 0 0;
  border-bottom:2px solid var(--fio-forte);
  overflow-x:auto;
}
.barra-temas-interna{display:flex;gap:0}
.tab-tema{
  font-family:var(--sans);
  font-size:.8rem;
  font-weight:600;
  color:var(--discreto);
  background:none;
  border:none;
  border-bottom:3px solid transparent;
  padding:.85rem 1.2rem;
  cursor:pointer;
  white-space:nowrap;
}
.tab-tema:hover{color:var(--azul-escuro)}
.tab-tema[aria-selected="true"]{color:var(--azul-escuro);border-bottom-color:var(--azul)}
.tab-tema .rotulo-status{
  display:inline-block;
  margin-left:.45rem;
  font-size:.6rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.06em;
  color:var(--discreto);
  background:var(--barra-fundo);
  padding:.1rem .4rem;
}
.tab-tema[aria-selected="true"] .rotulo-status{color:var(--azul-escuro)}

.tema-painel[hidden]{display:none}

.destaque-mg{
  margin:1.3rem 0 0;
  padding:1rem 1.2rem .8rem;
  background:var(--azul-claro);
  border:1px solid var(--fio);
  border-left:4px solid var(--azul-escuro);
  max-width:44rem;
}
.destaque-rotulo{
  display:block;
  font-size:.68rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.1em;
  color:var(--azul-escuro);
  margin-bottom:.5rem;
}
.destaque-registro .registro{padding:0}

details.ver-todos{margin:1.5rem 0 0}
details.ver-todos > summary{
  cursor:pointer;
  font-size:.82rem;
  font-weight:600;
  color:var(--azul);
  padding:.4rem 0;
  list-style:none;
}
details.ver-todos > summary::-webkit-details-marker{display:none}
details.ver-todos > summary::before{content:"\\25B8\\00a0";display:inline-block}
details.ver-todos[open] > summary::before{content:"\\25BE\\00a0"}
details.ver-todos .serie{margin-top:.4rem}

.selo-a-localizar{
  display:inline-block;
  font-size:.6rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.04em;
  color:var(--alerta);
  border:1px solid var(--alerta);
  padding:.05rem .35rem;
  margin-left:.4rem;
  white-space:nowrap;
  vertical-align:middle;
}
a.lig-oficial::after{content:" \\2197";font-size:.82em}

.aviso-convencao{
  font-size:.86rem;
  color:var(--discreto);
  max-width:44rem;
  margin:.8rem 0 0;
  padding:.8rem 1rem;
  border:1px solid var(--fio);
  background:var(--fundo);
}

.card-vazio{
  margin:1.2rem 0;
  padding:1.6rem 1.8rem;
  background:var(--papel);
  border:1px dashed var(--fio-forte);
  color:var(--discreto);
  font-size:.92rem;
  max-width:44rem;
}
.card-vazio strong{color:var(--tinta)}

@media print{
  .barra-temas{display:none}
  .tema-painel[hidden]{display:block !important}
  details.ver-todos{display:block}
  details.ver-todos > summary{display:none}
}
"""

MODELO = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BR-MG-ObservatoriumHumanitarium — Observatório de Direitos Humanos · Minas Gerais</title>
<style>__ESTILO__
""" + EXTRA_CSS + """</style>
</head>
<body>
<div class="folha">

  <nav class="barra-menu">
    <div class="barra-interna">
      <span class="marca">BR-MG-ObservatoriumHumanitarium</span>
      <div class="busca">
        <input type="text" id="campo-busca" placeholder="Buscar indicador, dever, fonte…"
               autocomplete="off" aria-label="Buscar no painel">
        <div id="resultados-busca" class="resultados-busca" hidden></div>
      </div>
    </div>
  </nav>

  <header>
    <p class="chapeu">Minas Gerais e Sistema Interamericano de Direitos Humanos</p>
    <h1>BR-MG-ObservatoriumHumanitarium — Observatório de Direitos Humanos</h1>
    <p class="linha-fina">
      Recorte principal: Estado de Minas Gerais &nbsp;·&nbsp;
      três temáticas — Execução Penal, Direitos Humanos no Meio Ambiente Urbano,
      Direitos Humanos no Meio Ambiente Rural &nbsp;·&nbsp;
      Brasil e demais unidades da federação aparecem como remissão opcional,
      não como página geral.
    </p>
  </header>

  <nav class="barra-temas" aria-label="Temáticas">
    <div class="barra-temas-interna">
      <button type="button" class="tab-tema" data-tema="tema-execucao-penal"
              aria-selected="true">Execução Penal
        <span class="rotulo-status">implementado</span></button>
      <button type="button" class="tab-tema" data-tema="tema-ambiente-urbano"
              aria-selected="false">Direitos Humanos no Meio Ambiente Urbano
        <span class="rotulo-status">candidato</span></button>
      <button type="button" class="tab-tema" data-tema="tema-ambiente-rural"
              aria-selected="false">Direitos Humanos no Meio Ambiente Rural
        <span class="rotulo-status">candidato</span></button>
    </div>
  </nav>

  <!-- ================================================== TEMA: EXECUÇÃO PENAL -->
  <section class="tema-painel" id="tema-execucao-penal">

    <p class="linha-fina" style="margin-top:1.4rem">
      Período de referência 2025-S1 &nbsp;·&nbsp;
      gerado em 2026-08-22T13:35:17+00:00 UTC &nbsp;·&nbsp;
      4 registros de evidência
    </p>

    <div class="nota grave">
      <span class="rotulo">Advertência</span>
      <p>Esta página contém dados sintéticos e não é estatística. Os números foram
      gerados por função determinística para exercitar o programa sem acesso à rede.
      Não descrevem qualquer estabelecimento, estado ou pessoa, e não devem ser
      citados, publicados nem encaminhados como informação sobre a realidade
      prisional brasileira.</p>
    </div>
    <div class="nota">
      <span class="rotulo">Citações por conferir — 12</span>
      <p>As referências normativas desta página foram semeadas pelo repositório a
      partir de fontes secundárias. Confira cada uma contra o documento oficial e
      marque <span class="mono">verified = true</span> antes de usá-las em peça ou
      publicação. O link ao lado de cada citação aponta para o texto oficial —
      quando ele existe e foi conferido — mas isso não substitui a conferência de
      redação linha a linha.</p>
    </div>

    <h2 id="objeto-execucao-penal">Objeto</h2>
    <div class="miolo">
      <p>Esta temática confronta duas coisas públicas: os números que o Estado
      brasileiro publica sobre o sistema penal em <strong>Minas Gerais</strong> e os
      deveres jurídicos que já o vinculam — na Constituição, na lei federal, na
      jurisprudência do STF e no Sistema Interamericano de Direitos Humanos.</p>
      <p>O recorte é o Estado de Minas Gerais. O Brasil e as demais unidades da
      federação aparecem como comparação — abra "Ver Minas Gerais ao lado do
      Brasil e das demais unidades da federação" em cada indicador para
      consultá-los — não como o objeto principal desta página.</p>
      <p>O observatório não mede a realidade prisional. Mede a
      <em>autodescrição</em> que a administração produz sobre ela e a coloca ao
      lado da norma. Toda cifra aqui pode ser refeita por um terceiro a partir dos
      arquivos originais listados na seção de evidência.</p>
      <p>Nenhum número desta página afirma que houve violação de direito. Afirmar
      isso é ato de aplicação do direito e cabe a quem tem competência para
      praticá-lo.</p>
    </div>
    <div class="aviso-convencao">
      <strong>Convenção de citação desta página:</strong> cada referência
      normativa abaixo é um hiperlink para o texto oficial correspondente —
      Planalto/Casa Civil para lei e decreto federal, o portal do STF para
      jurisprudência, a Corte Interamericana (ou o índice mantido pelo CNJ) para
      resoluções de supervisão de cumprimento. Uma citação sem esse vínculo ainda
      verificado fica sem link e recebe o selo
      <span class="selo-a-localizar" style="margin-left:0">fonte oficial: a localizar</span>
      em vez de apontar para qualquer coisa.
    </div>

    <h2 id="ressalvas-execucao-penal">O que estas fontes não medem</h2>
    <ul class="rol">
      <li><strong>Base sintética em formato SISDEPEN (demonstração).</strong> NÃO
      são dados reais. Nenhum número daqui descreve qualquer estabelecimento,
      estado ou pessoa.</li>
      <li><strong>Base sintética em formato SISDEPEN (demonstração).</strong> Serve
      para verificar o funcionamento do código, não para conhecer a realidade
      prisional brasileira.</li>
      <li>O recorte territorial é Minas Gerais; o comparativo com o Brasil e as
      demais unidades da federação é remissão opcional, não o objeto principal
      desta página.</li>
    </ul>

    <h2 id="indicadores-execucao-penal">Indicadores</h2>
    __EXECUCAO_PENAL_INDICADORES__

    <h2 id="fontes-execucao-penal">Fontes</h2>
    <div class="rolagem">
      <table>
        <thead><tr><th>Fonte</th><th>Órgão</th><th>Periodicidade</th><th>Licença</th></tr></thead>
        <tbody><tr><td>Base sintética em formato SISDEPEN (demonstração)</td><td>odh (gerada localmente)</td><td>sob demanda</td><td>—</td></tr></tbody>
      </table>
    </div>

    <h2 id="evidencia-execucao-penal">Evidência</h2>
    <p class="miolo">Cada coleta guarda o endereço original, o instante da
    requisição e o hash SHA-256 do arquivo recebido. Quem quiser conferir baixa o
    mesmo arquivo, calcula o hash e compara com a linha correspondente.</p>
    <div class="rolagem">
      <table>
        <thead><tr><th>Instante (UTC)</th><th>Endereço</th><th>Origem</th>
        <th>SHA-256</th><th>Bytes</th></tr></thead>
        <tbody><tr><td class="mono">2026-08-22T13:35:17+00:00</td><td class="mono"><a href="odh://synthetic/sisdepen/2025-S1">odh://synthetic/sisdepen/2025-S1</a></td><td>synthetic</td><td class="mono">6bb8655e804d5997…</td><td class="numero mono">7.423</td></tr></tbody>
      </table>
    </div>
    <h4>Âncora do livro de evidência</h4>
    <p class="ancora">de577be657241de3181b66df7b25bc4e94d19f52ca17a55f04e6dae9f6074462</p>
    <p class="miolo">Publique essa âncora junto do relatório. Qualquer alteração
    posterior em qualquer registro do livro muda esse valor, e
    <span class="mono">odh verificar</span> aponta onde.</p>

  </section>

  <!-- ============================================ TEMA: AMBIENTE URBANO -->
  <section class="tema-painel" id="tema-ambiente-urbano" hidden>

    <h2 id="objeto-ambiente-urbano">Objeto</h2>
    <div class="miolo">
      <p>Esta temática ainda não tem indicador implementado. A proposta é a
      mesma do restante do observatório: medir a <em>autodescrição</em> que o
      poder público produz sobre direitos humanos no meio ambiente urbano em
      Minas Gerais — saneamento, moradia, remoções e riscos ambientais em áreas
      urbanas são candidatos de escopo, não fontes já mapeadas — e colocá-la ao
      lado do dever jurídico correspondente.</p>
      <p>Nenhum sistema de informação foi mapeado e registrado como fonte
      candidata ainda. Isso é pré-requisito para qualquer indicador entrar aqui,
      na mesma convenção usada pela temática Execução Penal: um sistema entra
      como <strong>Candidato</strong> em <span class="mono">docs/sistemas.md</span>
      antes de virar adaptador.</p>
    </div>

    <h2 id="ressalvas-ambiente-urbano">O que estas fontes não medem</h2>
    <div class="card-vazio">Nenhuma fonte pública foi registrada para esta
    temática. Esta seção fica propositalmente sem conteúdo até que isso
    aconteça — o observatório não publica ressalva de fonte que ainda não
    existe.</div>

    <h2 id="indicadores-ambiente-urbano">Indicadores</h2>
    <div class="card-vazio"><strong>Nenhum indicador implementado nesta
    temática.</strong> Um indicador só entra aqui depois que uma fonte é mapeada
    como candidata, ganha adaptador testado e recebe vínculo normativo com
    justificativa escrita — o mesmo processo que já valeu para a temática
    Execução Penal.</div>

    <h2 id="fontes-ambiente-urbano">Fontes</h2>
    <div class="card-vazio">Nenhuma fonte registrada.</div>

    <h2 id="evidencia-ambiente-urbano">Evidência</h2>
    <div class="card-vazio">Sem coleta registrada — não há o que auditar
    ainda.</div>

  </section>

  <!-- ============================================= TEMA: AMBIENTE RURAL -->
  <section class="tema-painel" id="tema-ambiente-rural" hidden>

    <h2 id="objeto-ambiente-rural">Objeto</h2>
    <div class="miolo">
      <p>Esta temática ainda não tem indicador implementado. A proposta é medir
      a <em>autodescrição</em> que o poder público produz sobre direitos humanos
      no meio ambiente rural em Minas Gerais — conflitos fundiários, populações
      tradicionais, acesso à água e ao território são candidatos de escopo, não
      fontes já mapeadas — e colocá-la ao lado do dever jurídico
      correspondente.</p>
      <p>Impacto de atividade minerária sobre populações rurais pode cruzar com
      o que o <strong>MINERVA</strong> (observatório irmão, mesmo padrão de
      família) mede sobre a atividade minerária em si — mas cada observatório
      mantém seu próprio corpus normativo e suas próprias fontes; nenhum vínculo
      é herdado automaticamente de um para o outro.</p>
      <p>Nenhum sistema de informação foi mapeado e registrado como fonte
      candidata ainda.</p>
    </div>

    <h2 id="ressalvas-ambiente-rural">O que estas fontes não medem</h2>
    <div class="card-vazio">Nenhuma fonte pública foi registrada para esta
    temática.</div>

    <h2 id="indicadores-ambiente-rural">Indicadores</h2>
    <div class="card-vazio"><strong>Nenhum indicador implementado nesta
    temática.</strong> Mesmo processo de entrada da temática Execução
    Penal se aplica aqui.</div>

    <h2 id="fontes-ambiente-rural">Fontes</h2>
    <div class="card-vazio">Nenhuma fonte registrada.</div>

    <h2 id="evidencia-ambiente-rural">Evidência</h2>
    <div class="card-vazio">Sem coleta registrada — não há o que auditar
    ainda.</div>

  </section>

</div>

<footer class="rodape-eu">
  <div class="rodape-interno">
    <div>
      <h5>BR-MG-ObservatoriumHumanitarium</h5>
      <p>Observatório de segunda ordem para o Estado de Minas Gerais, organizado
      em temáticas: Execução Penal, Direitos Humanos no Meio Ambiente Urbano e
      Direitos Humanos no Meio Ambiente Rural. Confronta a autodescrição estatal
      com o dever jurídico correspondente. Não afirma violação de direito.</p>
    </div>
    <div>
      <h5>Fontes oficiais das citações</h5>
      <ul>
        <li>Planalto/Casa Civil — lei e decreto federal</li>
        <li>Portal do STF — jurisprudência</li>
        <li>Corte Interamericana de Direitos Humanos — resoluções de supervisão</li>
      </ul>
    </div>
    <div>
      <h5>Verificação</h5>
      <ul>
        <li><span class="mono">odh verificar</span> — cadeia de evidência</li>
        <li><span class="mono">odh normativo --pendentes</span> — citações a conferir</li>
        <li><span class="mono">odh fontes</span> — fontes registradas</li>
      </ul>
    </div>
  </div>
  <div class="rodape-base">
    Gerado por observatorio-dh &nbsp;·&nbsp; dados públicos &nbsp;·&nbsp;
    a verificação independente é o ponto: refaça as contas
  </div>
</footer>

<script>
(function(){
  var TEMAS = ["tema-execucao-penal", "tema-ambiente-urbano", "tema-ambiente-rural"];

  function ativarTema(id){
    TEMAS.forEach(function(t){
      var painel = document.getElementById(t);
      var botao = document.querySelector('.tab-tema[data-tema="' + t + '"]');
      if (!painel || !botao) return;
      if (t === id){
        painel.hidden = false;
        botao.setAttribute("aria-selected", "true");
      } else {
        painel.hidden = true;
        botao.setAttribute("aria-selected", "false");
      }
    });
  }

  document.querySelectorAll(".tab-tema").forEach(function(botao){
    botao.addEventListener("click", function(){
      ativarTema(botao.getAttribute("data-tema"));
    });
  });

  var INDICE = [
    {"titulo": "Objeto", "tipo": "seção · execução penal", "ancora": "objeto-execucao-penal", "tema": "tema-execucao-penal"},
    {"titulo": "O que estas fontes não medem", "tipo": "seção · execução penal", "ancora": "ressalvas-execucao-penal", "tema": "tema-execucao-penal"},
    {"titulo": "Fontes", "tipo": "seção · execução penal", "ancora": "fontes-execucao-penal", "tema": "tema-execucao-penal"},
    {"titulo": "Evidência", "tipo": "seção · execução penal", "ancora": "evidencia-execucao-penal", "tema": "tema-execucao-penal"},
    {"titulo": "Taxa de ocupação carcerária", "tipo": "indicador", "ancora": "taxa_ocupacao", "tema": "tema-execucao-penal"},
    {"titulo": "Déficit de vagas", "tipo": "indicador", "ancora": "deficit_vagas", "tema": "tema-execucao-penal"},
    {"titulo": "Estabelecimentos na base do ciclo", "tipo": "indicador", "ancora": "cobertura_informacao", "tema": "tema-execucao-penal"},
    {"titulo": "Direitos Humanos no Meio Ambiente Urbano", "tipo": "temática · candidato", "ancora": "objeto-ambiente-urbano", "tema": "tema-ambiente-urbano"},
    {"titulo": "Direitos Humanos no Meio Ambiente Rural", "tipo": "temática · candidato", "ancora": "objeto-ambiente-rural", "tema": "tema-ambiente-rural"}
  ];
  var campo = document.getElementById("campo-busca");
  var caixa = document.getElementById("resultados-busca");
  if (!campo || !caixa) return;

  function normaliza(t){
    return t.normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").toLowerCase();
  }

  function renderiza(consulta){
    var termo = normaliza(consulta.trim());
    if (!termo){ caixa.hidden = true; caixa.innerHTML = ""; return; }
    var achados = INDICE.filter(function(item){
      return normaliza(item.titulo).indexOf(termo) !== -1;
    }).slice(0, 10);
    if (!achados.length){
      caixa.innerHTML = '<div class="vazio">Nada encontrado para "' +
        consulta.replace(/</g, "&lt;") + '".</div>';
    } else {
      caixa.innerHTML = achados.map(function(item, i){
        return '<a href="#' + item.ancora + '" data-tema="' + item.tema + '" data-idx="' + i + '">' + item.titulo +
          '<span class="tipo">' + item.tipo + '</span></a>';
      }).join("");
    }
    caixa.hidden = false;
  }

  campo.addEventListener("input", function(){ renderiza(campo.value); });
  campo.addEventListener("focus", function(){ if (campo.value) renderiza(campo.value); });
  campo.addEventListener("keydown", function(ev){
    if (ev.key === "Enter"){
      var primeiro = caixa.querySelector("a");
      if (primeiro){
        ativarTema(primeiro.getAttribute("data-tema"));
        window.location.hash = primeiro.getAttribute("href");
        caixa.hidden = true;
      }
    }
    if (ev.key === "Escape"){ caixa.hidden = true; campo.blur(); }
  });
  caixa.addEventListener("click", function(ev){
    var a = ev.target.closest("a[data-tema]");
    if (a) ativarTema(a.getAttribute("data-tema"));
    caixa.hidden = true;
  });
  document.addEventListener("click", function(ev){
    if (!ev.target.closest(".busca")) caixa.hidden = true;
  });
})();
</script>
</body>
</html>
"""
