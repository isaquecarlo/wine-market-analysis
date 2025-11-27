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

#GRAFICO 13:Heatmap (regiao vs variedade)
top_regioes_hm = df_tabela['region_1'].value_counts().nlargest(7).index
top_variedades_hm = df_tabela['variety'].value_counts().nlargest(5).index

df_para_heatmap = df_tabela[
    df_tabela['region_1'].isin(top_regioes_hm) & 
    df_tabela['variety'].isin(top_variedades_hm)
].copy()

tabela_pivot = pd.pivot_table(
    df_para_heatmap, 
    values='points', 
    index='region_1', 
    columns='variety', 
    aggfunc='mean'
)

plt.figure(figsize=(10, 7))

paleta_heatmap = sns.blend_palette([areia_quente, rosa_queimado, bordo_profundo], as_cmap=True)

sns.heatmap(
    tabela_pivot, 
    annot=True, 
    fmt=".1f", 
    linewidths=.5, 
    linecolor=cinza_elegante, 
    cmap=paleta_heatmap
)
plt.title('PONTUAÇÃO MEDIA POR REGIÃO E VARIEDADE', fontsize=15, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=preto_falso, pad=20)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()