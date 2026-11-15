# FIFO Mutation Testing Findings

## Released Mutation Pool

| Mutant | Description | Result |
|---|---|---|
| full_offbyone | Full asserts one entry too early | KILLED |
| empty_offbyone | Empty asserts at count 1 | KILLED |
| ignore_full | Writes accepted while full | KILLED |
| ignore_empty | Reads accepted while empty | KILLED |
| count_wr_dec | Write-only cycle decrements count | KILLED |
| rd_data_wrptr | Reads from write pointer | KILLED |
| mem_corrupt | Stored data corrupted on write | KILLED |
| wrptr_wrap_early | Write pointer wraps one slot early | KILLED |

Current result: 8/8 mutants killed (100%).

## Mutation Score

- Mutants detected: 8
- Total released mutants: 8
- Mutation score: 100%

All eight released mutants were detected by the Cocotb testbench.
The scoreboard identified incorrect FIFO status, count, and data behavior.