import dimod
from dimod.reference.samplers import ExactSolver
import time
import collections

# Matriz QUBO para f = x1 AND x2 (N=2)
Q_final_and = {
    ('x1', 'x1'): 1.0, 
    ('x2', 'x2'): 1.0, 
    ('x1', 'x2'): -2.0
}
modelo_qubo_2var = dimod.BQM.from_qubo(Q_final_and)

# ----------------------------------------
# Medición de Tiempo - N=2
# ----------------------------------------
sampler_exacto = ExactSolver()

start_time = time.time()
sampler_exacto.sample(modelo_qubo_2var)
tiempo_n2 = time.time() - start_time

print("-------------------------------------------------------")
print("--- ANÁLISIS DE ESCALADO CLÁSICO (ExactSolver) ---")
print(f"Tiempo de ejecución para N=2 (4 estados): {tiempo_n2:.6f} segundos.")
