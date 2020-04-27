#!/usr/bin/env python3
# coding: utf-8
################################################################################
from __future__ import print_function
import tbvaccine as tb; tb.add_hook(isolate=False, show_vars=False)
import os
import random
import numpy as np
from qiskit import (
    IBMQ,
    QuantumRegister,
    ClassicalRegister,
    QuantumCircuit,
    Aer,
    execute,
    transpile
)
################################################################################


##################################################
################### Token auth ###################
##################################################
token_path = os.environ["HOME"] + "/" + ".IBMQ_token"
with open(token_path, "r") as file:
    token = file.read()
IBMQ.save_account(token, overwrite=True)


##################################################
################## Set problem ###################
##################################################
M = 15


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
def pick_random_x():
    """
    Pick up x (1 <= x <= M-1) randomly, then:
    * gcd(x,M) == 1 -> return x, continue...
    * gcd(x,M) != 1 -> gcd(x,M) is factor of M, exit.
    """
    x = random.randint(1, M-1)
    while (g := gcd(x, M)) != 1:
        print("M contains {} as a factor, exit.".format(g))
        print("Answer: {} = {} * {}".format(M, g, M//g))
        quit(0)
        x = random.randint(1, M-1)
    return x


################################################################################
################################################################################
################################################################################
def check_exp():
    """
    Answer Yes / No:
    M = a^b (a>=1, b>=2)
    """
    for b in range(2, M):
        a = M**(1/b)
        if a.is_integer():
            print("M contains {} as a factor, exit.".format(int(a)))
            print("Answer: {} = {} * {}".format(M, int(a), b))
            quit(0)
        elif a < 2.0:
            print("M does NOT consist of a^b, continue...")
            break


################################################################################
################################################################################
################################################################################
def check_even_odd():
    if M % 2 == 0:
        print("M contains 2 as a factor, exit.")
        print("Answer: {} = {} * {}".format(M, 2, M//2))
        quit(0)
    else:
        print("M does NOT contain 2 as a factor, continue...")
        

################################################################################
##################################### Main #####################################
################################################################################
def main():
    ##################################################
    ################## Make circuit ##################
    ##################################################
    ########## Initialization ##########
    qr = QuantumRegister(5)
    cr = ClassicalRegister(4)
    circ = QuantumCircuit(qr, cr)
    circ.h(0)
    circ.h(1)
    circ.h(2)
    circ.h(3)
    circ.x(4)
    ########## Order finding ########## <- Incorrect!!
    circ.barrier()
    repetitions = 1
    for counting_qubit in range(4):
        for i in range(repetitions):
            circ.cu1(np.pi/4, counting_qubit, 4)
        repetitions *= 2
    ########## QFT^(-1) ########## <- May be correct
    circ.barrier()
    circ.swap(0, 3)
    circ.swap(1, 2)
    circ.barrier()
    circ.h(3)
    circ.barrier()
    circ.cu1(-np.pi/2, 3, 2)
    circ.h(2)
    circ.barrier()
    circ.cu1(-np.pi/4, 3, 1)
    circ.cu1(-np.pi/2, 2, 1)
    circ.h(1)
    circ.barrier()
    circ.cu1(-np.pi/8, 3, 0)
    circ.cu1(-np.pi/4, 2, 0)
    circ.cu1(-np.pi/2, 1, 0)
    circ.h(0)
    ########## Measurement ##########
    circ.barrier()
    circ.measure([0,1,2,3], [3,2,1,0])

    ##################################################
    ################# Print circuit ##################
    ##################################################
    circ_trans = transpile(circ)
    style = {"dpi":200, "showindex":True, "cregbundle":True, "margin":[1.5,1,0.5,1]}
    circ_trans.draw(output="mpl", filename="./circuit.png", style=style, initial_state=True, plot_barriers=True, fold=20, justify="left")

    ##################################################
    #################### Run job #####################
    ##################################################
    backend = Aer.get_backend("qasm_simulator")
    shots = 4096
    job = execute(circ_trans, backend=backend, shots=shots)

    ##################################################
    ################## Print result ##################
    ##################################################
    result = job.result()
    result_dict = result.get_counts(circ_trans)
    ########## Export result ##########
    with open("result.ssv", "w") as file:
        file.write("# qubit probability\n")
        for i in result_dict:
            file.write("{0} {1:.8E}\n".format(i, result_dict[i]/shots))

            
################################################################################
################################################################################
################################################################################
if __name__ == "__main__":
    main()
