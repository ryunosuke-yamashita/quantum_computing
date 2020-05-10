# Shor's Algorithm (15 = 3*5)

Implementation of Shor's algorithm (15 = 3*5) based on Dr. Abe [^1]'s lecture at Keio university.

[^1]: https://www.appi.keio.ac.jp/Itoh_group/abe/english.html

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

1. `chmod u+x shor_15_abe.py plot.gp`.

2. `./shor_15_abe.py`  
   Following files will be generated:
   * `circuit.png`: Quantum circuit diagram.
   * `result.ssv`: Calculation results.
   
3. `./plot.gp` (Optional)  
   Following files will be generated:
   * `result.pdf`: Plot of `result.ssv`.

<!-- ================================================================================ -->
<!-- ================================================================================ -->
## References

* https://www.appi.keio.ac.jp/Itoh_group/abe/pdf/ap2019_2.pdf (Japanese)
* https://www.youtube.com/watch?v=YBo36vtLObM (Japanese)
