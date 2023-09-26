from rich import print
from math import sqrt
import json

def euclidiana(base, objct1, objct2):
    si = {}
    for item in base[objct1]:
        if item in base[objct2]: si[item] = 1
    
    if len(si) == 0: return 0
    
    soma = sum([
        pow(base[objct1][item] - base[objct2][item],2)
        for item in base[objct1] if item in base[objct2]
    ])
    return (1/(1 + sqrt(soma)))

def getSimilares(base, objct):
    similaridade = [
        (euclidiana(base, objct, outro), outro)
        for outro in base if outro != objct
        
    ]
    similaridade.sort()
    similaridade.reverse()

    return similaridade[0:30]

def getRecomendacoesUsuario(base, objct):
    totais={}
    somaSimilaridade={}
    for outro in base:
        if outro == objct: continue
        similaridade = euclidiana(base, objct, outro)
        
        if similaridade <= 0: continue
        
        for item in base[outro]:
            if item not in base[objct]:
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
    return rankings[0:30]

def carregaMovieLens():
    filmes = {}
    for linha in open('recomendacao-filme-usuario/u.item',encoding='latin-1'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo
    
    base = {}
    for linha in open('recomendacao-filme-usuario/u.data',encoding='latin-1'):
        (usuario, idfilme, nota, _) = linha.split('\t')
        base.setdefault(usuario, {})
        base[usuario][filmes[idfilme]] = float(nota)
    
    return base

def calculaItensSimilares(base):
    result = {}
    for item in base:
        notas = getSimilares(base, item)
        result[item] = notas
    return result

def getRecomendacoesItens(baseUsuario, similaridadeItens, usuario):
    notasUsuario = baseUsuario[usuario]
    notas={}
    totalSimilaridade={}
    for (item, nota) in notasUsuario.items():
        for (similaridade, item2) in similaridadeItens[item]:
            if item2 in notasUsuario: continue
            notas.setdefault(item2, 0)
            notas[item2] += similaridade * nota
            totalSimilaridade.setdefault(item2, 0)
            totalSimilaridade[item2] += similaridade
    rankings=[
        (score/totalSimilaridade[item], item)
        for item, score in notas.items()
    ]
    rankings.sort()
    rankings.reverse()
    return rankings

if __name__ == '__main__':
    f1 = open('recomendacao-filme-itens/data.json')
    f2 = open('recomendacao-filme-itens/data2.json')

    avaliacoesUsuarios = json.load(f1)
    avaliacoesFilmes = json.load(f2)
    print(':::: Recomendação Usuário::::')
    print(getRecomendacoesUsuario(avaliacoesUsuarios, 'Leonardo'))
    
    # esse processo aqui pode ser demorado, portanto, devemos ter uma base pré calculada e o custo pode ser alto
    listaitens = calculaItensSimilares(avaliacoesFilmes)
    print(':::: Recomendação Itens::::')
    print(getRecomendacoesItens(avaliacoesUsuarios, listaitens, 'Leonardo'))
    
    f1.close()
    f2.close()