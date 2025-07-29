import random
from ml_gen_alg.functions import operations

class GA:
    def __init__(
        self,
        fitness_func,
        num_generations=100,
        sol_per_pop=20,
        num_parents_mating=10,
        num_genes=10,
        init_range_low=0,
        init_range_high=255,
        initial_population=None,
        mutation_percent_genes=0.1,
        parent_selection_type="tournament",
        K_tournament=3,
        crossover_type="single_point",
        mutation_type="random",
        keep_parents=2,
        on_generation=None,
        stop_criteria=None,
    ):
        self.fitness_func = fitness_func
        self.num_generations = num_generations
        self.sol_per_pop = sol_per_pop
        self.num_parents_mating = num_parents_mating
        self.num_genes = num_genes
        self.init_range_low = init_range_low
        self.init_range_high = init_range_high
        self.initial_population = initial_population
        self.mutation_percent_genes = mutation_percent_genes
        self.parent_selection_type = parent_selection_type
        self.K_tournament = K_tournament
        self.crossover_type = crossover_type
        self.mutation_type = mutation_type
        self.keep_parents = keep_parents
        self.on_generation = on_generation
        self.stop_criteria = stop_criteria

        self.population = self._initialize_population()

    def _initialize_population(self):
        if self.initial_population is not None:
            return self.initial_population
        return [
            [random.randint(self.init_range_low, self.init_range_high) for _ in range(self.num_genes)]
            for _ in range(self.sol_per_pop)
        ]

    def _select_parents(self, fitnesses):
        selection_map = {
            "tournament": lambda: operations.tournament_selection(
                self.population, fitnesses, self.num_parents_mating, self.K_tournament
            ),
            "roulette": lambda: operations.roulette_wheel_selection(
                self.population, fitnesses, self.num_parents_mating
            ),
            "rank": lambda: operations.rank_selection(
                self.population, fitnesses, self.num_parents_mating
            ),
            "steady": lambda: operations.steady_state_selection(
                self.population, fitnesses, self.num_parents_mating
            ),
        }
        return selection_map.get(self.parent_selection_type, selection_map["tournament"])()

    def _crossover(self, parents):
        crossover_map = {
            "single_point": operations.single_point_crossover,
            "two_points": operations.two_points_crossover,
            "uniform": operations.uniform_crossover,
            "scattered": operations.scattered_crossover,
        }

        crossover_func = crossover_map.get(self.crossover_type, operations.single_point_crossover)
        offspring = []
        for i in range(0, len(parents), 2):
            p1 = parents[i]
            p2 = parents[i + 1 if i + 1 < len(parents) else 0]
            child1, child2 = crossover_func(p1, p2)
            offspring.extend([child1, child2])
        return offspring

    def _mutate(self, population, generation):
        mutation_map = {
            "random": operations.random_mutation,
            "swap": operations.swap_mutation,
            "inversion": operations.inversion_mutation,
            "scramble": operations.scramble_mutation,
            "adaptive": lambda ind: operations.adaptive_mutation(ind, generation=generation, max_generations=self.num_generations),
        }
        mutation_func = mutation_map.get(self.mutation_type, operations.random_mutation)
        return [mutation_func(ind) for ind in population]

    def _check_stopping(self, best_fitness, generation, best_history):
        if not self.stop_criteria:
            return False

        for criterion in self.stop_criteria:
            if criterion.startswith("reach_"):
                threshold = float(criterion.split("_")[1])
                if best_fitness >= threshold:
                    return True
            if criterion.startswith("saturate_"):
                limit = int(criterion.split("_")[1])
                if len(best_history) > limit and len(set(best_history[-limit:])) == 1:
                    return True
        return False

    def genetic_algorithm(self):
        best_history = []

        for generation in range(self.num_generations):
            # Adaptar cada individuo antes de pasarlo a la función fitness
            fitnesses = []
            for ind in self.population:
                # Si el individuo es una lista, convertirlo en un valor usable
                if isinstance(ind, list):
                    # Opción 1: Suma de los elementos
                    fitness_value = self.fitness_func(sum(ind))
                    # Alternativa - si necesitas aplicar la función a cada elemento:
                    # fitness_value = sum(self.fitness_func(x) for x in ind)
                else:
                    # Si no es una lista, usarlo directamente
                    fitness_value = self.fitness_func(ind)
                fitnesses.append(fitness_value)

            best_fitness = max(fitnesses)
            best_history.append(best_fitness)

            if self._check_stopping(best_fitness, generation, best_history):
                break

            parents = self._select_parents(fitnesses)
            offspring = self._crossover(parents)
            offspring = self._mutate(offspring, generation)

            # Elitismo
            best_individuals = sorted(
                zip(self.population, fitnesses), key=lambda x: x[1], reverse=True
            )[:self.keep_parents]
            self.population = [x[0] for x in best_individuals] + offspring[: self.sol_per_pop - self.keep_parents]

            if self.on_generation:
                self.on_generation(generation, self.population, best_fitness)

        # Calcular fitness final usando el mismo método adaptado
        final_fitnesses = []
        for ind in self.population:
            if isinstance(ind, list):
                fitness_value = self.fitness_func(sum(ind))
            else:
                fitness_value = self.fitness_func(ind)
            final_fitnesses.append(fitness_value)
        best_index = final_fitnesses.index(max(final_fitnesses))
        return self.population[best_index], final_fitnesses[best_index]
