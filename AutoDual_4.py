import dimod
from dimod.reference.samplers import ExactSolver

# --- Prueba 4: Auto-Dualidad para f = x1 AND x2 ---

# Hamiltoniano de Coste (H_PD): H = x1 + x2 + 8*x1*x2
# Esto representa (f - f^D)^2 para f = x1 AND x2
Q_PD = {
    ('x1', 'x1'): 1,
    ('x2', 'x2'): 1,
    ('x1', 'x2'): 8   # Coeficiente cuadrático (8 * x1 * x2)
}

modelo_qubo_pd = dimod.BQM.from_qubo(Q_PD)

sampler_exacto = ExactSolver()
resultados_pd_exactos = sampler_exacto.sample(modelo_qubo_pd)

print("\n--- PRUEBA 4: AUTO-DUALIDAD PARA f = x1 AND x2 ---")

# Imprimimos todas las soluciones ordenadas por energía
for sample, energy in resultados_pd_exactos.data(fields=['sample', 'energy']):
    # La solución de auto-dualidad se cumple si H=0
    # La energía representa la diferencia cuadrática entre f y f^D
    logica = "f = f^D (Auto-Dualidad SÍ se cumple en esta entrada)" if energy == 0 else f"f != f^D (Penalización: {energy})"
    print(f"Configuración {sample}: Energía {energy} -> {logica}")