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


#GRAFICO 15:pairplot alta qualidade


df_tabela.rename(columns={'points': 'PONTOS'}, inplace=True)


limite_alta_qualidade = 92

def extrair_ano_local(texto):
    match = re.search(r'\b(19[89]\d|20\d{2})\b', str(texto))
    if match: return int(match.group(1))
    return np.nan

df_tabela['year_vintage'] = df_tabela['title'].apply(extrair_ano_local)


df_alta_qualidade = df_tabela[df_tabela['PONTOS'] >= limite_alta_qualidade].copy()

top_variedades_hq = df_alta_qualidade['variety'].value_counts().nlargest(3).index
df_plot_pair = df_alta_qualidade[df_alta_qualidade['variety'].isin(top_variedades_hq)]
vars_pairplot = ['PONTOS', 'price', 'year_vintage']

sns.set_theme(style="ticks", rc={'axes.facecolor': branco})
pairplot_grafico = sns.pairplot(
    df_plot_pair, 
    vars=vars_pairplot, 
    hue='variety',
    palette=[ouro_antigo, bordo_profundo, azul_moderno],
    diag_kind='kde', 
    plot_kws={'alpha': 0.7, 's': 45}, 
    corner=True
)
pairplot_grafico.fig.suptitle(f'CARACTERÍSTICAS DE VINHOS >= {limite_alta_qualidade}', fontsize=14, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=preto_falso)
plt.show()