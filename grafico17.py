import pandas as pd
import numpy as np
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

# limpeza geral basica
colunas_nao_nan = ['country', 'province', 'variety', 'price', 'points']
df_tabela.dropna(subset=colunas_nao_nan, inplace=True)


df_tabela.rename(columns={'points': 'PONTOS'}, inplace=True)



#Tabela17: identificar top 5 países por media de pontos
top_5_paises = df_tabela.groupby('country')['PONTOS'].mean().nlargest(5).index
df_para_medias = df_tabela[df_tabela['country'].isin(top_5_paises)]

print("\n--- MÉDIAS DOS TOP 5 PAÍSES (MAIOR MÉDIA DE PONTOS) ---")


medias_top_5 = df_para_medias.groupby('country')[['PONTOS', 'price']].mean().reindex(top_5_paises)

if not medias_top_5.empty:
    medias_top_5.columns = ['MÉDIA DE PONTOS', 'PREÇO MÉDIO (USD)']
    

    medias_top_5['MÉDIA DE PONTOS'] = medias_top_5['MÉDIA DE PONTOS'].map(lambda x: f'{x:.1f} pts' if pd.notnull(x) else '-')
    medias_top_5['PREÇO MÉDIO (USD)'] = medias_top_5['PREÇO MÉDIO (USD)'].map(lambda x: f'${x:,.2f}' if pd.notnull(x) else '-')
    
    print(medias_top_5.to_string())
else:
    print("Não foi possível calcular as médias para a tabela.")