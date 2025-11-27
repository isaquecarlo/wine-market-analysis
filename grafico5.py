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



#grafico 5 -top regioes media de ponts
df_regiao_stats = df_tabela.groupby('region_1')[['points', 'price']].agg(media_pontos=('points', 'mean'), contagem_vinhos=('points', 'count'), media_preco=('price', 'mean')).reset_index()
df_regiao_stats_filtrado = df_regiao_stats[df_regiao_stats['contagem_vinhos'] >= 100].copy()
top_n_regioes = 10

# parte a:pontos
df_top_regioes_pontos = df_regiao_stats_filtrado.sort_values(by='media_pontos', ascending=False).head(top_n_regioes)
df_plot_regioes_pontos = df_top_regioes_pontos.sort_values(by='media_pontos', ascending=True)

plt.figure(figsize=(11, 7))
grafico_regiao_pontos = sns.stripplot(x='media_pontos', y='region_1', data=df_plot_regioes_pontos, color=bordo_profundo, size=10, marker='o', linewidth=0.8, edgecolor=preto_falso, jitter=False)

for i in range(len(df_plot_regioes_pontos)):
    valor = df_plot_regioes_pontos['media_pontos'].iloc[i]
    plt.hlines(y=i, xmin=80, xmax=valor, color=cinza_elegante, alpha=0.5, linestyle='-', linewidth=1)

plt.title(f'TOP {top_n_regioes} REGIÕES COM MAIOR MÉDIA DE PONTOS', fontsize=15, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=preto_falso)
for i, valor in enumerate(df_plot_regioes_pontos['media_pontos']):
    grafico_regiao_pontos.text(valor + 0.1, i, f'{valor:.1f}', color=preto_falso, va='center', fontsize=8)

sns.despine(top=True, right=True)
plt.tight_layout()
plt.show()

# parte b:preco
df_top_regioes_preco = df_regiao_stats_filtrado.sort_values(by='media_preco', ascending=False).head(top_n_regioes)
df_plot_regioes_preco = df_top_regioes_preco.sort_values(by='media_preco', ascending=True)

plt.figure(figsize=(11, 7))
grafico_regiao_preco = sns.stripplot(x='media_preco', y='region_1', data=df_plot_regioes_preco, color=rosa_queimado, size=10, marker='D', linewidth=0.8, edgecolor=preto_falso, jitter=False)

for i in range(len(df_plot_regioes_preco)):
    valor = df_plot_regioes_preco['media_preco'].iloc[i]
    plt.hlines(y=i, xmin=0, xmax=valor, color=cinza_elegante, alpha=0.5, linestyle='-', linewidth=1)

plt.title(f'TOP {top_n_regioes} REGIÕES POR PREÇO MÉDIO', fontsize=15, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=preto_falso)
for i, valor in enumerate(df_plot_regioes_preco['media_preco']):
    grafico_regiao_preco.text(valor + 2, i, f'${valor:,.2f}', color=preto_falso, va='center', fontsize=8)

sns.despine(top=True, right=True)
plt.tight_layout()
plt.show()