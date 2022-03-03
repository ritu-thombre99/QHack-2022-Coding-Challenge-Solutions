import sys
import pennylane as qml
from pennylane import numpy as np
from pennylane import hf


def ground_state_VQE(H):
    """Perform VQE to find the ground state of the H2 Hamiltonian.

    Args:
        - H (qml.Hamiltonian): The Hydrogen (H2) Hamiltonian

    Returns:
        - (float): The ground state energy
        - (np.ndarray): The ground state calculated through your optimization routine
    """

    # QHACK #

    dev = qml.device("default.qubit", wires=4)
    
    hf = np.array([1, 1, 0, 0])
    def circuit(param, wires):
        qml.BasisState(hf, wires=wires)
        qml.DoubleExcitation(param, wires=[0, 1, 2, 3])
    @qml.qnode(dev)
    def cost_fn(param):
        circuit(param, wires=range(4))
        return qml.expval(H)

    def get_state(theta):
        state = np.zeros(16)
        state[12] = np.cos(theta/2)
        state[3] = -np.sin(theta/2)
        return state
        
    opt = qml.GradientDescentOptimizer(stepsize=0.4)
    theta = np.array(0.0, requires_grad=True)
    energy = [cost_fn(theta)]

    # store the values of the circuit parameter
    angle = [theta]

    max_iterations = 100
    conv_tol = 1e-07
    for n in range(max_iterations):
        theta, prev_energy = opt.step_and_cost(cost_fn, theta)
        energy.append(cost_fn(theta))
        angle.append(theta)
        conv = np.abs(energy[-1] - prev_energy)
        if conv <= conv_tol:
            break

    state = np.zeros(16)
    state[12] = 1.
    return energy[-1],state


    # QHACK #


def create_H1(ground_state, beta, H):
    """Create the H1 matrix, then use `qml.Hermitian(matrix)` to return an observable-form of H1.

    Args:
        - ground_state (np.ndarray): from the ground state VQE calculation
        - beta (float): the prefactor for the ground state projector term
        - H (qml.Hamiltonian): the result of hf.generate_hamiltonian(mol)()

    Returns:
        - (qml.Observable): The result of qml.Hermitian(H1_matrix)
    """

    # QHACK #
    a = qml.utils.sparse_hamiltonian(H).toarray()
    b = beta*(np.outer(ground_state, np.conj(ground_state)).numpy())
    
    return qml.Hermitian(a+b,wires=range(4))
    
    # QHACK #


def excited_state_VQE(H1):
    """Perform VQE using the "excited state" Hamiltonian.

    Args:
        - H1 (qml.Observable): result of create_H1

    Returns:
        - (float): The excited state energy
    """

    # QHACK #
    dev = qml.device("default.qubit", wires=4)
    hf = np.array([1, 0, 0, 1])
    def circuit(param, wires):
        qml.BasisState(hf, wires=wires)
        qml.DoubleExcitation(param, wires=[1, 2, 0 ,3])
    @qml.qnode(dev)
    def cost_fn(param):
        circuit(param, wires=range(4))
        return qml.expval(H1)
        
    opt = qml.AdagradOptimizer(stepsize=0.8)
    theta = np.array(0.0, requires_grad=True)
    energy = [cost_fn(theta)]

    # store the values of the circuit parameter
    angle = [theta]

    max_iterations = 1000
    conv_tol = 1e-08
    for n in range(max_iterations):
        theta, prev_energy = opt.step_and_cost(cost_fn, theta)
        energy.append(cost_fn(theta))
        angle.append(theta)
        conv = np.abs(energy[-1] - prev_energy)
        if conv <= conv_tol:
            break
    return energy[-1]

    # QHACK #


if __name__ == "__main__":
    coord = float(sys.stdin.read())
    symbols = ["H", "H"]
    geometry = np.array([[0.0, 0.0, -coord], [0.0, 0.0, coord]], requires_grad=False)
    mol = hf.Molecule(symbols, geometry)

    H = hf.generate_hamiltonian(mol)()
    E0, ground_state = ground_state_VQE(H)

    beta = 15.0
    H1 = create_H1(ground_state, beta, H)
    E1 = excited_state_VQE(H1)

    answer = [np.real(E0), E1]
    print(*answer, sep=",")
