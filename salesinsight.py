# ETAPA 1 - Estrutura inicial: imports e constantes
import csv
import json
import os
import random
import re
from datetime import datetime, timedelta

CAMINHO_CSV = "vendas.csv"   # arquivo de entrada (gerado se não existir)
PASTA_SAIDA = "outputs"      # pasta onde os resultados são gravados

# Dicionário de mapeamento: evita depender do idioma do computador/Colab.
# (strftime("%B") devolve o mês em inglês no Google Colab.)
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}
