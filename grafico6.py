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


#grafico 6 -distribuicao de precos por regiao (violinplot)
contagem_regioes = df_tabela['region_1'].value_counts()
top_regioes_nomes = contagem_regioes.nlargest(7).index
df_plot_violino_regiao = df_tabela[df_tabela['region_1'].isin(top_regioes_nomes)]

plt.figure(figsize=(11, 6))
ax_violino = plt.gca()

sns.violinplot(
    ax=ax_violino, x='region_1', y='price', data=df_plot_violino_regiao,
    order=top_regioes_nomes, palette=[ouro_antigo]*7, linewidth=1.2, inner='box', cut=0, density_norm='width'
)

ax_violino.set_ylim(0, df_plot_violino_regiao['price'].quantile(0.90))
ax_violino.set_title(f'DISTRIBUIÇÃO DE PREÇOS POR REGIÃO - TOP 7', fontsize=16, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=bordo_profundo, pad=18)
ax_violino.yaxis.grid(True, linestyle=':', color=rosa_queimado, alpha=0.6)

sns.despine(top=True, right=True)
plt.tight_layout()
plt.show()