#!/usr/bin/env python3
"""
gerar_dados_mapa.py

Agrega sisdepen_mg_bruto.csv por município (mulheres em custódia física,
infraestrutura materna declarada) e produz o array de dados que a barra
de mapa de index.html consome. Roda de novo quando um novo ciclo do
SISDEPEN sair -- ajuste REFERENCIA abaixo para o ciclo desejado.

As coordenadas em COORDENADAS são aproximações de sede de município
(não conferidas contra uma fonte cartográfica única -- ver ressalva na
própria barra de mapa em index.html). Se um novo município aparecer
como tendo mulheres em custódia, adicione a coordenada aqui antes de
rodar -- o script avisa e não inventa coordenada.

Uso:
    python3 gerar_dados_mapa.py > municipios_mapa.js.txt
    # cole o conteúdo no lugar do array MUNICIPIOS em index.html
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
BRUTO = BASE / "sisdepen_mg_bruto.csv"
REFERENCIA = "2025/2"

# Sede do município -- aproximado, ver ressalva no docstring acima.
COORDENADAS = {
    "Belo Horizonte": (-19.9167, -43.9345), "Juiz de Fora": (-21.7642, -43.3467),
    "Ribeirão das Neves": (-19.7669, -44.0867), "Timóteo": (-19.5828, -42.6467),
    "Santa Rita do Sapucaí": (-22.2500, -45.7000), "Uberlândia": (-18.9186, -48.2772),
    "Governador Valadares": (-18.8511, -41.9494), "Teófilo Otoni": (-17.8578, -41.5050),
    "Presidente Olegário": (-18.4178, -46.4178), "Três Corações": (-21.6944, -45.2578),
    "Conselheiro Lafaiete": (-20.6608, -43.7864), "Pará de Minas": (-19.8611, -44.6081),
    "Divinópolis": (-20.1389, -44.8839), "São João Del Rei": (-21.1356, -44.2619),
    "Montes Claros": (-16.7350, -43.8617), "Frutal": (-20.0247, -48.9400),
    "Uberaba": (-19.7483, -47.9319), "Rio Piracicaba": (-19.8975, -43.1794),
    "Alfenas": (-21.4292, -45.9475), "Itaúna": (-20.0725, -44.5786),
    "Pouso Alegre": (-22.2300, -45.9364), "Unaí": (-16.3578, -46.9061),
    "Vespasiano": (-19.6928, -43.9236), "João Pinheiro": (-17.7425, -46.1731),
    "Barbacena": (-21.2256, -43.7736), "Curvelo": (-18.7558, -44.4308),
    "Capelinha": (-17.6975, -42.5142), "Diamantina": (-18.2428, -43.6008),
    "Araxá": (-19.5928, -46.9408), "Iturama": (-19.7267, -50.1975),
    "Passos": (-20.7181, -46.6106), "São Joaquim de Bicas": (-19.9581, -44.3128),
    "Almenara": (-16.1811, -40.6969), "Conselheiro Pena": (-19.1636, -41.4681),
    "Janaúba": (-15.8019, -43.3106), "Serro": (-18.6042, -43.3789),
    "São Lourenço": (-22.1167, -45.0500), "Varginha": (-21.5550, -45.4300),
    "Andradas": (-22.0644, -46.5686), "Bom Despacho": (-19.7439, -45.2517),
    "Itajubá": (-22.4256, -45.4528), "Malacacheta": (-17.8531, -42.0681),
    "Paracatu": (-17.2219, -46.8747), "Pirapora": (-17.3458, -44.9422),
    "Piumhi": (-20.4728, -45.9611), "Ubá": (-21.1189, -42.9436),
}


def to_num(v):
    try:
        return int(v)
    except (ValueError, TypeError):
        return 0


def main():
    with open(BRUTO, encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows = [row for row in r if row["Referência"] == REFERENCIA]

    if not rows:
        sys.exit(f"Nenhuma linha para o ciclo {REFERENCIA} -- confira REFERENCIA no topo do script.")

    pop_fem_cols = [c for c in rows[0].keys()
                    if c.startswith("4.1 População prisional |") and c.endswith("Feminino")]

    por_municipio = defaultdict(lambda: {"pop": 0, "estabs": 0, "ibge": None,
                                          "bercario": 0, "creche": 0, "cela_gest": 0})
    for row in rows:
        if row["Tipo de Recolhimento"] != "Cela física":
            continue
        total = sum(to_num(row[c]) for c in pop_fem_cols)
        if total <= 0:
            continue
        d = por_municipio[row["Município"]]
        d["pop"] += total
        d["estabs"] += 1
        d["ibge"] = row["Código IBGE"]
        if row["2.1 Há cela adequada/ dormitório para gestantes? (apenas para estabelecimentos com vagas para mulheres)"].startswith("Sim"):
            d["cela_gest"] += 1
        if row["2.2 Possui berçário e/ou centro de referência materno-infantil? (apenas para estabelecimentos com vagas para mulheres)"].startswith("Sim"):
            d["bercario"] += 1
        if row["2.3 Possui creche? (apenas para estabelecimentos com vagas para mulheres)"].startswith("Sim"):
            d["creche"] += 1

    faltando = set(por_municipio) - set(COORDENADAS)
    if faltando:
        sys.exit(f"Sem coordenada para: {sorted(faltando)} -- adicione em COORDENADAS antes de gerar.")

    registros = []
    for nome, d in por_municipio.items():
        lat, lon = COORDENADAS[nome]
        registros.append({
            "nome": nome, "ibge": int(d["ibge"]), "lat": lat, "lon": lon,
            "pop": d["pop"], "estabs": d["estabs"],
            "bercario": d["bercario"] > 0, "creche": d["creche"] > 0,
            "celaGestante": d["cela_gest"] > 0,
        })
    registros.sort(key=lambda r: -r["pop"])

    linhas = []
    for r in registros:
        linhas.append(
            '{nome:"%s",ibge:%d,lat:%s,lon:%s,pop:%d,estabs:%d,bercario:%s,creche:%s,celaGestante:%s}' % (
                r["nome"].replace('"', '\\"'), r["ibge"], r["lat"], r["lon"],
                r["pop"], r["estabs"],
                "true" if r["bercario"] else "false",
                "true" if r["creche"] else "false",
                "true" if r["celaGestante"] else "false",
            )
        )
    print("[")
    print("    " + ",\n    ".join(linhas))
    print("  ]")
    print(f"\n// {len(registros)} municípios · {sum(r['pop'] for r in registros)} mulheres em custódia física"
          f" · ciclo {REFERENCIA}", file=sys.stderr)


if __name__ == "__main__":
    main()
