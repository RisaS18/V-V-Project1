# V-V-Project1: Constrained-Random FIFO Verification

**Author:** Risa Suzuki  
**NID:** ri710407  
**Course:** EEE 4701 / EEE 5703

## Project Overview

This project verifies a synchronous FIFO using SystemVerilog, Cocotb, Verilator, and pyvsc constrained-random stimulus.

## Project Structure

- `code/dut/` - FIFO RTL design
- `code/lib/models/` - Python reference model
- `code/tb/fifo/` - Testbench, coverage, mutations, and documentation

## Running the Tests

Run `cd code/tb/fifo && make` from the project root.
