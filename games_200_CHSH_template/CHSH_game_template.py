#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


dev = qml.device("default.qubit", wires=2)


def prepare_entangled(alpha, beta):
    """Construct a circuit that prepares the (not necessarily maximally) entangled state in terms of alpha and beta
    Do not forget to normalize.

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>
    """

    # QHACK #
    norm = np.sqrt(alpha**2 + beta**2)
    alpha, beta = alpha/norm, beta/norm
    angle = 2*np.arcsin(beta)
    qml.RY(angle,wires=0)
    qml.CNOT(wires=[0,1])
    # QHACK #

@qml.qnode(dev)
def chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, x, y, alpha, beta):
    """Construct a circuit that implements Alice's and Bob's measurements in the rotated bases

    Args:
        - theta_A0 (float): angle that Alice chooses when she receives x=0
        - theta_A1 (float): angle that Alice chooses when she receives x=1
        - theta_B0 (float): angle that Bob chooses when he receives x=0
        - theta_B1 (float): angle that Bob chooses when he receives x=1
        - x (int): bit received by Alice
        - y (int): bit received by Bob
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (np.tensor): Probabilities of each basis state
    """

    prepare_entangled(alpha, beta)

    # QHACK #
    alice_theta, bob_theta = None, None
    if x == 0:
        alice_theta = theta_A0
    else:
        alice_theta = theta_A1
    qml.RY(2*alice_theta,wires=0)
    
    if y == 0:
        bob_theta = theta_B0
    else:
        bob_theta = theta_B1
    qml.RY(2*bob_theta,wires=1)
    # QHACK #

    return qml.probs(wires=[0, 1])
    

def winning_prob(params, alpha, beta):
    """Define a function that returns the probability of Alice and Bob winning the game.

    Args:
        - params (list(float)): List containing [theta_A0,theta_A1,theta_B0,theta_B1]
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning the game
    """

    # QHACK #

    theta_A0, theta_A1, theta_B0, theta_B1 = params[0], params[1], params[2], params[3]

    a = (chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, 0, 0, alpha, beta))
    win1 = a[0] + a[3]

    b = (chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, 0, 1, alpha, beta))
    win2 = b[0] + b[3]

    c = (chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, 1, 0, alpha, beta))
    win3 = c[0] + c[3]

    d = (chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, 1, 1, alpha, beta))
    win4 = d[1] + d[2]

    return np.round((win1+win2+win3+win4)/4 ,5)
    # QHACK #
    

def optimize(alpha, beta):
    """Define a function that optimizes theta_A0, theta_A1, theta_B0, theta_B1 to maximize the probability of winning the game

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning
    """

    def cost(params):
        """Define a cost function that only depends on params, given alpha and beta fixed"""

    # QHACK #
        theta_A0, theta_A1, theta_B0, theta_B1 = params[0], params[1], params[2], params[3]

        a = (chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, 0, 0, alpha, beta))
        win1 = a[0] + a[3]
        
        b = (chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, 0, 1, alpha, beta))
        win2 = b[0] + b[3]
        
        c = (chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, 1, 0, alpha, beta))
        win3 = c[0] + c[3]
        
        d = (chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, 1, 1, alpha, beta))
        win4 = d[1] + d[2]
        
        return 1 - ((win1+win2+win3+win4)/4)
        
    #Initialize parameters, choose an optimization method and number of steps
    init_params = np.array([0.01, 0.01, 0.01, 0.01],requires_grad=True)
    opt = qml.AdamOptimizer(stepsize=0.8)
    steps = 100

    # QHACK #
    
    # set the initial parameter values
    params = init_params

    for epoch in range(steps):
        params = opt.step(cost, params)
        params = np.clip(opt.step(cost, params), -2 * np.pi, 2 * np.pi)
        
    # QHACK #

    return winning_prob(params, alpha, beta)


if __name__ == '__main__':
    inputs = sys.stdin.read().split(",")
    output = optimize(float(inputs[0]), float(inputs[1]))
    print(f"{output}")