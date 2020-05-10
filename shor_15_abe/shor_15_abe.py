#!/usr/bin/env -S python3 -W ignore
# coding: utf-8
################################################################################
from __future__ import print_function
import tbvaccine as tb; tb.add_hook(isolate=False, show_vars=False)
import os
import random
import numpy as np
import qiskit
from qiskit.quantum_info.operators import Operator
from qiskit import (
    IBMQ,
    QuantumRegister,
    ClassicalRegister,
    QuantumCircuit,
    Aer,
    execute,
    transpile,
)
################################################################################


##################################################
################### Token auth ###################
##################################################
token_path = "../IBMQ_token"
with open(token_path, "r") as file:
    token = file.read()
IBMQ.save_account(token, overwrite=True)


##################################################
################## Set problem ###################
##################################################
M = 15
N = 4  # Satisfy 2^N > M
x = 7  # Initialization
r = 0  # Initialization


################################################################################
##################################### Main #####################################
################################################################################
def main():
    ########## Global variables ##########
    global M, N, x, r
    
    ##################################################
    ##################### Step 4 #####################
    ##################################################
    print("########## Step 4 ##########")
    
    ########## Make circuit ##########
    circ = make_circuit()
    
    ########## Print circuit ##########
    circ_trans = transpile(circ)
    style = {"dpi":200, "showindex":True, "cregbundle":True, "margin":[1.5,1,0.5,1]}
    circ_trans.draw(output="mpl", filename="./circuit.png",
                    style=style, initial_state=True, plot_barriers=True, fold=20,)

    ########## Run job ##########
    backend = Aer.get_backend("qasm_simulator")
    shots = 4096
    job = execute(circ_trans, backend=backend, shots=shots)

    ########## Print result ##########
    result = job.result()
    result_dict = result.get_counts(circ_trans)
    
    ########## Export result ##########
    with open("result.ssv", "w") as file:
        file.write("# qubit probability\n")
        for i in result_dict:
            file.write("{0} {1:.8E}\n".format(i, result_dict[i]/shots))
            
    ##################################################
    ##################### Step 5 #####################
    ##################################################
    print("########## Step 5 ##########")
    find_factor()


################################################################################
################################################################################
################################################################################
def find_factor():
    if r % 2 == 0:
        print("r = {} is even number, continue...".format(r))
    else:
        print("r = {} is odd number, exit.".format(r))
        quit(0)
    f1 = gcd(x1=x**(r//2)-1, x2=M)
    f2 = gcd(x1=x**(r//2)+1, x2=M)
    print("At least one of followings will be the answer:")
    print("Answer1: {} = {} * {}".format(M, f1, M//f1))
    print("Answer2: {} = {} * {}".format(M, f2, M//f2))
    

################################################################################
################################################################################
################################################################################
def gcd(x1=[], x2=[]):
    """
    Euclidean algorithm
    """
    while x1*x2 != 0:
        [a, b] = sorted([x1, x2], reverse=True)  # a > b
        r = a % b  # a = b*q + r
        x1 = b
        x2 = r
    return abs(x1 - x2)


################################################################################
################################################################################
################################################################################
def make_circuit():
    ########## Initialization ##########
    qr = QuantumRegister(7)
    cr = ClassicalRegister(3)
    circ = QuantumCircuit(qr, cr)
    circ.h(0)
    circ.h(1)
    circ.h(2)
    circ.x(6)
    ########## Order finding ########## <- Under development
    circ.cnot(2, 4)
    circ.cnot(2, 5)
    circ.cswap(1, 4, 6)
    circ.cswap(1, 3, 5)
    ########## QFT ##########
    circ.barrier()
    circ.h(0)
    cs = make_cs_operator()
    ct = make_ct_operator()
    circ.append(cs, [1, 0])
    circ.append(ct, [2, 0])
    circ.barrier()
    circ.h(1)
    circ.append(cs, [2, 1])
    circ.barrier()
    circ.h(2)
    circ.swap(0, 2)
    ########## Measurement ##########
    circ.barrier()
    circ.measure([0,1,2], [2,1,0])
    ########## Return circuit ##########
    return circ

################################################################################
################################################################################
################################################################################
def make_cs_operator():
    cs_matrix = np.array([[1+0j, 0+0j, 0+0j, 0+0j],
                          [0+0j, 1+0j, 0+0j, 0+0j],
                          [0+0j, 0+0j, 1+0j, 0+0j],
                          [0+0j, 0+0j, 0+0j, 0+1j]])
    cs = Operator(cs_matrix)
    print("Operator is unitary:", cs.is_unitary())
    return cs


################################################################################
################################################################################
################################################################################
def make_ct_operator():
    ct_matrix = np.array([[1+0j, 0+0j, 0+0j, 0+0j],
                          [0+0j, 1+0j, 0+0j, 0+0j],
                          [0+0j, 0+0j, 1+0j, 0+0j],
                          [0+0j, 0+0j, 0+0j, np.exp(1j*np.pi/4)]])
    ct = Operator(ct_matrix)
    print("Operator is unitary:", ct.is_unitary())
    return ct
            
################################################################################
################################################################################
################################################################################
if __name__ == "__main__":
    main()
