#!/usr/bin/env python3
"""
sisdepen_mg_direitos_femininos.py

Lê o SISDEPEN "base única" (nacional, todos os ciclos), filtra para
Minas Gerais e recorta as colunas que (a) são desagregadas por sexo
feminino OU são inerentemente exclusivas de mulheres na pesquisa, E
(b) correspondem a um bloco tematicamente ligado a direito já
positivado (LEP, CF/88, CADH) — não apenas capacidade física/estrutura
administrativa sem corte de gênero.

Critério de seleção documentado bloco a bloco em BLOCOS_DIREITOS abaixo.
Nada é inventado: cada bloco mantido cita o dispositivo legal que o
justifica como "direito penitenciário", não só "dado sobre mulheres".

Saídas:
  sisdepen_mg_bruto.csv                 -- MG, todas as colunas, todos os 19 ciclos (2016/2-2025/2)
  sisdepen_mg_direitos_femininos_2025-2.csv   -- recorte curado, ciclo mais recente (retrato atual)
  sisdepen_mg_direitos_femininos_serie.csv    -- mesmo recorte, agregado MG por ciclo (série 2016-2025)
  sisdepen_mg_resumo.json               -- números-resumo + hash de evidência
"""
import csv, hashlib, json, re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
BRUTO = BASE / "sisdepen_mg_bruto.csv"
# Caminho de quando este script rodou (sandbox desta sessão). Ajuste para o
# caminho local do arquivo baixado do SISDEPEN antes de rodar de novo —
# o .xlsx original (71 MB) não é distribuído junto do projeto.
FONTE_XLSX = Path("/mnt/user-data/uploads/sisdepen_baseunica_2025-2_25032026-163420.xlsx")

ID_COLS = ["ciclo", "Ano", "Referência", "ID", "Nome do Estabelecimento",
           "UF", "Situação do Estabelecimento", "Município", "Código IBGE"]

# ---------------------------------------------------------------------
# Blocos mantidos e o dispositivo que os torna "direito penitenciário"
# (não apenas dado administrativo). Blocos fora desta lista existem no
# bruto mas ficam de fora do recorte de direitos por não terem corte de
# gênero na pesquisa (ex.: módulos de saúde/educação físicos, LGBT,
# idosos, indígenas, estrangeiros — protegem outros marcadores, não o
# de gênero) ou por serem sobre o quadro de servidores, não sobre quem
# está privado de liberdade.
# ---------------------------------------------------------------------
BLOCOS_DIREITOS = {
    "1.3":  "LEP art. 82, §1º — separação de custódia por sexo",
    "4.1":  "LEP arts. 84–87 — regime e situação processual",
    "4.2":  "CPP art. 316/LEP art. 41 — excesso de prazo da prisão provisória",
    "4.3":  "LEP art. 112 — progressão de regime (mesmo campo normativo de ADPF 347/SV 56)",
    "4.4":  "LEP art. 41, XVI — direito ao atestado de pena a cumprir",
    "4.5":  "LEP art. 41 + direito à vida (óbitos) e benefícios (saída temporária, art. 122)",
    "5.1":  "perfil etário — insumo para políticas de execução penal diferenciadas",
    "5.2":  "perfil racial — CF art. 5º, caput c/c monitoramento de seletividade penal",
    "5.3":  "procedência — planejamento de reintegração territorial",
    "5.4":  "estado civil — direito à visita do cônjuge/companheira, LEP art. 41, X",
    "5.5":  "LEP + Convenção sobre Direitos das Pessoas com Deficiência — acessibilidade",
    "5.6":  "LEP art. 41, VII — direito à instrução escolar",
    "5.7":  "LEP art. 41 + direito à documentação civil (reintegração)",
    "5.8":  "CADH + direito à assistência consular de estrangeiras (resumo, sem detalhe por país)",
    "5.9":  "LEP art. 83, §2º e art. 89 — berçário/creche/gestante-lactante (exclusivo mulheres)",
    "5.10": "LEP art. 83, §2º — vínculo materno-filial",
    "5.11": "LEP art. 41, X — direito à visita",
    "5.12": "direito à correta individualização da pena",
    "5.13": "direito à correta individualização da pena (pena remanescente)",
    "5.14": "perfil de tipificação — insumo para políticas de descarcerização",
    "6.1":  "LEP art. 41, II — direito ao trabalho",
    "6.2":  "LEP art. 29 — remuneração do trabalho",
    "6.3":  "LEP art. 41, VII + Lei 12.433/2011 — educação e remição pelo estudo",
    "6.4":  "LEP arts. 28/41 — trabalho e estudo simultâneos",
    "6.5":  "Lei 8.213/1991 — auxílio-reclusão (proteção da família)",
    "6.6":  "LEP art. 14 + art. 41, VII — direito à saúde",
    "6.7":  "LEP art. 14 — vigilância epidemiológica/direito à saúde",
    "6.8":  "direito à vida — mortalidade no cárcere",
    "7.3":  "LEP art. 41, X — direito à visita",
}

# blocos inerentemente exclusivos de mulheres na própria pesquisa
# (não têm sufixo "Feminino" porque só existem para estabelecimentos
# com vagas femininas) -- mantidos inteiros, sem exigir o sufixo.
BLOCOS_SO_MULHERES = {"2.1", "2.2", "2.3", "3.2", "5.9"}

# dentro do bloco 5.8 (nacionalidade), a pesquisa abre uma coluna por
# país (mais de 150). Mantemos só o nível "direito" -- nato/
# naturalizado/estrangeiro/sem informação -- e descartamos o
# detalhamento por país, que é demografia, não direito.
NACIONALIDADE_RESUMO = {
    "5.8 Quantidade de pessoas privadas de liberdade por nacionalidade | Brasileiro nato | Feminino",
    "5.8 Quantidade de pessoas privadas de liberdade por nacionalidade | Brasileiro naturalizado | Feminino",
    "5.8 Quantidade de pessoas privadas de liberdade por nacionalidade | Estrangeiros - total | Feminino",
    "5.8 Quantidade de pessoas privadas de liberdade por nacionalidade | Sem informação sobre a nacionalidade | Feminino",
}


def bloco_de(header: str) -> str | None:
    m = re.match(r'^(\d+\.\d+)\s', header)
    return m.group(1) if m else None


def selecionar_colunas(header: list[str]) -> list[str]:
    mantidas = list(ID_COLS)
    for h in header:
        if h in ID_COLS:
            continue
        b = bloco_de(h)
        if b is None:
            continue
        if b == "5.8":
            if h in NACIONALIDADE_RESUMO:
                mantidas.append(h)
            continue
        if b in BLOCOS_SO_MULHERES:
            mantidas.append(h)
            continue
        if b in BLOCOS_DIREITOS and ("Feminino" in h or "Fem." in h):
            mantidas.append(h)
    return mantidas


def to_num(v):
    if v in (None, "", "None"):
        return None
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return None


def main():
    with open(BRUTO, encoding="utf-8") as f:
        r = csv.reader(f)
        header = next(r)
        rows = list(r)

    idx = {h: i for i, h in enumerate(header)}
    colunas = selecionar_colunas(header)
    print(f"Colunas no bruto: {len(header)}  |  colunas no recorte de direitos: {len(colunas)}")

    # ---- retrato atual: ciclo mais recente (2025/2) ----
    ref_recente = max(row[idx["Referência"]] for row in rows)
    linhas_recentes = [row for row in rows if row[idx["Referência"]] == ref_recente]
    print(f"Referência mais recente: {ref_recente}  |  estabelecimentos MG nesse ciclo: {len(linhas_recentes)}")

    out_path = BASE / f"sisdepen_mg_direitos_femininos_{ref_recente.replace('/', '-')}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(colunas)
        for row in linhas_recentes:
            w.writerow([row[idx[c]] for c in colunas])
    print(f"Escrito: {out_path}")

    # ---- série histórica: agregado MG por ciclo (soma dos campos numéricos) ----
    campos_numericos = [c for c in colunas if c not in ID_COLS]
    por_ciclo = defaultdict(lambda: defaultdict(float))
    contagem_estabelecimentos = defaultdict(int)
    for row in rows:
        ref = row[idx["Referência"]]
        contagem_estabelecimentos[ref] += 1
        for c in campos_numericos:
            v = to_num(row[idx[c]])
            if v is not None:
                por_ciclo[ref][c] += v

    serie_path = BASE / "sisdepen_mg_direitos_femininos_serie.csv"
    with open(serie_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Referência", "estabelecimentos_MG"] + campos_numericos)
        for ref in sorted(por_ciclo, key=lambda r: tuple(int(x) for x in r.split("/"))):
            linha = [ref, contagem_estabelecimentos[ref]]
            for c in campos_numericos:
                val = por_ciclo[ref].get(c, 0.0)
                if val is None:
                    linha.append("")
                elif val == int(val):
                    linha.append(int(val))
                else:
                    linha.append(val)
            w.writerow(linha)
    print(f"Escrito: {serie_path}")

    # ---- resumo + evidência ----
    def soma(col):
        if col not in idx:
            return None
        return sum((to_num(row[idx[col]]) or 0) for row in linhas_recentes)

    def conta_sim(col):
        if col not in idx:
            return None
        return sum(1 for row in linhas_recentes if row[idx[col]] and row[idx[col]].startswith("Sim"))

    pop_fem_4_1_cols = [c for c in colunas if c.startswith("4.1 População prisional |") and c.endswith("Feminino")]
    populacao_feminina_total = sum(soma(c) or 0 for c in pop_fem_4_1_cols)

    obitos_fem_6_8_cols = [c for c in colunas if c.startswith("6.8 Mortalidade") and c.endswith("Feminino")]
    obitos_femininos_total = sum(soma(c) or 0 for c in obitos_fem_6_8_cols)

    resumo = {
        "fonte": {
            "arquivo_original": FONTE_XLSX.name,
            "sha256": hashlib.sha256(FONTE_XLSX.read_bytes()).hexdigest(),
        },
        "recorte": {
            "uf": "MG",
            "ciclos_disponiveis_MG": sorted(contagem_estabelecimentos, key=lambda r: tuple(int(x) for x in r.split("/"))),
            "ciclo_retrato_atual": ref_recente,
            "estabelecimentos_MG_ciclo_atual": len(linhas_recentes),
            "colunas_bruto": len(header),
            "colunas_recorte_direitos": len(colunas),
        },
        "numeros_MG_ciclo_atual": {
            "populacao_feminina_total": populacao_feminina_total,
            "estabelecimentos_com_cela_gestante_dormitorio": conta_sim(
                "2.1 Há cela adequada/ dormitório para gestantes? (apenas para estabelecimentos com vagas para mulheres)"),
            "estabelecimentos_com_bercario_ou_centro_materno_infantil": conta_sim(
                "2.2 Possui berçário e/ou centro de referência materno-infantil? (apenas para estabelecimentos com vagas para mulheres)"),
            "estabelecimentos_com_creche": conta_sim(
                "2.3 Possui creche? (apenas para estabelecimentos com vagas para mulheres)"),
            "mulheres_com_atestado_de_pena_atualizado": soma(
                "4.4 O estabelecimento recebe o atestado de pena a cumprir? | Quantas pessoas privadas de liberdade sentenciadas que estão no estabelecimento possuem o atestado de pena atualizado arquivado no prontuário? | Feminino"),
            "consultas_medicas_mulheres_total_periodo": (
                (soma("6.6 Informações da área de saúde - total do período | Consultas médicas realizadas externamente | Feminino") or 0)
                + (soma("6.6 Informações da área de saúde - total do período | Consultas médicas realizadas no estabelecimento | Feminino") or 0)
            ),
            "obitos_femininos_total_periodo": obitos_femininos_total,
        },
        "metodologia": {
            "blocos_incluidos": BLOCOS_DIREITOS,
            "blocos_exclusivos_mulheres_sem_sufixo": sorted(BLOCOS_SO_MULHERES),
            "nacionalidade_reduzida_a_resumo": True,
        },
    }

    resumo_path = BASE / "sisdepen_mg_resumo.json"
    resumo_path.write_text(json.dumps(resumo, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Escrito: {resumo_path}")


if __name__ == "__main__":
    main()
