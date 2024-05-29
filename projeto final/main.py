import numpy as np
import random

# Função para calcular a distância euclidiana entre dois pontos no espaço 3D
def distance(point1, point2):
    return np.linalg.norm(point1 - point2)

# Função para calcular o custo total de uma rota
def total_distance(route, distances):
    total = 0
    for i in range(len(route) - 1):
        total += distances[route[i], route[i+1]]
    total += distances[route[-1], route[0]]  # Voltar para o ponto inicial
    return total

# Função GRASP para encontrar uma solução inicial
def grasp(distances, max_iter):
    best_route = None
    best_distance = float('inf')
    
    for _ in range(max_iter):
        candidate_route = [0]  # Começa do ponto inicial (sol)
        remaining = set(range(1, len(distances)))

        while remaining:
            current = candidate_route[-1]
            # Seleciona o próximo ponto aleatoriamente dentre os restantes
            next_point = min(remaining, key=lambda x: distances[current, x])
            candidate_route.append(next_point)
            remaining.remove(next_point)
        
        candidate_distance = total_distance(candidate_route, distances)
        if candidate_distance < best_distance:
            best_route = candidate_route
            best_distance = candidate_distance
    
    return best_route

# Algoritmo 2-opt para otimizar a solução
def two_opt(route, distances):
    improved = True
    best_distance = total_distance(route, distances)
    
    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                new_route = route[:i] + route[i:j][::-1] + route[j:]
                new_distance = total_distance(new_route, distances)
                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True
                    break
            if improved:
                break
    
    return route, best_distance

# Carregar as coordenadas das estrelas a partir do arquivo star100.xyz
def load_star_coordinates(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()[2:]  # Ignorar as duas primeiras linhas
        coordinates = np.array([list(map(float, line.split()[1:])) for line in lines])
    return coordinates

# Carregar as coordenadas das estrelas
star_coordinates = load_star_coordinates('star100.xyz.txt')

# Calcular as distâncias entre as estrelas
distances = np.zeros((len(star_coordinates), len(star_coordinates)))
for i in range(len(star_coordinates)):
    for j in range(len(star_coordinates)):
        distances[i, j] = distance(star_coordinates[i], star_coordinates[j])

# Executar o GRASP para encontrar uma solução inicial
initial_solution = grasp(distances, max_iter=1000)

# Aplicar o algoritmo 2-opt para otimizar a solução
optimized_solution, optimized_distance = two_opt(initial_solution, distances)

print("Solução inicial:", initial_solution)
print("Distância inicial:", total_distance(initial_solution, distances))
print("Solução otimizada:", optimized_solution)
print("Distância otimizada:", optimized_distance)
