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





#grafico 1 - contagem de vinhos por pais(stripplot horizontal)
top_n_paises_contagem = 10
contagem_por_pais = df_tabela['country'].value_counts().nlargest(top_n_paises_contagem)
df_plot_contagem_pais = contagem_por_pais.reset_index()
df_plot_contagem_pais.columns = ['PAÍS', 'NÚMERO DE VINHOS']
df_plot_contagem_pais = df_plot_contagem_pais.sort_values(by='NÚMERO DE VINHOS', ascending=True)

plt.figure(figsize=(10, 6))
ax_contagem = plt.gca()

sns.stripplot(
    x='NÚMERO DE VINHOS', y='PAÍS', data=df_plot_contagem_pais,
    order=df_plot_contagem_pais['PAÍS'], color=bordo_profundo,
    size=10, marker='o', linewidth=0.8, edgecolor=preto_falso, jitter=False, ax=ax_contagem
)

for i in range(len(df_plot_contagem_pais)):
    valor_contagem = df_plot_contagem_pais['NÚMERO DE VINHOS'].iloc[i]
    ax_contagem.hlines(y=i, xmin=0, xmax=valor_contagem, color=cinza_elegante, alpha=0.5, linestyle='-', linewidth=0.9)

ax_contagem.xaxis.grid(True, linestyle=':', color=cor_linhas_grade_sutil, alpha=0.7)
ax_contagem.set_title(f'TOP {top_n_paises_contagem} PAÍSES POR NÚMERO DE VINHOS', fontsize=14, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=preto_falso, pad=12)
ax_contagem.set_xlabel('NÚMERO DE VINHOS (CONTAGEM)', fontsize=10, color=preto_falso)
ax_contagem.set_ylabel('PAÍS', fontsize=10, color=preto_falso)

#txt ao lado de cada ponto
for i, valor in enumerate(df_plot_contagem_pais['NÚMERO DE VINHOS']):
    ax_contagem.text(valor + (df_plot_contagem_pais['NÚMERO DE VINHOS'].max() * 0.01), i, f'{int(valor)}', color=preto_falso, va='center', fontsize=7.5)

sns.despine(top=True, right=True)
plt.tight_layout()
plt.show()