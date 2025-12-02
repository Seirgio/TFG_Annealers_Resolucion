import dimod
import neal
from dimod.reference.samplers import ExactSolver 


# 1. Definición del problema: Queremos que x1 sea 1 (minimizando -x1).
# QUBO: -1 * x1
Q = {('x1', 'x1'): -1.0}

# Creamos el modelo QUBO
modelo_qubo = dimod.BQM.from_qubo(Q)

# ----------------------------------------------------
# A) PRUEBA 1: RECOCIDO SIMULADO (Simulated Annealing - Heurístico)
# ----------------------------------------------------
sampler_simulado = neal.SimulatedAnnealingSampler()

# Ejecutamos la simulación 100 veces
resultados_simulados = sampler_simulado.sample(modelo_qubo, num_reads=100)

# El 'estado fundamental' (solución de mínima energía) es el primer resultado
mejor_solucion_simulada = resultados_simulados.first


# ----------------------------------------------------
# B) PRUEBA 2: SOLUCIONADOR EXACTO (Determinístico)
# ----------------------------------------------------
sampler_exacto = ExactSolver()

# Ejecutamos el solucionador exacto (solo una vez, ya que es determinístico)
resultados_exactos = sampler_exacto.sample(modelo_qubo)

# ----------------------------------------------------
# C) RESULTADOS
# ----------------------------------------------------

print("--- SOLUCIÓN EXACTA (Garantizada) ---")
# La solución exacta garantiza el mínimo global, la energía debe ser -1.0 y x1=1
print(f"Mejor configuración Exacta: {resultados_exactos.first.sample}")
print(f"Energía mínima alcanzada: {resultados_exactos.first.energy}")

print("\n--- RESULTADOS DEL RECOCIDO SIMULADO (Heurístico) ---")
# El simulador heurístico también debería encontrar el mínimo en un problema tan simple
print(f"Mejor configuración de variables: {mejor_solucion_simulada.sample}")
print(f"Energía mínima alcanzada: {mejor_solucion_simulada.energy}")