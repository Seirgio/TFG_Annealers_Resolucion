import dimod
import neal

# Matriz QUBO para f = x1 AND x2
Q_final_and = {
    ('x1', 'x1'): 1.0, 
    ('x2', 'x2'): 1.0, 
    ('x1', 'x2'): -2.0
}

modelo_qubo = dimod.BQM.from_qubo(Q_final_and)

# ----------------------------------------
# A) Recocido Simulado (Heurístico)
# ----------------------------------------

print("\n-------------------------------------------------------")
print("--- PRUEBA DE RECOCIDO SIMULADO (neal) ---")
print("-------------------------------------------------------")

sampler_neal = neal.SimulatedAnnealingSampler()

# Ejecutar la simulación 1000 veces
resultados_neal = sampler_neal.sample(modelo_qubo, num_reads=1000)

mejor_solucion_neal = resultados_neal.first
print(f"Mejor Energía (Recocido Simulado, H_min): {mejor_solucion_neal.energy}")
print(f"Muestra con energía mínima: {mejor_solucion_neal.sample}")

# Imprimimos las 3 mejores soluciones encontradas
print("\nTop 3 Soluciones encontradas (frecuencia):")
# FIX: Se convierte el generador a lista para poder indexar [:3]
for sample, energy, count in list(resultados_neal.data(fields=['sample', 'energy', 'num_occurrences'], sorted_by='energy'))[:3]:
    # Hacemos el mapeo lógico para entender el resultado
    logica = "f = f^D (Auto-Dualidad SÍ se cumple)" if energy == 0 else f"f != f^D (Penalización: {energy})"
    print(f"Configuración {sample}: Energía {energy} (Ocurrencias: {count}) -> {logica}")