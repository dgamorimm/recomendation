import json
from rich import print

f = open('busca-usuarios-similares/data.json')

avaliacoes = json.load(f)

print(avaliacoes)

f.close()