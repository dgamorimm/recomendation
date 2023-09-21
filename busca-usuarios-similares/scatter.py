import json
import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import plotly.express as px
from rich import print


df = pd.read_json('busca-usuarios-similares/data.json')
# print(df)

# Use o método transpose() para trocar as colunas por linhas e vice-versa
df_transposed = df.transpose()

# Ou você pode usar a propriedade .T
# df_transposed = df.T

# Exiba o DataFrame resultante
# Mover o índice para uma coluna na primeira posição
df_transposed.reset_index(inplace=True)
df_transposed.rename(columns={'index': 'Name'}, inplace=True)
print(df_transposed)

fig  = px.scatter(df_transposed, x = ['Star Trek','Freddy x Jason','O Ultimato Bourne','Norbit','Star Wars','Exterminador do Futuro'], y = 'Name', log_x = False, width = 800)
fig.update_traces(marker = dict(size = 12, line=dict(width = 2)), selector = dict(mode = 'markers'))
# fig.update_layout(title = 'Star Trek X Exterminador')
# fig.update_xaxes(title = 'Star Trek')
# fig.update_yaxes(title = 'Exterminador')
fig.show()

