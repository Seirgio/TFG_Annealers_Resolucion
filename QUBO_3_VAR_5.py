# --- Prueba 5: Estructura QUBO para una FBP compleja (3 variables) ---
import dimod
from dimod.reference.samplers import ExactSolver

# Este QUBO representa (f - f^D)^2 para una FBP más grande,
# reflejando una matriz Q densa (con muchos términos cuadráticos x_i * x_j).
# Los coeficientes son solo ilustrativos de la complejidad:

Q_COMPLEJO = {
    ('x1', 'x1'): 3.0,      ('x2', 'x2'): 5.0,      ('x3', 'x3'): -2.0,  # Términos lineales (diagonales)
    ('x1', 'x2'): -7.5,    # Interacción entre x1 y x2
    ('x1', 'x3'): 2.0,     # Interacción entre x1 y x3
    ('x2', 'x3'): 10.0     # Interacción entre x2 y x3
}

modelo_qubo_comp = dimod.BQM.from_qubo(Q_COMPLEJO)

# Solucionador Exacto (2^3 = 8 estados, muy rápido)
sampler_exacto = ExactSolver()
resultados_pd_comp_exactos = sampler_exacto.sample(modelo_qubo_comp)

print("\n--- PRUEBA 5: ESTRUCTURA DE QUBO COMPLEJO (f - f^D)^2 ---")
print("Top 3 Configuraciones de Mínima Energía:")

# Imprimimos las 3 mejores soluciones (CORREGIDO: uso de list() para permitir el slicing)
for sample, energy in list(resultados_pd_comp_exactos.data(fields=['sample', 'energy'], sorted_by='energy'))[:3]:
    print(f"Configuración {sample}: Energía {energy}")
    
#Debido Dado que tu Hamiltoniano de coste real es $(f-f^D)^2$, 
# la matriz QU no debe producir energías negativas.