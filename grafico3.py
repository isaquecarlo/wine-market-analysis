import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.ticker as mtick
from matplotlib.colors import LinearSegmentedColormap
import re
import os



diretorio_script = os.path.dirname(os.path.abspath(__file__))

#juntando o diretorio do escript com o nome do arqv
arqv = os.path.join(diretorio_script, 'arquivo.csv')

#verificand se o arquivo existe antes de tentar abrir
if not os.path.exists(arqv):
    arqv = os.path.join(os.path.dirname(diretorio_script), 'arquivo.csv')
    
if not os.path.exists(arqv):
    print(f"ERRO CRÍTICO: Não encontrei 'arquivo.csv'.\nO script está procurando em: {arqv}")
    exit()

df_tabela = pd.read_csv(arqv)

if 'Unnamed' in df_tabela.columns:
    df_tabela = df_tabela.drop('Unnamed: 0', axis=1)

#limpeza geral basica
colunas_nao_nan = ['country', 'province', 'variety', 'price', 'points']
df_tabela.dropna(subset=colunas_nao_nan, inplace=True)

#definicao das cores personalizadas
preto_falso = '#361A20'
bordo_profundo = "#6B2F3D"
azul_moderno = '#46647E'
areia_quente = '#D4BFAA'
verde_oliva = '#2E8B57'
rosa_queimado ='#C08081'
cinza_elegante = '#5A5A5A'
ouro_antigo = '#C2B280'
branco = "#FFFFFF"
areia_quente_fundo = '#F9F9F9'

#config de fontes
fonte_titulos_familia = 'serif'
fonte_corpo_familia = 'sans-serif'
peso_fonte_titulo = 'heavy'
cor_linhas_grade_sutil = "#E0E0E0"

sns.set_theme(style="whitegrid")



#grafico 3 - top 10 melhores custo beneficio(stripplot)
df_analise_valor = df_tabela.copy()
df_analise_valor['value_ratio'] = df_analise_valor['points'] / df_analise_valor['price']
df_analise_valor.replace([np.inf, -np.inf], np.nan, inplace=True)
df_analise_valor.dropna(subset=['value_ratio'], inplace=True)
df_melhor_custo_beneficio = df_analise_valor.sort_values(by='value_ratio', ascending=False).head(10)
df_plot_strip = df_melhor_custo_beneficio.sort_values(by='value_ratio', ascending=True)

plt.figure(figsize=(12, 8))
grafico_strip_cb = sns.stripplot(
    x='value_ratio', y='title', data=df_plot_strip,
    color=preto_falso, size=10, marker='o', linewidth=0.8, edgecolor=cinza_elegante, jitter=False
)

for i in range(len(df_plot_strip)):
    plt.hlines(y=i, xmin=0, xmax=df_plot_strip['value_ratio'].iloc[i], color=preto_falso, alpha=0.6, linestyle='-', linewidth=1.2)

grafico_strip_cb.xaxis.grid(True, linestyle=':', color=cor_linhas_grade_sutil, alpha=0.7)
plt.title('TOP 10 VINHOS POR CUSTO-BENEFÍCIO', fontsize=17, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=preto_falso, pad=18)
plt.xlabel('ÍNDICE (PONTOS POR DÓLAR)', fontsize=13, color=preto_falso, fontweight='bold')

#anotacao dos valores
for i, (valor, titulo) in enumerate(zip(df_plot_strip['value_ratio'], df_plot_strip['title'])):
    grafico_strip_cb.text(valor + 0.02, i, f'{valor:.2f}', color=preto_falso, va='center', fontsize=9, bbox=dict(boxstyle='round,pad=0.15', fc='white', alpha=0.5, ec='none'))

sns.despine(top=True, right=True)
plt.tight_layout()
plt.show()