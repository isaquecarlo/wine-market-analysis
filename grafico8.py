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


#filtrandoo
contagem_variedades = df_tabela['variety'].value_counts()
top_variedades_nomes = contagem_variedades.nlargest(10).index
df_plot_violino_variedade = df_tabela[df_tabela['variety'].isin(top_variedades_nomes)]



#grafico 8 -medias de pontos e precos combinadas por variedade
df_medias_por_variedade = df_plot_violino_variedade.groupby('variety', as_index=False).agg(media_pontos=('points', 'mean'), media_preco=('price', 'mean'), contagem=('points', 'count'))
df_plot_medias_var = df_medias_por_variedade.sort_values(by='media_pontos', ascending=True)

plt.figure(figsize=(10, 7))
grafico_medias_var = sns.stripplot(x='media_pontos', y='variety', data=df_plot_medias_var, color=bordo_profundo, size=12, marker='o', linewidth=1.2, edgecolor=preto_falso, jitter=False)

for i in range(len(df_plot_medias_var)):
    valor = df_plot_medias_var['media_pontos'].iloc[i]
    plt.hlines(y=i, xmin=80, xmax=valor, color=ouro_antigo, alpha=0.6, linestyle='-', linewidth=1.2)

plt.title('MEDIA DE PONTOS E PREÇOS PELAS TOP VARIEDADES', fontsize=16, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=preto_falso)

for i, row in df_plot_medias_var.iterrows():
    texto_anotacao = f'{row["media_pontos"]:.1f} pts\n(${row["media_preco"]:,.2f} USD)'
    grafico_medias_var.text(row['media_pontos'] + 0.15, i, texto_anotacao, color=preto_falso, va='center', fontsize=10.5, bbox=dict(boxstyle='round,pad=0.25', fc='white', alpha=0.7, ec=cinza_elegante))

sns.despine(top=True, right=True)
plt.tight_layout()
plt.show()