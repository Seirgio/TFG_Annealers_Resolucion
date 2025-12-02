import dimod
from dimod.reference.samplers import ExactSolver
import neal
from dwave.system import EmbeddingComposite 

# --- PRUEBA DE 3 VARIABLES (f = x1 OR (x2 AND x3)) ---

# Q generada del Hamiltoniano: H = x1 + x2*x3 - x1*x2 - x1*x3
Q_3var = {
    ('x1', 'x1'): 1.0,  # x1
    ('x2', 'x2'): 0.0,  # (No hay término x2 lineal)
    ('x3', 'x3'): 0.0,  # (No hay término x3 lineal)
    
    ('x2', 'x3'): 1.0,  # x2*x3
    ('x1', 'x2'): -1.0, # -x1*x2
    ('x1', 'x3'): -1.0  # -x1*x3
}

modelo_qubo_3var = dimod.BQM.from_qubo(Q_3var)

print("-------------------------------------------------------")
print("--- MATRIZ QUBO GENERADA para f = x1 OR (x2 AND x3) ---")
print("-------------------------------------------------------")
for (var1, var2), coef in Q_3var.items():
    if var1 == var2:
        print(f"  Término Lineal {var1}: {coef}")
    else:
        print(f"  Acoplamiento {var1}*{var2}: {coef}")
print("-------------------------------------------------------")

# --- SIMULACIÓN EXACTA (3 Variables) ---

sampler_exacto = ExactSolver()
resultados_exactos_3var = sampler_exacto.sample(modelo_qubo_3var)

print("\n--- RESULTADOS DEL SOLUCIONADOR EXACTO (3 Variables) ---")

# Imprimimos todos los 2^3 = 8 estados
for sample, energy in list(resultados_exactos_3var.data(fields=['sample', 'energy'], sorted_by='energy')):
    # Mapeo lógico: H=0 significa que f = f^D en esa entrada
    logica = "SÍ (f = f^D)" if energy == 0 else f"NO (H = {energy})"
    print(f"Configuración {sample}: ¿Auto-Dual? -> {logica}")
    
# Mapeo QUBO con exito para un problema de 3 variables. Los resultados confirman 
# que f NO es auto-dual globalmente, ya que el Hamiltoniano H alcanza un valor de $1.0$
# (no es 0 en todas las entradas).

# Nota sobre HOBO: Aunque en este caso los términos HOBO se cancelaron, este es el punto donde 
# se aplicaría la reducción HOBO a QUBO si los términos no se hubieran cancelado.