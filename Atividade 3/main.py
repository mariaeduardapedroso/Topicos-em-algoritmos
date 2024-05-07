import time
import random
import matplotlib.pyplot as plt
from multiprocessing import Pool
tamanhos = [50000, 100000, 150000, 200000, 250000, 300000]

def quicksort(X, IniVet, FimVet):
    if IniVet >= FimVet:
        return  # Condição de parada para a recursão

    i = IniVet
    j = FimVet
    pivo = X[(IniVet + FimVet) // 2]

    while i <= j:
        while X[i] < pivo:
            i += 1
        while X[j] > pivo:
            j -= 1
        if i <= j:
            aux = X[i]
            X[i] = X[j]
            X[j] = aux
            i += 1
            j -= 1

    quicksort(X, IniVet, j)
    quicksort(X, i, FimVet)


def gerar_arranjo_aleatorio(tamanho):
    return [random.randint(0, 1000) for _ in range(tamanho)]

def gerar_arranjo_ordenado(tamanho):
    return [i for i in range(1, tamanho + 1)]

def gerar_arranjo_pior_caso(tamanho):
    return [tamanho - i for i in range(tamanho)]


def executar_experimento(caso_tamanho):
    caso, tamanho = caso_tamanho
    tempos = []
    with open('execussao.txt', 'a+') as f:
        for _ in range(10):
            if caso == 'melhor':
                arr = gerar_arranjo_ordenado(tamanho)
            elif caso == 'medio':
                arr = gerar_arranjo_aleatorio(tamanho)
            elif caso == 'pior':
                arr = gerar_arranjo_pior_caso(tamanho) 
            tempo_inicio = time.time()
            quicksort(arr, 0, len(arr) - 1)
            tempo_fim = time.time()
            tempo_execucao = tempo_fim - tempo_inicio
            tempos.append(tempo_execucao)
            print(f"Tamanho: {tamanho}, Caso {caso} Tempo médio de execução: {tempo_execucao} s")
            f.write(f"Tamanho: {tamanho}, Caso {caso} Tempo medio de execucao: {tempo_execucao} s\n")
    return caso, tamanho, sum(tempos) / len(tempos)

def tempo_execucao_medio(resultados):
    medias = {}
    for caso, tamanhos in resultados.items():
        medias[caso] = {}
        for tamanho, tempos in tamanhos.items():
            medias[caso][tamanho] = sum(tempos) / len(tempos)
    return medias

def plotar_resultado(caso, dados):
    plt.plot(tamanhos, [dados[tamanho] for tamanho in tamanhos], label=caso)
    plt.xlabel('Tamanho do Vetor')
    plt.ylabel('Tempo Médio de Execução (s)')
    plt.title(f'Desempenho da Ordenação por Inserção - Caso {caso.capitalize()}')
    plt.legend()
    plt.show()

def plotar_resultados(medias):
    for caso, dados in medias.items():
        plt.plot(tamanhos, [dados[tamanho] for tamanho in tamanhos], label=caso)
    plt.xlabel('Tamanho do Vetor')
    plt.ylabel('Tempo Médio de Execução (s)')
    plt.title('Desempenho da Ordenação por Inserção')
    plt.legend()
    plt.show()

def principal():
    casos = ['melhor', 'medio', 'pior']
    pool = Pool()
    resultados = {}
    for caso in casos:
        resultados[caso] = {}
        resultados_temp = pool.map(executar_experimento, [(caso, tamanho) for tamanho in tamanhos])
        for r in resultados_temp:
            resultados[r[0]][r[1]] = [r[2]]  # Guardar apenas o tempo médio de execução
    with open('output.txt', 'w') as f:
        f.write("Resultados do experimento:\n")
        for caso, data in tempo_execucao_medio(resultados).items():
            f.write(f"Caso: {caso}\n")
            for tamanho, tempo in data.items():
                f.write(f"Tamanho: {tamanho}, Tempo medio de execucao: {tempo:.6f} s\n")
    for caso, dados in tempo_execucao_medio(resultados).items():
        plotar_resultado(caso, dados)
    plotar_resultados(tempo_execucao_medio(resultados))

if __name__ == "__main__":
    principal()
    
    
    
    
    
# Análise de Operações:
#   Melhor Caso:
#       No melhor caso, o pivô divide o array em duas partes de tamanho aproximadamente igual. Portanto, a cada chamada recursiva, metade dos elementos são descartados.
#       O número de operações é aproximadamente proporcional ao número de vezes que o array é dividido ao meio.
#       Complexidade de tempo: O(n log n), onde n é o tamanho do array.
#   Pior Caso:
#       No pior caso, o pivô escolhido sempre é o menor ou o maior elemento do array, resultando em uma partição desbalanceada.
#       Isso leva a uma divisão do array em apenas um elemento e (n - 1) elementos, resultando em n chamadas recursivas.
#       O número total de operações no pior caso é proporcional à soma dos primeiros n números inteiros, o que é O(n^2).
#       Complexidade de tempo: O(n^2), onde n é o tamanho do array.
#   Caso Médio:
#       No caso médio, espera-se que o pivô divida o array em duas partes de tamanho aproximadamente igual, mas isso não é garantido.
#       O número de operações no caso médio é difícil de determinar com precisão, mas é comumente aceito como O(n log n).
#       Complexidade de tempo: O(n log n), onde n é o tamanho do array.