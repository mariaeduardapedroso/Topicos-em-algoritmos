import matplotlib.pyplot as plt

# Resultados do experimento
resultados = {
    "melhor": {
        "tamanho": [50000, 100000, 150000, 200000, 250000, 300000],
        "tempo": [0.010209, 0.022388, 0.028002, 0.034813, 0.039135, 0.040773]
    },
    "medio": {
        "tamanho": [50000, 100000, 150000, 200000, 250000, 300000],
        "tempo": [60.820827, 239.140769, 516.733032, 874.294828, 1258.889437, 1837.556728]
    },
    "pior": {
        "tamanho": [50000, 100000, 150000, 200000, 250000, 300000],
        "tempo": [126.495176, 488.693262, 1041.330425, 1649.486600, 2231.747426, 3740]
    }
}

# Gerar gráficos separados para cada caso
for caso, dados in resultados.items():
    plt.figure()
    plt.plot(dados["tamanho"], dados["tempo"], label = caso)
    plt.xlabel('Tamanho do Vetor')
    plt.ylabel('Tempo Médio de Execução (s)')
    plt.title(f'Desempenho da Ordenação por Inserção - Caso {caso}')
    plt.legend()
    plt.grid(True)
    plt.show()

# Gerar gráfico com os três casos juntos
plt.figure()
for caso, dados in resultados.items():
    plt.plot(dados["tamanho"], dados["tempo"], label=caso)
plt.xlabel('Tamanho do Vetor')
plt.ylabel('Tempo Médio de Execução (s)')
plt.title('Desempenho da Ordenação por Inserção')
plt.legend()
plt.grid(True)
plt.show()
