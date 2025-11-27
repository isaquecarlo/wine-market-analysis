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


#grafico 9-tendencia anual pontos vs preco(linha dupla)
def extrair_ano(texto_titulo):
    match = re.search(r'\b(19[89]\d|20\d{2})\b', str(texto_titulo))
    if match: return int(match.group(1))
    return np.nan

df_tabela['year_vintage'] = df_tabela['title'].apply(extrair_ano)
df_vinhos_com_ano = df_tabela.dropna(subset=['year_vintage']).copy()
df_vinhos_com_ano = df_vinhos_com_ano[df_vinhos_com_ano['year_vintage'] <= 2025]
df_tendencia_anual = df_vinhos_com_ano.groupby('year_vintage', as_index=False).agg(media_pontos=('points', 'mean'), media_preco=('price', 'mean'), contagem=('title', 'count'))
df_tendencia_anual = df_tendencia_anual[df_tendencia_anual['contagem'] >= 10]

fig, ax1 = plt.subplots(figsize=(11, 6))

sns.lineplot(data=df_tendencia_anual, x='year_vintage', y='media_pontos', ax=ax1, color=bordo_profundo, linewidth=2, marker='o', label='Média de Pontos')
ax1.set_xlabel('ANO DA SAFRA', fontsize=11, fontweight='bold')
ax1.set_ylabel('PONTUAÇÃO', fontsize=11, fontweight='bold', color=bordo_profundo)

ax2 = ax1.twinx()
sns.lineplot(data=df_tendencia_anual, x='year_vintage', y='media_preco', ax=ax2, color=bordo_profundo, linewidth=2, marker='s', linestyle='--', label='Média de Preço')
ax2.set_ylabel('PREÇO (USD)', fontsize=11, fontweight='bold', color=cinza_elegante)

fig.suptitle('TENDÊNCIA ANUAL: PONTOS VS. PREÇO', fontsize=15, fontfamily=fonte_titulos_familia, fontweight=peso_fonte_titulo, color=bordo_profundo)
sns.despine(ax=ax1, right=False)
sns.despine(ax=ax2, right=False, left=True)
plt.tight_layout()
plt.show()