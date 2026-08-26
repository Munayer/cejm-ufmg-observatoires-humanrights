#!/usr/bin/env python3
"""Monta a prévia index.html a partir do painel existente (base.html)
mais as mudanças de escopo pedidas: MG em primeiro plano, menu de
Temáticas, e citações normativas linkadas à fonte oficial.

Não inventa dado novo: reaproveita literalmente as três seções de
indicador já existentes (taxa_ocupacao, deficit_vagas,
cobertura_informacao) e as reorganiza. As duas temáticas novas entram
como "Candidato" (sem indicador, sem fonte) — mesma convenção de
sistemas.md — porque não há fonte real registrada para elas ainda.
"""
from __future__ import annotations
import html
import re
from pathlib import Path

BASE = Path(__file__).parent / "base.html"
ESTILO = Path(__file__).parent / "estilo.css"
SAIDA = Path(__file__).parent / "index.html"

# ---------------------------------------------------------------------
# Mapa de fonte oficial por citação normativa.
#
# Regra que este script segue (e que a página declara ao leitor):
# só o Planalto/Casa Civil publica lei e decreto federal. Jurisprudência
# do STF mora no portal do próprio STF; resolução da Corte IDH mora em
# corteidh.or.cr. Link para o texto errado é pior do que nenhum link,
# então uma citação sem par verificado aqui fica sem link e ganha o
# selo "fonte oficial: a localizar" em vez de apontar para qualquer
# coisa. Cada URL abaixo foi conferida em 24/08/2026.
# ---------------------------------------------------------------------
FONTES_OFICIAIS = [
    ("CADH, art.", "https://www.planalto.gov.br/ccivil_03/decreto/d0678.htm",
     "Planalto — Decreto 678/1992"),
    ("CF/88", "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm",
     "Planalto — Constituição Federal"),
    ("Lei 7.210/1984 (LEP)", "https://www.planalto.gov.br/ccivil_03/leis/l7210.htm",
     "Planalto — Lei 7.210/1984"),
    ("STF, ADPF 347", "https://portal.stf.jus.br/processos/detalhe.asp?incidente=4783560",
     "Portal STF — acompanhamento processual"),
    ("STF, Súmula Vinculante 56",
     "https://www.stf.jus.br/arquivo/cms/jurisprudenciaSumulaVinculante/anexo/2020SumulaVinculante1a29e31a58Resumidocapaecontedo.pdf",
     "Portal STF — texto compilado das súmulas vinculantes"),
    ("Corte IDH, Assunto Complexo Penitenciário de Curado",
     "https://www.cnj.jus.br/poder-judiciario/relacoes-internacionais/monitoramento-e-fiscalizacao-das-decisoes-da-corte-idh/jurisprudencia-corte-idh/medidas-provisorias/",
     "CNJ — índice de medidas provisórias da Corte IDH sobre o Brasil"),
    ("Corte IDH, Assunto Instituto Penal Plácido de Sá Carvalho",
     "https://www.cnj.jus.br/poder-judiciario/relacoes-internacionais/monitoramento-e-fiscalizacao-das-decisoes-da-corte-idh/jurisprudencia-corte-idh/medidas-provisorias/",
     "CNJ — índice de medidas provisórias da Corte IDH sobre o Brasil"),
    ("Corte IDH, Caso Favela Nova Brasília",
     "https://www.corteidh.or.cr/docs/casos/articulos/seriec_333_por.pdf",
     "Corte IDH — sentença do caso (texto oficial)"),
    ("ONU — Regras de Nelson Mandela",
     "https://www.unodc.org/documents/justice-and-prison-reform/Nelson_Mandela_Rules-P-ebook.pdf",
     "UNODC — texto oficial das Regras de Mandela"),
]


def linkar_citacao(citacao_esc: str) -> str:
    """Recebe a citação já com html.escape aplicado e devolve <a> se
    houver fonte verificada, senão o texto puro + selo de pendência."""
    for prefixo, url, rotulo in FONTES_OFICIAIS:
        if citacao_esc.startswith(html.escape(prefixo)):
            return (f'<a href="{url}" target="_blank" rel="noopener" '
                    f'class="lig-oficial" title="{html.escape(rotulo)}">{citacao_esc}</a>')
    return f'{citacao_esc} <span class="selo-a-localizar">fonte oficial: a localizar</span>'


def transformar_devers(bloco: str) -> str:
    """Substitui cada <strong>citação</strong> por versão linkada."""
    def sub(m):
        citacao = m.group(1)
        return f'<div class="fonte-legal"><strong>{linkar_citacao(citacao)}</strong>'
    return re.sub(r'<div class="fonte-legal"><strong>(.*?)</strong>', sub, bloco)


def extrair_mg(serie_html: str) -> str | None:
    m = re.search(
        r'<div class="registro"><span class="lugar">Minas Gerais \(MG\)</span>'
        r'(.*?)</div>\s*(?=<div class="registro"|$)',
        serie_html, re.S)
    if not m:
        return None
    return m.group(0)


def montar_secao_indicador(sid: str, corpo: str) -> str:
    corpo = transformar_devers(corpo)

    # localizar o bloco <div class="serie">...</div> inteiro
    m = re.search(r'(<div class="serie">)(.*)(</div>\n\s*<h4>Como)', corpo, re.S)
    if not m:
        return corpo  # não deveria acontecer, mas falha alta em vez de mascarar

    antes, serie_interna, depois = m.group(1), m.group(2), m.group(3)

    mg_bloco = extrair_mg(serie_interna)
    destaque = ""
    if mg_bloco:
        destaque = (
            '<div class="destaque-mg">'
            '<span class="destaque-rotulo">Minas Gerais</span>'
            f'<div class="destaque-registro">{mg_bloco}</div>'
            '</div>'
        )

    n_registros = len(re.findall(r'class="registro', serie_interna))
    bloco_completo = (
        f'{destaque}'
        f'<details class="ver-todos"><summary>Ver Minas Gerais ao lado do Brasil '
        f'e das demais unidades da federação ({n_registros} registros)</summary>'
        f'<div class="serie">{serie_interna}</div>'
        f'</details>'
    )

    corpo_novo = corpo[:m.start()] + bloco_completo + '\n  <h4>Como' + corpo[m.end():]
    return corpo_novo


def main():
    base = BASE.read_text(encoding="utf-8")
    estilo = ESTILO.read_text(encoding="utf-8")

    secoes = dict(re.findall(
        r'<section class="indicador" id="(\w+)">(.*?)</section>', base, re.S))

    partes = []
    for sid in ("taxa_ocupacao", "deficit_vagas", "cobertura_informacao"):
        corpo = montar_secao_indicador(sid, secoes[sid])
        # recupera h3/qualificacao/pergunta originais (já estão em `corpo`)
        partes.append(f'<section class="indicador" id="{sid}">{corpo}</section>')
    execucao_penal_indicadores = "\n".join(partes)

    from modelo_html import MODELO
    saida = (MODELO
             .replace("__ESTILO__", estilo)
             .replace("__EXECUCAO_PENAL_INDICADORES__", execucao_penal_indicadores))
    SAIDA.write_text(saida, encoding="utf-8")
    print(f"Escrito: {SAIDA} ({len(saida):,} bytes)")


if __name__ == "__main__":
    main()
