# SalesInsight PY

Análise de dados de vendas em Python puro (sem bibliotecas externas), desenvolvida como Mini-Projeto Avaliativo do **Módulo 01** do curso *Desenvolvedor(a) em IA para Análise Preditiva*.

## Objetivo do projeto

Simular o trabalho de um Analista de Dados Júnior em uma empresa de varejo: receber um histórico de vendas em CSV com dados sujos, limpá-lo, transformá-lo e gerar um insights

O programa responde a cinco perguntas de negócio:

1. Como as vendas se comportam ao longo do tempo (por mês e por trimestre)?
2. Quais produtos e categorias geram mais receita?
3. Quais regiões têm melhor desempenho?
4. Quais clientes são mais valiosos (Bronze, Prata e Ouro)?
5. Quantas vendas individuais tiveram receita acima da média geral por venda?

## O que o projeto faz (fluxo de ponta a ponta)

| Etapa | O que acontece | Requisito |
| 1 | Gera o dataset sintético `vendas.csv` (200 registros, com sujeira proposital) ou usa o arquivo existente | RF01 |
| 2 | Inspeciona: total de registros, colunas, valores ausentes por coluna e primeiros registros | RF02 |
| 3 | Limpa: remove espaços, datas inválidas e nulos; ajusta tipos; padroniza clientes com regex; imprime o relatório de limpeza | RF03 |
| 4 | Cria colunas derivadas: `receita_total`, `mes`, `mes_nome`, `trimestre`, `ano`, `faixa_receita_item` | RF04 |
| 5 | Calcula métricas por mês, trimestre, produto (Top 5), categoria e região | RF05 |
| 6 | Segmenta clientes em Bronze / Prata / Ouro com função `lambda` | RF06 |
| 7 | Organiza tudo em funções reutilizáveis, inclusive uma função que recebe outra função (`processar_coluna`) | RF07 |
| 8 | Exporta resultados em CSV e JSON e lê o JSON de volta para conferência | RF08 |
| 9 | Executa tudo na ordem correta a partir de `main()` | RF09 |

## Conceitos aplicados (Módulo 01, Semanas 01 a 05)

- **Lógica de programação:** variáveis, tipos (`int`, `float`, `str`, `bool`, `list`, `tuple`, `dict`), operadores aritméticos, lógicos e relacionais, `if/elif/else`, `for` e `while`.
- **Estruturas de dados:** lista de dicionários (o dataset), dicionário de listas (as métricas), tuplas como chave de agrupamento, *comprehensions*.
- **Funções:** parâmetros, valor padrão, retorno, docstrings, funções `lambda` em contextos distintos (classificação de segmento, ordenação, transformação de colunas) e função de ordem superior (`processar_coluna`).
- **Arquivos:** leitura e escrita de CSV (`csv.DictReader` / `csv.DictWriter`) e JSON (`json.dump` / `json.load`).
- **datetime:** conversão com `strptime` dentro de `try/except`, extração de mês e ano, cálculo de trimestre.
- **Expressões regulares (`re`):** `re.compile()` e `re.sub()` para limpar e padronizar nomes de clientes.
- **Módulos e importação:** `csv`, `json`, `os`, `random`, `re`, `datetime`.
- **Git e GitHub:** GitFlow simplificado, branches descritivas, commits no padrão *conventional commits* e Pull Requests.

## Como executar

Requisito: **Python 3.10 ou superior**. Não é preciso instalar nenhuma biblioteca externa.

### Google Colab

1. Acesse [colab.research.google.com](https://colab.research.google.com) e crie um notebook.
2. Faça upload de `salesinsight.py` (o `vendas.csv` é opcional: se não existir, é gerado).
3. Em uma célula, execute: `!python salesinsight.py`

### Localmente (VS Code ou terminal)

```bash
git clone https://github.com/arthursphilippi-coder/salesinsight-py.git
cd salesinsight-py
python salesinsight.py
```

No Windows, se `python` não funcionar, use `py salesinsight.py`.

Ao final, a pasta `outputs/` contém os resultados.

## Estrutura do projeto

```
salesinsight-py/
|-- salesinsight.py          # fluxo principal (todas as funções + main)
|-- vendas.csv               # dataset (gerado pelo próprio código)
|-- README.md
|-- outputs/
|   |-- metricas_por_mes.csv
|   |-- metricas_por_trimestre.csv
|   |-- metricas_top_produtos.csv
|   |-- metricas_por_categoria.csv
|   |-- metricas_por_regiao.csv
|   |-- segmentacao_clientes.csv
|   |-- estatisticas_gerais.json
|-- planejamento/
    |-- tarefas-kanban.md    # planejamento das tarefas
```

## Resultados com o dataset padrão (`seed=42`)

Como a semente aleatória é fixa, qualquer pessoa obtém os mesmos números:

- **Limpeza:** 200 registros entraram; 17 foram removidos (4 por data inválida e 13 por quantidade ou preço ausente); 183 permaneceram.
- **Produto líder:** Notebook, com R$ 374.174,85 de receita.
- **Melhor trimestre:** Q4, com R$ 375.924,07.
- **Melhor região em receita:** Nordeste, com R$ 366.321,23.
- **Vendas acima da média:** 70 de 183 vendas superaram a média de R$ 7.051,07 por venda.

## Decisões técnicas

**1. Remover registros inválidos em vez de preenchê-los.** Neste módulo ainda não se trabalha imputação estatística (Semanas 09 a 11). Além disso, inventar uma data ou uma quantidade contaminaria a receita. A remoção é registrada no relatório de limpeza, então nada é descartado em silêncio.

**2. Padronizar o nome do cliente antes de agrupar.** O dataset traz variações como `CLIENTE-007`, `cliente#007` e `Cliente_007!!`. Sem a padronização com regex, o mesmo cliente viraria vários "clientes" e a segmentação Bronze/Prata/Ouro sairia errada. Por isso a limpeza ocorre sempre **antes** das agregações.

**3. Uma única função `agrupar()` para todas as métricas.** Em vez de repetir o mesmo laço cinco vezes, ela recebe a tupla de colunas que define o grupo (por exemplo `("ano", "mes")`) e devolve os totais. Isso reduz código repetido e facilita incluir novas dimensões.

## Limitações e melhorias possíveis

- Com os limites do enunciado (Ouro acima de R$ 15.000), 34 dos 50 clientes ficam em Ouro, o que enfraquece a segmentação. Faixas baseadas em percentis dariam uma divisão mais equilibrada (assunto de semanas futuras).
- O dataset é sintético e cobre apenas 2025, com dados reais de vários anos, seria útil comparar períodos.
- Uma versão futura pode usar Pandas para simplificar agregações e Matplotlib/Seaborn para gráficos (Semanas 06 a 08).

## Ferramentas utilizadas

- Python 3.10+
- Google Colab
- Biblioteca padrão do Python: `csv`, `json`, `re`, `datetime`, `os`, `random`
- GitHub
- GitHub Projects

## Vídeo de demonstração

[inserir o link do Google Drive ou do YouTube aqui]
