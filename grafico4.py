import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.ticker as mtick
from matplotlib.colors import LinearSegmentedColormap
import re
import os


diretorio_script = os.path.dirname(os.path.abspath(__file__))
arqv = os.path.join(diretorio_script, 'arquivo.csv')

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
cinza_elegante = '#5A5A5A'
branco = "#FFFFFF"

#config de fontes
fonte_titulos_familia = 'serif'
peso_fonte_titulo = 'heavy'

sns.set_theme(style="whitegrid")


df_analise_valor = df_tabela.copy()


#grafico4 - diferenca normalizada entre pontos e preco
min_points, max_points = df_analise_valor['points'].min(), df_analise_valor['points'].max()
min_price, max_price = df_analise_valor['price'].min(), df_analise_valor['price'].max()

#calculos
df_analise_valor['points_norm'] = (df_analise_valor['points'] - min_points) / (max_points - min_points)
df_analise_valor['price_norm'] = (df_analise_valor['price'] - min_price) / (max_price - min_price)
df_analise_valor['score_price_diff'] = df_analise_valor['points_norm'] - df_analise_valor['price_norm']

#top 10
df_alta_pontuacao_rel_preco = df_analise_valor.sort_values(by='score_price_diff', ascending=False).head(10)
df_plot_sd = df_alta_pontuacao_rel_preco.sort_values(by='score_price_diff', ascending=True)

#plot
plt.figure(figsize=(10, 7))
grafico_sd = sns.stripplot(x='score_price_diff', y='title', data=df_plot_sd, color=bordo_profundo, size=9, marker='D', linewidth=0.7, edgecolor=preto_falso, jitter=False)

for i in range(len(df_plot_sd)):
    valor_metrica = df_plot_sd['score_price_diff'].iloc[i]
    plt.hlines(y=i, xmin=min(0, valor_metrica), xmax=max(0, valor_metrica), color=cinza_elegante, alpha=0.5, linestyle='-', linewidth=1)

plt.axvline(0, color=cinza_elegante, linestyle='--', linewidth=0.8, alpha=0.7)
plt.title('TOP 10 - PONTUAÇÃO ALTA REL.PREÇO', fontsize=16, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=preto_falso, pad=15)

for i, valor in enumerate(df_plot_sd['score_price_diff']):
    alinhamento_h = 'left' if valor >= 0 else 'right'
    deslocamento = 0.02 if valor >= 0 else -0.02
    grafico_sd.text(valor + deslocamento, i, f'{valor:.2f}', color=preto_falso, va='center', ha=alinhamento_h, fontsize=8, bbox=dict(boxstyle='round,pad=0.15', fc='white', alpha=0.6, ec='none'))

sns.despine(top=True, right=True)
plt.tight_layout()
plt.show()