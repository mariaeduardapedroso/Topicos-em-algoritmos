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

def greedy_search(distances):
    num_stars = len(distances)
    current_star = 0  # Começa do ponto inicial (sol)
    visited_stars = [current_star]
    remaining_stars = set(range(num_stars))
    remaining_stars.remove(current_star)

    while remaining_stars:
        next_star = min(remaining_stars, key=lambda x: distances[current_star, x])
        visited_stars.append(next_star)
        remaining_stars.remove(next_star)
        current_star = next_star
    
    return visited_stars

def random_alpha(min_alpha, max_alpha):
    return random.uniform(min_alpha, max_alpha)

# Função GRASP para encontrar uma solução inicial
def grasp(distances, max_iter, alpha=0.5):
    best_route = None
    best_distance = float('inf')
    
    for _ in range(max_iter):
        candidate_route = [0]  # Começa do ponto inicial (sol)
        remaining = set(range(1, len(distances)))

        while remaining:
            current = candidate_route[-1]
            # Construção da lista restrita de candidatos (RCL)
            rcl = []
            for point in remaining:
                if distances[current, point] <= alpha * best_distance:
                    rcl.append(point)
            # Se a RCL estiver vazia, selecione aleatoriamente qualquer ponto
            if not rcl:
                rcl = list(remaining)
            next_point = random.choice(rcl)
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
        lines = file.readlines()  # Ignorar as duas primeiras linhas
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
min_alpha = 0.1
max_alpha = 0.9
alpha = random_alpha(min_alpha, max_alpha)
print("Alpha aleatório:", alpha)

initial_solution = grasp(distances, max_iter=1000,alpha=alpha)

# Aplicar o algoritmo 2-opt para otimizar a solução
optimized_solution, optimized_distance = two_opt(initial_solution, distances)

print("Solução inicial GRASP:", initial_solution)
print("Distância inicial GRASP:", total_distance(initial_solution, distances))

print("Solução otimizada 2-opt:", optimized_solution)
print("Distância otimizada 2-opt:", optimized_distance)

# Executar a busca gulosa para encontrar uma solução
greedy_solution = greedy_search(distances)

print("Solução gulosa:", greedy_solution)
print("Distância gulosa:", total_distance(greedy_solution, distances))
