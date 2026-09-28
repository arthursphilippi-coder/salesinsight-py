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

# ======================================================================
# RF04: Criar Colunas Derivadas
# ======================================================================
def criar_colunas_derivadas(registros):
    """Calcula receita total, mês, trimestre, ano e faixa de valor."""
    for r in registros:
        r["receita_total"] = round(r["quantidade"] * r["preco_unitario"], 2)
        dt = r["data_venda"]
        r["mes"] = dt.month
        r["mes_nome"] = MESES_PT[dt.month]
        r["ano"] = dt.year

        # Trimestre com condicional simples
        if dt.month <= 3:
            r["trimestre"] = "Q1"
        elif dt.month <= 6:
            r["trimestre"] = "Q2"
        elif dt.month <= 9:
            r["trimestre"] = "Q3"
        else:
            r["trimestre"] = "Q4"

        # Faixa de valor da venda
        if r["receita_total"] < 500:
            r["faixa_receita_item"] = "Baixo Valor"
        elif r["receita_total"] < 5000:
            r["faixa_receita_item"] = "Médio Valor"
        else:
            r["faixa_receita_item"] = "Alto Valor"
    return registros

# ======================================================================
# RF05: Métricas Agregadas
# ======================================================================
def calcular_metricas(registros):
    """Agrupa e calcula totais por Mês, Top 5 Produtos, Categoria e Região."""
    metricas = {}

    # 1. Por Mês
    por_mes = {}
    for r in registros:
        chave = (r["ano"], r["mes"], r["mes_nome"])
        if chave not in por_mes:
            por_mes[chave] = {"receita_total": 0.0, "quantidade": 0, "n_vendas": 0}
        por_mes[chave]["receita_total"] += r["receita_total"]
        por_mes[chave]["quantidade"] += r["quantidade"]
        por_mes[chave]["n_vendas"] += 1

    metricas["por_mes"] = [
        {"ano": k[0], "mes": k[1], "mes_nome": k[2], "receita_total": round(v["receita_total"], 2),
         "quantidade": v["quantidade"], "n_vendas": v["n_vendas"]}
        for k, v in sorted(por_mes.items())
    ]

    # 2. Top 5 Produtos por Receita
    por_prod = {}
    for r in registros:
        p = r["produto"]
        por_prod[p] = por_prod.get(p, 0.0) + r["receita_total"]
    prods = [{"produto": k, "receita_total": round(v, 2)} for k, v in por_prod.items()]
    prods.sort(key=lambda x: x["receita_total"], reverse=True)
    metricas["top_produtos"] = prods[:5]

    # 3. Por Categoria
    por_cat = {}
    for r in registros:
        c = r["categoria"]
        por_cat[c] = por_cat.get(c, 0.0) + r["receita_total"]
    cats = [{"categoria": k, "receita_total": round(v, 2)} for k, v in por_cat.items()]
    cats.sort(key=lambda x: x["receita_total"], reverse=True)
    metricas["por_categoria"] = cats

    # 4. Por Região (com Ticket Médio)
    por_reg = {}
    for r in registros:
        reg = r["regiao"]
        if reg not in por_reg:
            por_reg[reg] = {"receita_total": 0.0, "n_vendas": 0}
        por_reg[reg]["receita_total"] += r["receita_total"]
        por_reg[reg]["n_vendas"] += 1

    regs = [{"regiao": k, "receita_total": round(v["receita_total"], 2),
             "ticket_medio": round(v["receita_total"] / v["n_vendas"], 2)} for k, v in por_reg.items()]
    regs.sort(key=lambda x: x["receita_total"], reverse=True)
    metricas["por_regiao"] = regs

    return metricas

# ======================================================================
# RF06: Segmentar Clientes com Lambda
# ======================================================================
def segmentar_clientes(registros):
    """Classifica clientes em Ouro, Prata e Bronze utilizando função lambda."""
    classificar = lambda t: "Ouro" if t > 15000 else ("Prata" if t >= 5000 else "Bronze")
    gasto = {}
    for r in registros:
        gasto[r["cliente"]] = gasto.get(r["cliente"], 0.0) + r["receita_total"]

    clientes = [{"cliente": k, "total_gasto": round(v, 2), "segmento": classificar(v)} for k, v in gasto.items()]
    clientes.sort(key=lambda x: x["total_gasto"], reverse=True)
    return clientes

# ======================================================================
# RF07: Função de Ordem Superior e Estatísticas Gerais
# ======================================================================
def processar_coluna(registros, coluna, funcao_transformacao, nome_saida=None):
    """Aplica uma função de transformação a uma coluna (função de ordem superior)."""
    nome_saida = nome_saida or f"{coluna}_transformado"
    for r in registros:
        r[nome_saida] = funcao_transformacao(r[coluna])
    return registros


def calcular_estatisticas_gerais(registros):
    """Calcula estatísticas gerais e responde quantas vendas ficaram acima da média."""
    total = len(registros)
    receitas = [r["receita_total"] for r in registros]
    receita_total = sum(receitas)
    media = receita_total / total
    acima_da_media = sum(1 for r in receitas if r > media)

    return {
        "total_vendas": total,
        "receita_total": round(receita_total, 2),
        "media_receita_por_venda": round(media, 2),
        "vendas_acima_da_media": acima_da_media
    }

# ======================================================================
# RF08: Exportação em CSV e JSON
# ======================================================================
def exportar_resultados(metricas, clientes, estatisticas):
    """Grava arquivos na pasta de saídas e faz a releitura de conferência do JSON."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # Escrever CSVs de métricas
    for nome, dados in metricas.items():
        with open(os.path.join(PASTA_SAIDA, f"metricas_{nome}.csv"), "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=dados[0].keys())
            w.writeheader()
            w.writerows(dados)

    # Escrever CSV de clientes
    with open(os.path.join(PASTA_SAIDA, "segmentacao_clientes.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=clientes[0].keys())
        w.writeheader()
        w.writerows(clientes)

    # Escrever JSON
    caminho_json = os.path.join(PASTA_SAIDA, "estatisticas_gerais.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(estatisticas, f, indent=4, ensure_ascii=False)

    # Reler JSON para conferência
    with open(caminho_json, "r", encoding="utf-8") as f:
        conferencia = json.load(f)

    print("\n=== EXPORTAÇÃO COMPLETA ===")
    print(f"JSON lido de volta com sucesso: {conferencia}")

# ======================================================================
# RF09: Ponto de Entrada (main)
# ======================================================================
def main():
    print("=" * 50)
    print("SALESINSIGHT PY - Análise de Dados de Vendas")
    print("=" * 50)

    # 1. Garantir e carregar o dataset
    if not os.path.exists(CAMINHO_CSV):
        gerar_dataset_vendas(CAMINHO_CSV)
    registros = carregar_dataset(CAMINHO_CSV)
    inspecionar_dados(registros)

    # 2. Limpeza e colunas derivadas
    registros_limpos, _ = limpar_dados(registros)
    registros_limpos = criar_colunas_derivadas(registros_limpos)

    # 3. Função de ordem superior (RF07)
    registros_limpos = processar_coluna(
        registros_limpos, "receita_total", lambda x: round(x / 1000, 2), "receita_em_milhares"
    )

    # 4. Cálculo de métricas
    metricas = calcular_metricas(registros_limpos)
    print("\n=== RESUMO DAS MÉTRICAS ===")
    print("Top 1 Produto:", metricas["top_produtos"][0])
    print("Top 1 Região:", metricas["por_regiao"][0])

    # 5. Segmentação de clientes
    clientes = segmentar_clientes(registros_limpos)
    print("\n=== TOP 3 CLIENTES ===")
    for c in clientes[:3]:
        print(c)

    # 6. Estatísticas e resposta do desafio
    estatisticas = calcular_estatisticas_gerais(registros_limpos)
    print(f"\nResposta ao Desafio: {estatisticas['vendas_acima_da_media']} de "
          f"{estatisticas['total_vendas']} vendas ficaram acima da média.")

    # 7. Exportação
    exportar_resultados(metricas, clientes, estatisticas)
    print("\n[CONCLUÍDO] Fluxo executado com sucesso!")


if __name__ == "__main__":
    main()
