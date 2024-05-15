import time
import random
import matplotlib.pyplot as plt
from multiprocessing import Pool
tamanhos = [50000, 100000, 150000, 200000, 250000, 300000]

def countingSort(A):
    n = len(A)
    k = max(A)  # descobre o valor máximo no vetor A

    C = [0] * (k + 1)  # Inicializa a lista de contagem com zeros
    B = [0] * n  # Inicializa a lista de saída com zeros

    # Conta a ocorrência de cada elemento em A
    for j in range(n):
        C[A[j]] += 1

    # Atualiza C para indicar a posição correta de cada elemento na saída
    for i in range(1, k + 1):
        C[i] += C[i - 1]

    # Monta o array ordenado B
    for j in range(n - 1, -1, -1):
        B[C[A[j]] - 1] = A[j]
        C[A[j]] -= 1

    return B

def gerar_arranjo_aleatorio(tamanho):
    return [random.randint(0, 1000) for _ in range(tamanho)]

def gerar_arranjo_ordenado(tamanho, decrescente=False):
    if decrescente:
        return [i for i in range(tamanho, 0, -1)]
    else:
        return [i for i in range(1, tamanho + 1)]

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
                arr = gerar_arranjo_ordenado(tamanho, decrescente=True)
            tempo_inicio = time.time()
            countingSort(arr)
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
    plt.title(f'Desempenho da Ordenação por Contagem - Caso {caso.capitalize()}')
    plt.legend()
    plt.show()

def plotar_resultados(medias):
    for caso, dados in medias.items():
        plt.plot(tamanhos, [dados[tamanho] for tamanho in tamanhos], label=caso)
    plt.xlabel('Tamanho do Vetor')
    plt.ylabel('Tempo Médio de Execução (s)')
    plt.title('Desempenho da Ordenação por Contagem')
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