# 1+1

Calculation of 0+0, 0+1, 1+0, 1+1 in parallel using quantum computer (IBM Q).

<!-- ================================================================================ -->
<!-- ================================================================================ -->
## Requirements

* `python >= 3.8.0`
* `qiskit`
* `gnuplot` (Optional)

<!-- ================================================================================ -->
<!-- ================================================================================ -->
## How to use

0. Create your IBM Q token file to `~/.IBMQ_token`.

1. `chmod u+x 1+1.py plot.gp`

2. `./1+1.py`  
   Following files will be generated:
   * `circuit.png`: Quantum circuit diagram.
   * `result.ssv`: Calculation results.
   
3. `./plot.gp` (Optional)  
   Following files will be generated:
   * `result.pdf`: Plot of `result.ssv`.
