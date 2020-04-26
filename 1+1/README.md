# 1+1

Calculate 0+0, 0+1, 1+0, 1+1 in parallel using quantum computer (IBM Q).

<!-- ================================================================================ -->
<!-- ================================================================================ -->
## Requirements

* `python >= 3.8.0`
* `qiskit`

<!-- ================================================================================ -->
<!-- ================================================================================ -->
## Calculation

0. Create your IBM Q token file to `~/.IBMQ_token`.

1. `python 1+1.py`
   Following files will be generated:
   * `circuit.png`: Quantum circuit diagram.
   * `result.ssv`: Calculation results.
   
2. `gnuplot plot.gp`
   Following files will be generated:
   * `result.pdf`: Plot of `result.ssv`.
