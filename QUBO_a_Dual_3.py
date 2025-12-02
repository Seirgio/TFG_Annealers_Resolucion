import dimod
from dimod.reference.samplers import ExactSolver

# --- Prueba 3: Restricción AND (x1 AND x2) ---

# QUBO para penalizar cuando x1 AND x2 es falso.
# H = x1 + x2 - 2*x1*x2
Q_AND = {
    ('x1', 'x1'): 1,  # Coeficiente lineal de x1
    ('x2', 'x2'): 1,  # Coeficiente lineal de x2
    ('x1', 'x2'): -2  # Coeficiente cuadrático (interacción)
}

modelo_qubo_and = dimod.BQM.from_qubo(Q_AND)

# ----------------------------------------------------
# A) Solucionador Exacto
# ----------------------------------------------------
sampler_exacto = ExactSolver()
resultados_and_exactos = sampler_exacto.sample(modelo_qubo_and)

print("--- SOLUCIÓN EXACTA PARA (x1 AND x2) ---")
# Imprimimos todas las soluciones ordenadas por energía
for sample, energy in resultados_and_exactos.data(fields=['sample', 'energy']):
    # Mapeamos la energía de H a la lógica (0=Verdadero, >0=Falso)
    logica = "VERDADERO (Cumple)" if energy == 0 else f"FALSO (Penalización: {energy})"
    print(f"Configuración {sample}: Energía {energy} -> {logica}")