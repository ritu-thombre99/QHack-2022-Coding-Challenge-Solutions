import sys
import pennylane as qml
from pennylane import numpy as np

NUM_WIRES = 6


def triple_excitation_matrix(gamma):
    """The matrix representation of a triple-excitation Givens rotation.

    Args:
        - gamma (float): The angle of rotation

    Returns:
        - (np.ndarray): The matrix representation of a triple-excitation
    """

    # QHACK #
    b1 = int('000111',2)
    b2 = int('111000',2)
    U = []
    for i in range(64):
        state = np.zeros(64)
        if i == b1:
            state[b1] = np.cos(gamma/2)
            state[b2] = np.sin(gamma/2)
        elif i == b2:
            state[b1] = -np.sin(gamma/2)
            state[b2] = np.cos(gamma/2)
        else:
            state[i] = 1.
        U.append(state)
    return np.array(U)
            
    # QHACK #


dev = qml.device("default.qubit", wires=6)


@qml.qnode(dev)
def circuit(angles):
    """Prepares the quantum state in the problem statement and returns qml.probs

    Args:
        - angles (list(float)): The relevant angles in the problem statement in this order:
        [alpha, beta, gamma]

    Returns:
        - (np.tensor): The probability of each computational basis state
    """

    # QHACK #
    alpha, beta, gamma = angles[0],angles[1],angles[2]
    qml.PauliX(0)
    qml.PauliX(1)
    qml.PauliX(2)
    qml.SingleExcitation(alpha, wires=[0,5])
    qml.DoubleExcitation(beta, wires=[0, 1, 4, 5])
    TripleExcitation = triple_excitation_matrix(gamma)
    qml.QubitUnitary(TripleExcitation,wires=range(6))
    # QHACK #

    return qml.probs(wires=range(NUM_WIRES))


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = np.array(sys.stdin.read().split(","), dtype=float)
    probs = circuit(inputs).round(6)
    print(*probs, sep=",")
