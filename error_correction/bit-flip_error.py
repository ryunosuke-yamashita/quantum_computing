#!/usr/bin/env -S python3 -W ignore
# coding: utf-8
################################################################################
from __future__ import print_function
import tbvaccine as tb; tb.add_hook(isolate=False, show_vars=False)
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
token_path = "../IBMQ_token"
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
    q = QuantumRegister(3)
    c = ClassicalRegister(3)
    circ = QuantumCircuit(q, c)
    circ.x(q[0])  # |psi> = |1>
    ########## Encoding ##########
    circ.barrier()
    circ.cx(q[0], q[1])
    circ.cx(q[0], q[2])
    ########## Bit filp error ##########
    circ.barrier()
    circ.x(q[0])
    ########## Decoding ##########
    circ.barrier()
    circ.cx(q[0], q[2])
    circ.cx(q[0], q[1])
    circ.measure(q[1], c[1])
    circ.measure(q[2], c[2])
    circ.x(q[0]).c_if(c, 6)  # "c_if(c, 6)" means "if c[2]c[1]c[0]==110"
    circ.barrier()
    ########## Measurement ##########
    circ.measure(q[0], c[0])

    ##################################################
    ################# Print circuit ##################
    ##################################################
    circ_trans = transpile(circ)
    style = {"dpi":200, "showindex":True, "cregbundle":False, "margin":[1.5,1,0.5,1]}
    circ_trans.draw(output="mpl", filename="./bit-flip_error.png",
                    style=style, initial_state=True, plot_barriers=True, fold=20)

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
    with open("bit-flip_error.ssv", "w") as file:
        file.write("# qubit probability\n")
        for i in result_dict:
            file.write("{0} {1:.8E}\n".format(i, result_dict[i]/shots))

            
################################################################################
################################################################################
################################################################################
if __name__ == "__main__":
    main()
