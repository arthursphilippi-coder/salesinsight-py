"""
SalesInsight PY - Análise de Dados de Vendas (Versão Simplificada)
==================================================================
Mini-Projeto Avaliativo - Módulo 01 (Semanas 01 a 05)
Usa apenas a biblioteca padrão do Python (csv, json, os, random, re, datetime).
"""

import csv
import json
import os
import random
import re
from datetime import datetime, timedelta

CAMINHO_CSV = "vendas.csv"
PASTA_SAIDA = "outputs"

# Mapeamento para garantir nomes de meses em português
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}


# ======================================================================
# RF01 e RF02: Gerar/Carregar e Inspecionar Dataset
# ======================================================================
def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    """Gera o dataset de vendas em CSV com alguns dados sujos propositais."""
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse", "Headset"]
    categorias = {
        "Notebook": "Computadores", "Smartphone": "Celulares", "Tablet": "Celulares",
        "Monitor": "Computadores", "Teclado": "Perifericos", "Mouse": "Perifericos", "Headset": "Perifericos"
    }
    precos = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800, "Monitor": 1200, "Teclado": 250, "Mouse": 120, "Headset": 350}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    colunas = ["id_venda", "data_venda", "cliente", "produto", "categoria", "regiao", "quantidade", "preco_unitario"]

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        for i in range(n_registros):
            prod = random.choice(produtos)
            qtd = random.randint(1, 10)
            prc = round(precos[prod] * random.uniform(0.85, 1.15), 2)
            dt = (data_inicio + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")
            cli = f"Cliente_{random.randint(1, 50):03d}"

            # Inserção de ruídos simples
            if random.random() < 0.05: qtd = ""
            if random.random() < 0.04: prc = ""
            if random.random() < 0.06: prod = f" {prod} "
            if random.random() < 0.03: dt = "DATA INVALIDA"
            if random.random() < 0.10: cli = cli.upper().replace("_", "-")

            escritor.writerow({
                "id_venda": i + 1, "data_venda": dt, "cliente": cli,
                "produto": prod, "categoria": categorias.get(prod.strip(), "Outros"),
                "regiao": random.choice(regioes), "quantidade": qtd, "preco_unitario": prc
            })
    print(f"Dataset gerado em '{caminho_csv}'.")


def carregar_dataset(caminho_csv):
    """Lê o arquivo CSV e retorna uma lista de dicionários."""
    with open(caminho_csv, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def inspecionar_dados(registros):
    """Exibe informações básicas da estrutura do dataset."""
    total = len(registros)
    colunas = list(registros[0].keys()) if registros else []
    nulos = {c: 0 for c in colunas}
    for r in registros:
        for c in colunas:
            if (r.get(c) or "").strip() == "":
                nulos[c] += 1

    print("\n=== INSPEÇÃO INICIAL ===")
    print(f"Total de registros: {total}")
    print(f"Colunas: {colunas}")
    print(f"Valores ausentes: {nulos}")
    print("Primeiros 3 registros:", registros[:3])

# ======================================================================
# RF03: Limpeza e Tratamento de Dados
# ======================================================================
def limpar_dados(registros):
    """Limpa textos, valida datas com datetime e padroniza clientes com regex."""
    relatorio = {"iniciais": len(registros), "removidos_data": 0, "removidos_nulos": 0, "finais": 0}
    limpos = []

    for r in registros:
        # Remover espaços extras nas colunas de texto
        for k in ("cliente", "produto", "categoria", "regiao"):
            r[k] = (r.get(k) or "").strip()

        # Validar data
        try:
            r["data_venda"] = datetime.strptime(r["data_venda"], "%Y-%m-%d")
        except (ValueError, TypeError):
            relatorio["removidos_data"] += 1
            continue

        # Validar nulos e conversão numérica
        q_str, p_str = str(r.get("quantidade") or "").strip(), str(r.get("preco_unitario") or "").strip()
        if not q_str or not p_str:
            relatorio["removidos_nulos"] += 1
            continue

        try:
            r["quantidade"] = int(float(q_str))
            r["preco_unitario"] = float(p_str)
        except ValueError:
            relatorio["removidos_nulos"] += 1
            continue

        # Padronizar nome do cliente para formato Cliente_NNN
        nome_limpo = re.sub(r"[^A-Za-z0-9_]", "", r["cliente"])
        numeros = re.findall(r"\d+", nome_limpo)
        r["cliente"] = f"Cliente_{int(numeros[0]):03d}" if numeros else nome_limpo

        limpos.append(r)

    relatorio["finais"] = len(limpos)
    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print(f"Entraram: {relatorio['iniciais']} | Removidos (Data): {relatorio['removidos_data']} | "
          f"Removidos (Nulos): {relatorio['removidos_nulos']} | Permaneceram: {relatorio['finais']}")
    return limpos, relatorio
