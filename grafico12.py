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

#GRAFICO 12:pontuacao por degustador

top_degustadores = df_tabela['taster_name'].value_counts().nlargest(7).index
df_plot_degustadores = df_tabela[df_tabela['taster_name'].isin(top_degustadores)]

plt.figure(figsize=(11, 7))
sns.violinplot(
    x='taster_name', 
    y='points', 
    data=df_plot_degustadores, 
    order=top_degustadores, 
    palette=[cinza_elegante]*7, 
    linewidth=1.2, 
    inner='box'
)
plt.title('DISTRIBUIÇÃO DE PONTUAÇÕES POR DEGUSTADOR', fontsize=15, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=preto_falso)
plt.xticks(rotation=30)
sns.despine()
plt.tight_layout()
plt.show()