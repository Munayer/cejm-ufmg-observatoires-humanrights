# Links oficiais das citações normativas

Conferidos em 24/08/2026. Cada linha diz **onde** o link aponta e **por quê**
esse é o portal certo — não o Planalto por padrão, o portal que de fato
publica aquele tipo de ato.

| Citação | Fonte oficial | Por que este portal |
| --- | --- | --- |
| CADH, art. 2 / 5.1 / 5.2 / 5.6 | [planalto.gov.br/ccivil_03/decreto/d0678.htm](https://www.planalto.gov.br/ccivil_03/decreto/d0678.htm) | Decreto 678/1992, que promulga a Convenção no direito interno — ato do Executivo, mora no Planalto/Casa Civil |
| CF/88, art. 5º, XLIX | [planalto.gov.br/ccivil_03/constituicao/constituicao.htm](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm) | Texto oficial da Constituição, mantido pela Casa Civil |
| Lei 7.210/1984 (LEP), art. 85 | [planalto.gov.br/ccivil_03/leis/l7210.htm](https://www.planalto.gov.br/ccivil_03/leis/l7210.htm) | Lei federal — Planalto/Casa Civil |
| STF, ADPF 347 | [portal.stf.jus.br/processos/detalhe.asp?incidente=4783560](https://portal.stf.jus.br/processos/detalhe.asp?incidente=4783560) | Jurisprudência do STF não é publicada no Planalto; acompanhamento processual mora no portal do próprio Tribunal |
| STF, Súmula Vinculante 56 | [stf.jus.br — compilado de súmulas vinculantes (PDF)](https://www.stf.jus.br/arquivo/cms/jurisprudenciaSumulaVinculante/anexo/2020SumulaVinculante1a29e31a58Resumidocapaecontedo.pdf) | Texto oficial compilado pelo próprio STF |
| Corte IDH, Curado | [CNJ — índice de medidas provisórias da Corte IDH sobre o Brasil](https://www.cnj.jus.br/poder-judiciario/relacoes-internacionais/monitoramento-e-fiscalizacao-das-decisoes-da-corte-idh/jurisprudencia-corte-idh/medidas-provisorias/) | Há várias resoluções de supervisão ao longo dos anos (2014, 2016, 2018, 2023…); o índice do CNJ lista todas com data, evitando linkar uma resolução específica errada. Os originais em espanhol/português ficam em `corteidh.or.cr/docs/medidas/` |
| Corte IDH, Plácido de Sá Carvalho | mesmo índice do CNJ acima | mesma razão |
| Corte IDH, Favela Nova Brasília | [corteidh.or.cr — sentença do caso (PDF)](https://www.corteidh.or.cr/docs/casos/articulos/seriec_333_por.pdf) | Sentença de mérito, documento único (não é medida provisória com múltiplas resoluções) |
| ONU — Regras de Nelson Mandela | [UNODC — texto oficial (PDF)](https://www.unodc.org/documents/justice-and-prison-reform/Nelson_Mandela_Rules-P-ebook.pdf) | Texto das Regras publicado pelo UNODC, órgão que as administra |
| LEP, art. 83 §2º / art. 89 (mulheres — creche, berçário) | [planalto.gov.br/ccivil_03/leis/l7210.htm](https://www.planalto.gov.br/ccivil_03/leis/l7210.htm) | Mesma lei federal — Planalto/Casa Civil |
| Lei 12.433/2011 (remição de pena pelo estudo) | [planalto.gov.br — L12433](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12433.htm) | Lei federal — Planalto/Casa Civil |
| Lei 8.213/1991, art. 80 (auxílio-reclusão) | [planalto.gov.br — L8213 (consolidada)](https://www.planalto.gov.br/ccivil_03/leis/l8213cons.htm) | Lei federal — Planalto/Casa Civil |

## O que ainda falta

- Cada link acima aponta para o **documento correto**, não necessariamente
  para o **trecho exato** citado (artigo, considerando, ponto resolutivo).
  O selo `redação a conferir` que já existia continua valendo — conferir a
  redação linha a linha continua sendo trabalho de jurista, não deste
  script.
- Para as resoluções de Curado e Plácido de Sá Carvalho, o link genérico do
  CNJ é o ponto de partida seguro; trocar pelo PDF específico da resolução
  certa (ano certo) em `corteidh.or.cr/docs/medidas/` é o próximo passo, e
  exige confirmar qual resolução corresponde ao texto de `obrigacao` já
  escrito em `linkages.toml`.
- O repositório original menciona 18 pendências no total; este pacote só
  contém os 12 vínculos que aparecem nas três seções de indicador
  incluídas em `base.html`. As demais 6 não estavam neste envio.
