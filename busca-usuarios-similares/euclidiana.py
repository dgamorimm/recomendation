import json
from rich import print
from math import sqrt

f = open('busca-usuarios-similares/data.json')

avaliacoes = json.load(f)

print(avaliacoes)

def euclidiana(usuario1, usuario2):
    si = {}
    for item in avaliacoes[usuario1]:
        if item in avaliacoes[usuario2]: si[item] = 1
    
    if len(si) == 0: return 0
    
    soma = sum([
        pow(avaliacoes[usuario1][item] - avaliacoes[usuario2][item],2)
        for item in avaliacoes[usuario1] if item in avaliacoes[usuario2]
    ])
    print(usuario1 + ' X ' + usuario2)
    return f'{(1/(1 + sqrt(soma))):.2%}'

print(euclidiana('Leonardo', 'Ana'))
print(euclidiana('Marcos', 'Claudia'))
print(euclidiana('Pedro', 'Marcos'))
print(euclidiana('Ana', 'Pedro'))
f.close()