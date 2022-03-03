import sys
import pennylane as qml
from pennylane import numpy as np


def second_renyi_entropy(rho):
    """Computes the second Renyi entropy of a given density matrix."""
    # DO NOT MODIFY anything in this code block
    rho_diag_2 = np.diagonal(rho) ** 2.0
    return -np.real(np.log(np.sum(rho_diag_2)))


def compute_entanglement(theta):
    """Computes the second Renyi entropy of circuits with and without a tardigrade present.

    Args:
        - theta (float): the angle that defines the state psi_ABT

    Returns:
        - (float): The entanglement entropy of qubit B with no tardigrade
        initially present
        - (float): The entanglement entropy of qubit B where the tardigrade
        was initially present
    """

    dev = qml.device("default.qubit", wires=3)

    # QHACK #
    @qml.qnode(dev)
    def get_mu_b():
        qml.Hadamard(0)
        qml.CNOT(wires=[0,1])
        qml.X(1)
        return qml.density_matrix([0,1])
    @qml.qnode(dev)
    def get_rho_b():
        qml.Hadamard(0)
        qml.X(0)
        qml.CRY(theta, wires=[0,1])
        qml.X(0)
        qml.CNOT(wires=[1,2])
        qml.X(1)
        qml.CNOT(wires=[0,1])
        return qml.density_matrix([1])
    
    
    S2_without_tardigrade = second_renyi_entropy(get_mu_b()) 
    S2_with_tardigrade = second_renyi_entropy(get_rho_b())
    return S2_without_tardigrade, S2_with_tardigrade
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    theta = np.array(sys.stdin.read(), dtype=float)

    S2_without_tardigrade, S2_with_tardigrade = compute_entanglement(theta)
    print(*[S2_without_tardigrade, S2_with_tardigrade], sep=",")
