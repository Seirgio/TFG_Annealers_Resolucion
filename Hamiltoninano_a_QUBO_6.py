import collections
from itertools import combinations
import dimod
from dimod.reference.samplers import ExactSolver

# Usamos un Counter para manejar fácilmente la suma de coeficientes
Polynomial = collections.Counter

def expand_sq_to_qubo(poly: Polynomial) -> dict:
    """
    Toma un polinomio P (como Counter de términos) y calcula la matriz QUBO Q
    que representa P^2, aplicando la regla x_i^2 = x_i.
    """
    Q = collections.defaultdict(float)

    poly_list = list(poly.items())
    
    # I. Expansión P^2 (producto de todos los pares de términos diferentes: 2AB)
    for i in range(len(poly_list)):
        for j in range(i + 1, len(poly_list)):
            (term1, coeff1) = poly_list[i]
            (term2, coeff2) = poly_list[j]

            new_term_set = set(term1) | set(term2)
            new_coeff = 2 * coeff1 * coeff2 

            # Simplificación y truncamiento a QUBO (grado <= 2)
            if len(new_term_set) > 2:
                continue
            
            if len(new_term_set) == 2:
                Q[tuple(sorted(list(new_term_set)))] += new_coeff
            elif len(new_term_set) == 1:
                Q[tuple(new_term_set)] += new_coeff

    # II. Expansión P^2 (producto de cada término consigo mismo: A^2)
    for term, coeff in poly.items():
        new_coeff = coeff * coeff
        
        # Aplicamos x_i^2 = x_i
        if len(term) == 2: # Ej: (x1*x2)^2 = x1*x2
            Q[term] += new_coeff
        elif len(term) == 1: # Ej: x1^2 = x1
            Q[term] += new_coeff
        
    return dict(Q)


def generar_qubo_autodualidad(f_terms: list[list[str]]) -> dict:
    """
    Genera la matriz Q (como diccionario QUBO) para el Hamiltoniano
    H = (f - f^D)^2 de una Función Booleana Positiva f.
    """
    
    f_poly = Polynomial()
    for term_vars in f_terms:
        f_poly[tuple(sorted(term_vars))] = 1.0

    # CASO DE PRUEBA: f = x1 AND x2
    if f_terms == [['x1', 'x2']]:
        f_poly = {('x1', 'x2'): 1.0}
        # f^D = x1 OR x2 = x1 + x2 - x1*x2
        fD_poly = {('x1',): 1.0, ('x2',): 1.0, ('x1', 'x2'): -1.0}
    else:
        raise NotImplementedError("Solo se ha codificado el caso de prueba f=x1*x2.")

    # 2. Construir la diferencia (f - f^D)
    # FIX: Usamos defaultdict para prevenir KeyError en la resta
    diff_poly = collections.defaultdict(float, f_poly) 
    
    for term, coeff in fD_poly.items():
        diff_poly[term] -= coeff
    
    # 3. y 4. Elevar al cuadrado (f - f^D)^2 y convertir a QUBO
    Q_dict = expand_sq_to_qubo(diff_poly)
    
    # Formato final QUBO (solo términos de grado 1 y 2)
    final_qubo = {}
    for term, coeff in Q_dict.items():
        if len(term) == 1:
            final_qubo[(term[0], term[0])] = coeff # Término lineal: x1 -> ('x1', 'x1')
        elif len(term) == 2:
            final_qubo[term] = coeff # Término cuadrático: (x1, x2)
    
    return final_qubo

# --- EJEMPLO DE USO ---

try:
    Q_final_and = generar_qubo_autodualidad([['x1', 'x2']])
    
    # NUEVO FORMATO DE IMPRESIÓN PARA LA MATRIZ QUBO
    print("-------------------------------------------------------")
    print("--- MATRIZ QUBO GENERADA para H = (f - f^D)^2, f = x1 AND x2 ---")
    print("-------------------------------------------------------")
    print("Términos Lineales (Diagonal Q_ii):")
    lineales = {k[0]: v for k, v in Q_final_and.items() if k[0] == k[1]}
    for var, coef in lineales.items():
        print(f"  {var}: {coef}")
        
    print("\nTérminos de Acoplamiento (Fuera de la Diagonal Q_ij):")
    acoplamiento = {k: v for k, v in Q_final_and.items() if k[0] != k[1]}
    for var_pair, coef in acoplamiento.items():
        print(f"  {var_pair[0]} * {var_pair[1]}: {coef}")
    print("-------------------------------------------------------")

    # ----------------------------------------
    # Ejecución de la Prueba (Verificación)
    # ----------------------------------------
    modelo_qubo = dimod.BQM.from_qubo(Q_final_and)
    sampler_exacto = ExactSolver()
    resultados = sampler_exacto.sample(modelo_qubo)

    print("\n--- RESULTADOS DEL SOLUCIONADOR EXACTO ---")
    # Recordatorio: H = x1 + x2 + 8*x1*x2
    for sample, energy in list(resultados.data(fields=['sample', 'energy'], sorted_by='energy'))[:]:
        logica = "f = f^D (Auto-Dualidad SÍ se cumple)" if energy == 0 else f"f != f^D (Penalización: {energy})"
        print(f"Configuración {sample}: Energía {energy} -> {logica}")

except NotImplementedError as e:
    print(f"Error: {e}. Por favor, modifique la función para su caso de prueba.")