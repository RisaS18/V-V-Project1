# AI Usage Log

## 1. Cocotb Testbench Setup

**Prompt / Assistance:** Asked for help organizing the Cocotb testbench and connecting the testbench to the SystemVerilog FIFO design.

**Prediction:** A Cocotb testbench could drive the FIFO inputs, monitor its outputs, and compare the results against a Python reference model.

**Evidence:** The testbench successfully compiled and ran using Cocotb and Verilator. The directed tests and randomized tests completed with no scoreboard mismatches.

**Fix / Outcome:** Organized the testbench into a driver, monitor, reference model, and scoreboard. Corrected file paths and Makefile settings to match the project directory structure.

## 2. Reference Model and Scoreboard Debugging

**Prompt / Assistance:** Asked for help implementing a Python FIFO reference model and checking the DUT's count, full, empty, and read data signals.

**Prediction:** A queue-based reference model would provide the expected FIFO behavior and identify incorrect DUT outputs.

**Evidence:** The scoreboard detected mismatches when intentionally modified FIFO designs produced incorrect status, count, or data values.

**Fix / Outcome:** Used a Python deque to model FIFO contents. Updated the scoreboard to compare the DUT against the reference model after each clock cycle.

## 3. Randomized Testing with pyvsc

**Prompt / Assistance:** Asked how to generate randomized FIFO read and write transactions using pyvsc.

**Prediction:** Randomized transactions would exercise combinations of read enable, write enable, and write data beyond the directed test sequences.

**Evidence:** The pyvsc transaction class successfully generated randomized values, and the randomized test completed 500 transactions without scoreboard mismatches.

**Fix / Outcome:** Created a randomized transaction class containing read enable, write enable, and 8-bit write data. Corrected the order of variable assignments so that randomized values were assigned before being logged and applied to the DUT.

## 4. Functional Coverage and Coverage Convergence

**Prompt / Assistance:** Asked how to implement functional coverage and measure coverage convergence using pyvsc.

**Prediction:** Coverpoints for occupancy, read requests, write requests, and boundary combinations would show which defined verification scenarios had been exercised.

**Evidence:** The functional coverage model reached 100% overall coverage. In a separate randomized-only convergence experiment, coverage reached 98.33% after 50 transactions and 100% after 100 transactions. It remained at 100% through 500 transactions.

**Fix / Outcome:** Created a pyvsc covergroup and used a separate coverage instance for randomized-only convergence measurements so that directed tests did not affect the convergence results.

## 5. Mutation Testing

**Prompt / Assistance:** Asked for help running the released FIFO mutation pool and interpreting the results.

**Prediction:** Mutations that introduced incorrect FIFO behavior should be detected by the testbench and scoreboard.

**Evidence:** All eight released mutants were detected. The failures included incorrect full and empty flags, overflow and underflow behavior, count updates, read data selection, corrupted stored data, and pointer wraparound.

**Fix / Outcome:** Corrected Verilator width warnings in the mutant files without changing the intended mutations. Re-ran each mutant and documented the results in `FINDINGS.md`. The released mutation score was 8/8 (100%).

## 6. Overall AI Usage

AI assistance was used to explain verification concepts, help organize the testbench, troubleshoot errors, and interpret simulation and coverage results. The testbench was executed using Cocotb and Verilator, and the reported results were based on actual simulation output. AI-generated suggestions were checked against the project files and simulation results.
