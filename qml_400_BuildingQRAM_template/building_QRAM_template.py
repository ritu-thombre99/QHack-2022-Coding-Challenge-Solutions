#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def qRAM(thetas):
    """Function that generates the superposition state explained above given the thetas angles.

    Args:
        - thetas (list(float)): list of angles to apply in the rotations.

    Returns:
        - (list(complex)): final state.
    """

    # QHACK #

    # Use this space to create auxiliary functions if you need it.
    def get_unitary(theta):
        RY = [[0,0],[0,0]]
        RY[0][0] = np.cos(theta/2)
        RY[0][1] = -np.sin(theta/2)
        RY[1][0] = np.sin(theta/2)
        RY[1][1] = np.cos(theta/2)
        RY = np.array(RY)
        U = []
        for i in range(16):
            state = np.zeros(16)
            if i<14:
                state[i] = 1
            elif i == 14:
                state[14] = np.cos(theta/2)
                state[15] = -np.sin(theta/2)
            elif i == 15:
                state[14] = np.sin(theta/2)
                state[15] = np.cos(theta/2)
            U.append(state)
        U = np.array(U)
        return U
                
                

    # QHACK #

    dev = qml.device("default.qubit", wires=range(4))

    @qml.qnode(dev)
    def circuit():

        # QHACK #
        qml.Hadamard(0)
        qml.Hadamard(1)
        qml.Hadamard(2)
        arr = ['000','001','010','011','100','101','110','111']
        # Create your circuit: the first three qubits will refer to the index, the fourth to the RY rotation.
        for i,index in enumerate(arr):
            for j in range(len(index)):
                if index[j] == '0':
                    qml.PauliX(j)
            U = get_unitary(thetas[i])
            qml.QubitUnitary(U, wires=[0, 1, 2, 3]) 
            for j in range(len(index)):
                if index[j] == '0':
                    qml.PauliX(j)
        # QHACK #

        return qml.state()

    return circuit()


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    thetas = np.array(inputs, dtype=float)

    output = qRAM(thetas)
    output = [float(i.real.round(6)) for i in output]
    print(*output, sep=",")
