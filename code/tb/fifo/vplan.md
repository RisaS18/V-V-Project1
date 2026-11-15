# Verification plan — <DUT>

**Author: Risa Suzuki** **Spec version:fifo.md** **Date:11/14/2026**

> A vplan is an argument that "done" is definable before you write tests. Every
> row here should be something you could defend in a signoff meeting. Rows you
> cannot defend are the honest content of the Risk section, not omissions.

## 1. Scope

**In scope:** <Verify FIFO write and read operations, Verify FIFO data ordering using a reference queue, Verify occupancy count, full, and empty status, >
**Out of scope:** <Physical timing analysis and hardware implementation, Synthesis and gate-level verification, Internal memory contents when the FIFO is empty>
**Assumptions about the environment:** <The FIFO uses a synchronous clock, Reset is active-low, Transactions are sampled and evaluated on the rising edge of clk>

## 2. Feature list

One row per behavior the spec requires. `Req` cites a line or section of the
spec — if you cannot cite one, that is a spec gap and it belongs in section 5.

| ID | Feature | Req | Priority | How it is verified |
|----|---------|-----|----------|--------------------|
| F1 | Active-low reset|Reset behavior| H | directed |
| F2 | Write operation | Write handshake | H | Directed + CRV |
| F3 | Read operation | Read handshake | H | Directed + CRV |
| F4 | FIFO data ordering | Ordering guarantee | H | Scoreboard |
| F5 | Occupancy count | Count behavior | H | Monitor + scoreboard |
| F6 | Full flag | Full condition | H | Directed + CRV |
| F7 | Empty flag | Empty condition | H | Directed + CRV |
| F8 | Pointer wraparound | Pointer behavior | H | Directed + CRV |
| F9 | Simultaneous read/write | Concurrent operations | H | Directed + CRV |
| F10 | FWFT output | FWFT behavior | H | Directed + scoreboard |
| F11 | Write while full | Overflow handling | H | Directed + CRV |
| F12 | Read while empty | Underflow handling | H | Directed + CRV |

## 3. Coverage model

Coverpoints and their bins. A cross earns its place only if the interaction is
where a bug would hide — say which bug.

| ID | Coverpoint | Bins | Why these bins |
|----|-----------|------|----------------|
| C1 | FIFO occupancy | 0, 1, 2, 3, 4, 5, 6, 7, 8 | Covers every legal occupancy |
| C2 | Write enable | 0, 1 | Covers idle and write requests |
| C3 | Read enable | 0, 1 | Covers idle and read requests |
| C4 | Full flag | 0, 1 | Checks full and non-full states |
| C5 | Empty flag | 0, 1 | Checks empty and non-empty states |
| C6 | Accepted write | 0, 1 | Covers blocked and accepted writes |
| C7 | Accepted read | 0, 1 | Covers blocked and accepted reads |
| C8 | Simultaneous request | 0, 1 | Covers read/write concurrency |
| C9 | Pointer wraparound | read wrap, write wrap | Checks circular buffer behavior |
| C10 | Reset | reset asserted, reset released | Covers reset transitions |

**Crosses**

| ID | Cross | The interaction it is aimed at |
|----|-------|-------------------------------|
| X1 | Occupancy × write enable | Writes at empty, middle, and full |
| X2 | Occupancy × read enable | Reads at empty, middle, and full |
| X3 | Occupancy × simultaneous read/write | Boundary concurrency behavior |
| X4 | Full × write enable × read enable | Write blocking while full |
| X5 | Empty × write enable × read enable | Read blocking while empty |
| X6 | Reset × write/read enables | Reset interaction with requests |

**Illegal / ignore bins:** <Occupancy values greater than DEPTH or less than zero are illegal., Do not compare rd_data when empty because the output data is not guaranteed to be valid.>

## 4. Test matrix

Every feature maps to at least one test; every test traces back to a feature.
An untraceable test is a test nobody can defend.

| Test | Features | Kind | Pass criterion |
|------|----------|------|----------------|
| T1 Reset test | F1 | Directed | Count=0 and empty=1 after reset |
| T2 Basic write/read | F2, F3, F4 | Directed | Data is read in write order |
| T3 Fill FIFO | F2, F5, F6 | Directed | Count reaches DEPTH and full asserts |
| T4 Empty FIFO | F3, F5, F7 | Directed | Count reaches 0 and empty asserts |
| T5 Overflow attempt | F11 | Directed | Extra write is rejected |
| T6 Underflow attempt | F12 | Directed | Extra read is rejected |
| T7 Pointer wraparound | F8 | Directed | Data integrity is preserved after wrap |
| T8 Simultaneous read/write | F9 | Directed + CRV | Count and data ordering remain correct |
| T9 FWFT test | F10 | Directed | Head data is visible without read enable |
| T10 Random regression | F1-F12 | CRV | Scoreboard has no mismatches |
| T11 Reset during activity | F1, F2, F3 | Directed | FIFO returns to reset state |

## 5. Risk and spec ambiguity

| # | Ambiguity or risk | Where in the spec | How I resolved it | Residual |
|---|-------------------|-------------------|-------------------|----------|
| 1 | Behavior of simultaneous read/write at empty | To be checked | Analyze written spec | TBD |
| 2 | Behavior of simultaneous read/write at full | To be checked | Analyze written spec | TBD |
| 3 | Output data when empty | To be checked | Avoid checking invalid data | TBD |
| 4 | Whether memory is cleared by reset | To be checked | RTL resets pointers/count only | TBD |
| 5 | Overflow and underflow behavior | To be checked | Verify against written spec | TBD |

## 6. Closure criteria

State the numbers *before* you start, so closure is a measurement and not a
negotiation.

- Functional coverage target: **100%** of the model in section 3
- Mutation target: **90%_** on the hidden pool
- Assertions: every property paired with a passing `cover` (no vacuous passes)
- What I will report as **not verified**:
Physical timing and electrical characteristics, Gate-level implementation behavior, Unspecified FIFO behavior not defined in the written specification.