import json
from rich import print
from math import sqrt

f = open('busca-usuarios-similares/data.json')

avaliacoes = json.load(f)

def euclidiana(usuario1, usuario2):
    si = {}
    for item in avaliacoes[usuario1]:
        if item in avaliacoes[usuario2]: si[item] = 1
    
    if len(si) == 0: return 0
    
    soma = sum([
        pow(avaliacoes[usuario1][item] - avaliacoes[usuario2][item],2)
        for item in avaliacoes[usuario1] if item in avaliacoes[usuario2]
    ])
    return (1/(1 + sqrt(soma)))

def getSimilares(usuario):
    similaridade = [
        (euclidiana(usuario, outro), outro)
        for outro in avaliacoes if outro != usuario
        
    ]
    similaridade.sort()
    similaridade.reverse()

    return similaridade

def getRecomendacoes(usuario):
    totais={}
    somaSimilaridade={}
    for outro in avaliacoes:
        if outro == usuario: continue
        similaridade = euclidiana(usuario, outro)
        
        if similaridade <= 0: continue
        
        for item in avaliacoes[outro]:
            if item not in avaliacoes[usuario]:
                totais.setdefault(item,0)
                totais[item] += avaliacoes[outro][item] * similaridade
                somaSimilaridade.setdefault(item,0)
                somaSimilaridade[item] += similaridade
    rankings = [
        (total / somaSimilaridade[item], item)
        for item, total in totais.items()
    ]
    rankings.sort()
    rankings.reverse()
    return rankings

print('::Leonardo::', getRecomendacoes('Leonardo'))
print('::Pedro::', getRecomendacoes('Pedro'))
print('::Claudia::', getRecomendacoes('Claudia'))
print('::Janaina::', getRecomendacoes('Janaina'))

f.close()