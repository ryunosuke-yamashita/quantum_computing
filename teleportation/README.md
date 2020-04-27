# Quantum Teleportation

<!-- ================================================================================ -->
<!-- ================================================================================ -->
## Requirements

* `python >= 3.8.0`
* `qiskit`
* `perl 5.x`

<!-- ================================================================================ -->
<!-- ================================================================================ -->
## Calculation

0. Create your IBM Q token file to `~/.IBMQ_token`.

1. `chmod u+x 1+1.py ssv2ssv.pl plot.gp`.

2. `./1+1.py`  
   Following files will be generated:
   * `circuit.png`: Quantum circuit diagram.
   * `result.ssv`: Calculation results.

3. `./ssv2ssv.pl > result_bob.ssv` (Optional)
   
4. `./plot.gp` (Optional)  
   Following files will be generated:
   * `result.pdf`: Plot of `result_bob.ssv`.
