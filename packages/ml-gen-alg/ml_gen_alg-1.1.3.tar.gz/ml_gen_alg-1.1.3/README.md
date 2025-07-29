# 📦 ml-gen-alg

`ml-gen-alg` es una librería de Python para aplicar **algoritmos genéticos** personalizados sobre funciones objetivo, permitiendo seleccionar distintos métodos de selección, cruce y mutación.

---

## 🚀 Instalación

Puedes instalar la librería directamente desde PyPI con:

```bash
pip install ml-gen-alg
```

---

## ⚙️ Estructura del objeto `GA`

La librería expone un objeto principal `GA`, el cual ejecuta el algoritmo genético sobre una función objetivo personalizada.

### 📌 Constructor `GA()`

```python
GA(
    num_generations=1000,
    num_parents_mating=20,
    sol_per_pop=50,
    initial_population=None,
    num_genes=None,
    init_range_low=0,
    init_range_high=255,
    mutation_percent_genes=[0.3, 1.5],
    parent_selection_type=None,
    K_tournament=3,
    crossover_type=None,
    mutation_type=None,
    keep_parents=5,
    on_generation=None,
    fitness_func=None,
    stop_criteria=[],
    optimization_mode="maximize"  # O "minimize"
)
```

### ⚠️ Parámetros obligatorios

* `fitness_func`: función de evaluación de cada individuo.
* `num_genes` y/o `initial_population`.

---

## 🧮 Función de Fitness

La función de fitness debe tener **una o dos entradas**:

```python
def fitness_func(solution):
    return sum(solution)

# o bien:
def fitness_func(solution, solution_idx):
    return sum(solution)
```

---

## 📊 Métodos de Selección Soportados

Desde `ml_gen_alg.functions.operations`:

```python
steady_state_selection
rank_selection
random_selection
tournament_selection
roulette_wheel_selection
stochastic_universal_selection
nsga2_selection
tournament_selection_nsga2
```

## 🔗 Métodos de Cruce Soportados

```python
single_point_crossover
two_points_crossover
uniform_crossover
scattered_crossover
```

## 🧬 Métodos de Mutación Soportados

```python
random_mutation
swap_mutation
inversion_mutation
scramble_mutation
adaptive_mutation
```

---

## ✅ Ejemplo Básico (Maximización)

```python
from ml_gen_alg import GA
from ml_gen_alg.functions.operations import (
    roulette_wheel_selection,
    two_points_crossover,
    inversion_mutation
)

def fitness_func(solution):
    return sum(solution)

def on_generation(generation, best, score):
    print(f"Gen {generation}: best={best}, score={score}")

initial_population = [
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
]

ga = GA(
    num_generations=50,
    num_parents_mating=2,
    sol_per_pop=4,
    initial_population=initial_population,
    num_genes=10,
    parent_selection_type=roulette_wheel_selection,
    crossover_type=two_points_crossover,
    mutation_type=inversion_mutation,
    fitness_func=fitness_func,
    on_generation=on_generation,
    stop_criteria=["saturate_10"],
    optimization_mode="maximize"
)

best_solution, best_score = ga.genetic_algorithm()
```

---

## 🔻 Ejemplo (Minimización)

```python
def fitness_func(solution):
    return sum([gene ** 2 for gene in solution])

ga = GA(
    num_generations=100,
    num_parents_mating=3,
    sol_per_pop=6,
    initial_population=[[1,2,3,4], [2,2,2,2], [3,1,4,1], [4,4,4,4], [0,0,0,0], [1,1,1,1]],
    num_genes=4,
    parent_selection_type=roulette_wheel_selection,
    crossover_type=two_points_crossover,
    mutation_type=inversion_mutation,
    fitness_func=fitness_func,
    optimization_mode="minimize"
)

best_solution, best_score = ga.genetic_algorithm()
```

---

## 📤 Publicación

Para más información sobre cómo publicar tu propia versión:

* Actualiza el archivo `setup.py`
* Cambia la versión (`version='1.0.1'`, por ejemplo)
* Luego ejecuta:

```bash
python setup.py sdist bdist_wheel
```

Y publica:

```bash
twine upload dist/*
```

---

## 📬 Autor

* **Yamid Quiroga**
* Email: [yfquiroga@ucundinamarca.edu.co](mailto:yfquiroga@ucundinamarca.edu.co)
