import json
from rich import print
from math import sqrt

f = open('recomendacao-filme-usuario/data2.json')

avaliacoes = json.load(f)

def euclidiana(base, filme1, filme2):
    si = {}
    for item in base[filme1]:
        if item in base[filme2]: si[item] = 1
    
    if len(si) == 0: return 0
    
    soma = sum([
        pow(base[filme1][item] - base[filme2][item],2)
        for item in base[filme1] if item in base[filme2]
    ])
    return (1/(1 + sqrt(soma)))

def getSimilares(base, filme):
    similaridade = [
        (euclidiana(base, filme, outro), outro)
        for outro in base if outro != filme
        
    ]
    similaridade.sort()
    similaridade.reverse()

    return similaridade

def getRecomendacoes(base, filme):
    totais={}
    somaSimilaridade={}
    for outro in base:
        if outro == filme: continue
        similaridade = euclidiana(base, filme, outro)
        
        if similaridade <= 0: continue
        
        for item in base[outro]:
            if item not in base[filme]:
                totais.setdefault(item,0)
                totais[item] += base[outro][item] * similaridade
                somaSimilaridade.setdefault(item,0)
                somaSimilaridade[item] += similaridade
    rankings = [
        (total / somaSimilaridade[item], item)
        for item, total in totais.items()
    ]
    rankings.sort()
    rankings.reverse()
    return rankings

print(getSimilares(avaliacoes, 'Star Wars'))
print(getRecomendacoes(avaliacoes, 'Star Wars'))

f.close()