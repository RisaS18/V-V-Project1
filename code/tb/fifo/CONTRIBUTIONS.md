# Contributions — <team name> · <track>

> This file and the git history are cross-checked against each other, and
> against every member's confidential peer eval. Where the three disagree, the
> conversation happens *before* the Professionalism row is scored — so make
> them agree. A file written the night of M4 will not survive that check, and
> the way it fails is by being vague.

**Members:** <Risa Suzuki ri710407
**Repo:** <URL>
**Track:** RV32I core / AXI-Lite subsystem / secure_gate
**Last updated:** <11.14.2026> · **through milestone:** M__

---

## How to read this file

Each milestone section lists what each member owned, with the commits, files, or
tags that show it. "Helped with the testbench" is not a contribution record.
"Wrote the constrained-random sequence and its coverage bins — `tb/seq_rw.py`,
commits `a1b2c3d`..`e4f5g6h`" is.

Work that is genuinely shared gets its own row and says how it was shared
(pairing, review, a split you can describe). Do not inflate, and do not
flatten real differences into a polite fiction — an honest record of an uneven
milestone reads far better than a uniform one nobody believes.

---

## M1 — <due Wk 11>

| Member | What they owned | Evidence (commits / files / PRs) | Approx. share |
|--------|-----------------|----------------------------------|--------------:|
| Risa Suzuk |   Developed the Cocotb driver, monitor, and scoreboard; implemented directed and randomized FIFO tests; created the reference-model checks; developed functional coverage; ran mutation testing; documented results and prepared the report.        |  test_fifo.py, transaction.py, fifo_coverage.py, coverage_convergence.txt, FINDINGS.md, vplan.md, REPORT.pdf  |  100%     
**Shared or paired work:**
This was completed individually.

**What slipped, and who picked it up:**
No work was delegated to teammates. The required analysis of two surviving mutants was not completed because all eight mutants in the released pool were detected, and the additional survivor-analysis step was skipped.

## Whole-project summary

One row per member, across all four milestones. This is the row a reader checks
first, so it must be consistent with the four sections above.

| Member | Principal contributions (all four milestones) | Overall share |
|--------|-----------------------------------------------|--------------:|
|   Risa Suzuki     |    Completed the FIFO verification environment, directed testing, constrained-random testing, functional coverage, mutation testing, and final report.   |    100%           |

**The three things this team did that we would each defend in an interview:**

1. Developed a layered Cocotb testbench with a driver, monitor, queue-based reference model, and cycle-by-cycle scoreboard.

2. Implemented directed and constrained-random testing, achieving 100% functional coverage by 200 randomized transactions.

3. Detected all eight mutants in the released mutation pool, achieving a mutation score of 100%.

## Non-code contributions

Real work that leaves a thin git trace — and is graded all the same. Cite the
artifact where one exists.

| Member | Contribution | Where it shows |
|--------|--------------|----------------|
| Risa Suzuki       | spec archaeology / vplan authorship / debugging sessions / demo prep / review | vplan.md, test_fifo.py, FINDINGS.md, REPORT.pdf|

## AI assistance

Consistent with the course policy and your `ctm` record: name where an assistant
was used on capstone work, and who verified the output. The verifier is a named
person, always.

| Where | Used for | Verified by | Where the verification shows |
|-------|----------|-------------|------------------------------|
| Testbench development| Assistance with Cocotb structure, driver/monitor/scoreboard implementation, and debugging | Risa Suzuki | Successful simulation: 1 test passed |
|Randomization and coverage | Assistance with pyvsc constraints and coverage-model development| RS | coverage_convergence.txt and simulation output|
|Mutation testing| Assistance interpreting mutant failures and documenting results| RS | FINDINGS.md|

---

## Attestation

- [ ] Every claim above can be traced to the repo history.
- [ ] This file was updated at each milestone, not reconstructed at the end.
- [ ] Every member has read this file and agrees it is accurate.
- [ ] Each member has separately submitted their **confidential individual peer
      eval** — teammates' main contributions, an equity judgment, one sentence
      of evidence each — outside this repo, by the M4 deadline.

