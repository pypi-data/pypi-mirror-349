import random
# =============================
# Parent Selection Methods
# =============================

def steady_state_selection(population, fitnesses, num_parents):
    return sorted(zip(population, fitnesses), key=lambda x: x[1])[:num_parents]

def rank_selection(population, fitnesses, num_parents):
    ranked = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
    return [x[0] for x in ranked[:num_parents]]

def random_selection(population, fitnesses, num_parents):
    return random.sample(population, num_parents)

def tournament_selection(population, fitnesses, num_parents, tournament_size=3):
    selected = []
    for _ in range(num_parents):
        participants = random.sample(list(zip(population, fitnesses)), tournament_size)
        winner = max(participants, key=lambda x: x[1])
        selected.append(winner[0])
    return selected

def roulette_wheel_selection(population, fitnesses, num_parents):
    total_fitness = sum(fitnesses)
    probabilities = [f / total_fitness for f in fitnesses]
    return random.choices(population, weights=probabilities, k=num_parents)

def stochastic_universal_selection(population, fitnesses, num_parents):
    total_fitness = sum(fitnesses)
    step = total_fitness / num_parents
    start = random.uniform(0, step)
    points = [start + i * step for i in range(num_parents)]

    chosen = []
    i = 0
    cumulative = fitnesses[0]
    for p in points:
        while cumulative < p:
            i += 1
            cumulative += fitnesses[i]
        chosen.append(population[i])
    return chosen

def nsga2_selection(population, fitnesses, num_parents):
    # Placeholder para selección basada en dominancia (NSGA-II)
    return population[:num_parents]

def tournament_selection_nsga2(population, fitnesses, num_parents):
    # Placeholder para torneo con dominancia (NSGA-II)
    return population[:num_parents]

# =============================
# Crossover Methods
# =============================

def single_point_crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

def two_points_crossover(parent1, parent2):
    p1, p2 = sorted(random.sample(range(len(parent1)), 2))
    return (
        parent1[:p1] + parent2[p1:p2] + parent1[p2:],
        parent2[:p1] + parent1[p1:p2] + parent2[p2:]
    )

def uniform_crossover(parent1, parent2):
    child1, child2 = [], []
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    return child1, child2

def scattered_crossover(parent1, parent2):
    mask = [random.randint(0, 1) for _ in range(len(parent1))]
    child1 = [p1 if m else p2 for p1, p2, m in zip(parent1, parent2, mask)]
    child2 = [p2 if m else p1 for p1, p2, m in zip(parent1, parent2, mask)]
    return child1, child2

# =============================
# Mutation Methods
# =============================

def random_mutation(individual, mutation_rate=0.1):
    return [gene + random.uniform(-1, 1) if random.random() < mutation_rate else gene for gene in individual]

def swap_mutation(individual):
    a, b = random.sample(range(len(individual)), 2)
    individual[a], individual[b] = individual[b], individual[a]
    return individual

def inversion_mutation(individual):
    a, b = sorted(random.sample(range(len(individual)), 2))
    individual[a:b] = reversed(individual[a:b])
    return individual

def scramble_mutation(individual):
    a, b = sorted(random.sample(range(len(individual)), 2))
    sub = individual[a:b]
    random.shuffle(sub)
    individual[a:b] = sub
    return individual

def adaptive_mutation(individual, mutation_rate=0.1, generation=1, max_generations=100):
    rate = mutation_rate * (1 - (generation / max_generations))
    return [gene + random.uniform(-1, 1) if random.random() < rate else gene for gene in individual]