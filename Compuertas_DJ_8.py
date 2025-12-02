import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
n = 2 # Número de variables (x1, x2)
qr = qiskit.QuantumRegister(n + 1) # n qubits para x, 1 para y
cr = qiskit.ClassicalRegister(n) # n bits clásicos para la medición

# --- 1. FUNCIÓN PARA CREAR EL ORÁCULO DE h(x) ---
def create_oracle_h(f_type: str, circuit: QuantumCircuit):
    """Implementa el oráculo U_h para dos casos conocidos."""
    
    if f_type == "f_x1_and_x2":
        # Caso: f = x1*x2. Esto resulta en h(x) = x1 XOR x2 (Balanceada/No constante)
        
        # Implementa h(x) = x1 XOR x2:
        # Aplica CNOT con control en x1 (qubit 0) sobre el qubit auxiliar (qubit n=2)
        circuit.cx(0, n)
        # Aplica CNOT con control en x2 (qubit 1) sobre el qubit auxiliar (qubit n=2)
        circuit.cx(1, n)
        
    elif f_type == "f_x1_self_dual":
        # Caso: f = x1. Esto resulta en h(x) = 0 (Constante Cero)
        # Oráculo es la identidad (no se añaden compuertas)
        pass
        
    else:
        raise ValueError("Tipo de función no implementado.")

# --- 2. ESTRUCTURA COMPLETA DEL ALGORITMO DEUTSCH-JOZSA ---

def run_deutsch_jozsa_simulation(f_type: str):
    qc = QuantumCircuit(qr, cr)

    # Inicialización: Poner qubit auxiliar |y> en estado |-> (X gate, luego H)
    qc.x(n)
    qc.h(n)

    # Poner qubits de entrada |x> en estado de superposición uniforme
    qc.h(range(n))
    
    # BARRERA (solo visualización)
    qc.barrier()
    
    # Aplicación del ORÁCULO U_h
    create_oracle_h(f_type, qc)
    
    # BARRERA (solo visualización)
    qc.barrier()
    
    # Aplicar H a los qubits de entrada nuevamente
    qc.h(range(n))

    # Medición de los qubits de entrada |x>
    qc.measure(range(n), range(n))
    
    # Simulación
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    print(f"\n--- Resultado para {f_type.upper()} ---")
    print("Conteo de mediciones:", counts)
    
    # Mostrar el circuito (útil para la documentación del TFG)
    # print(qc.draw(output='mpl')) 
    
    return counts

# --- EJECUCIÓN DE PRUEBAS ---

# 1. Prueba: f = x1*x2 (NO Auto-Dual). Esperamos resultados != |00>
run_deutsch_jozsa_simulation("f_x1_and_x2") 

# 2. Prueba: f = x1 (Auto-Dual). Esperamos 100% de resultados en |0>
run_deutsch_jozsa_simulation("f_x1_self_dual")