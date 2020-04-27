#!/usr/bin/env python3
# coding: utf-8
################################################################################
from __future__ import print_function
# import tbvaccine as tb; tb.add_hook(isolate=False, show_vars=False)
import os
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


################################################################################
##################################### Main #####################################
################################################################################
def main():
    ##################################################
    ################## Make circuit ##################
    ##################################################
    q_alice = QuantumRegister(2)
    q_bob = QuantumRegister(1)
    c0 = ClassicalRegister(1)
    c1 = ClassicalRegister(1)
    c_bob = ClassicalRegister(1)
    c_alice = ClassicalRegister(1)
    circ = QuantumCircuit(q_alice, q_bob, c0, c1, c_bob, c_alice)
    circ.h(0)
    circ.h(1)
    circ.barrier()
    circ.measure(q_alice[0], c_alice)
    circ.barrier()
    circ.cx(q_alice[1], q_bob)
    circ.cx(q_alice[0], q_alice[1])
    circ.h(q_alice[0])
    circ.barrier()
    circ.measure(q_alice[0], c0)
    circ.measure(q_alice[1], c1)
    circ.barrier()
    circ.x(q_bob).c_if(c1, 1)
    circ.z(q_bob).c_if(c0, 1)
    circ.barrier()
    circ.measure(q_bob, c_bob)

    ##################################################
    ################# Print circuit ##################
    ##################################################
    circ_trans = transpile(circ)
    style = {"dpi":200, "showindex":True, "cregbundle":False, "margin":[1.5,1,0.5,1]}
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
        file.write("# qubit(c_alice c_bob c1 c0) probability\n")
        for i in result_dict:
            file.write("{0} {1:.8E}\n".format(i.replace(" ",""), result_dict[i]/shots))

            
################################################################################
################################################################################
################################################################################
if __name__ == "__main__":
    main()
