"""STUDENT STARTER -- Week 4 FIFO testbench.

Build a driver / monitor / scoreboard testbench around the FWFT FIFO. Use the
golden model (models.fifo_model.FifoModel) as your scoreboard and check count,
full, empty, and rd_data *every* cycle. Hit the corners: fill to full, drain to
empty, write-while-full (dropped), read-while-empty (ignored), simultaneous
read+write, and pointer wrap.

Run:            make                # (or make SIM=icarus)
Score:          cd code && just mutate fifo        # found/total (released pool)

Right now this only does three writes and one weak check -- raise the found/total.
"""
import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from models.fifo_model import FifoModel
from collections import Counter
from transaction import FifoTransaction
from fifo_coverage import FifoCoverage
import vsc

WIDTH = 8
DEPTH = 8
MASK = (1 << WIDTH) - 1

class FifoDriver:
    def __init__(self, dut):
        self.dut = dut

    async def drive(self, wr_en, rd_en, wr_data):
        await FallingEdge(self.dut.clk)
        self.dut.wr_en.value = wr_en
        self.dut.rd_en.value = rd_en
        self.dut.wr_data.value = wr_data & MASK


class FifoMonitor:
    def __init__(self, dut):
        self.dut = dut

    async def sample(self):
        await RisingEdge(self.dut.clk)
        await Timer(1, units="ns")

        empty = int(self.dut.empty.value)

        return {
            "count": int(self.dut.count.value),
            "full": int(self.dut.full.value),
            "empty": empty,
            "rd_data": int(self.dut.rd_data.value) if not empty else None,
        }


class FifoScoreboard:
    def __init__(self, width=WIDTH, depth=DEPTH):
        self.model = FifoModel(width=width, depth=depth)

    def check(self, driven_wr, driven_rd, driven_data, sampled, rst_n=1):
        # Reset is synchronous and active-low.
        if not rst_n:
            self.model.reset()
        else:
            self.model.step(driven_wr, driven_data, driven_rd)

        expected_count = self.model.count
        expected_full = int(self.model.full)
        expected_empty = int(self.model.empty)
        expected_head = self.model.head

        assert sampled["count"] == expected_count, (
            f"Count mismatch: DUT={sampled['count']}, "
            f"expected={expected_count}"
        )

        assert sampled["full"] == expected_full, (
            f"Full mismatch: DUT={sampled['full']}, "
            f"expected={expected_full}"
        )

        assert sampled["empty"] == expected_empty, (
            f"Empty mismatch: DUT={sampled['empty']}, "
            f"expected={expected_empty}"
        )

        if not expected_empty:
            assert sampled["rd_data"] == expected_head, (
                f"rd_data mismatch: DUT={sampled['rd_data']}, "
                f"expected={expected_head}"
            )


@cocotb.test()
async def test_fifo(dut):
   
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    driver = FifoDriver(dut)
    monitor = FifoMonitor(dut)
    scoreboard = FifoScoreboard()

    coverage = Counter()
    pyvsc_cov = FifoCoverage()
    cycle_num = 0

    dut.wr_en.value = 0
    dut.rd_en.value = 0
    dut.wr_data.value = 0
    dut.rst_n.value = 0

    
    async def step_cycle(wr_en=0, rd_en=0, wr_data=0, rst_n=1):
        nonlocal cycle_num
        cycle_num += 1

        # Drive inputs before the rising clock edge.
        await driver.drive(wr_en, rd_en, wr_data)
        dut.rst_n.value = rst_n

        # Save occupancy BEFORE the clock edge updates the model.
        pre_count = scoreboard.model.count

        # Sample DUT outputs after the rising edge.
        sampled = await monitor.sample()

        # Update the reference model and compare every output.
        scoreboard.check(
            wr_en,
            rd_en,
            wr_data,
            sampled,
            rst_n=rst_n,
        )

        # Record coverage.
        coverage[("occupancy", sampled["count"])] += 1
        coverage[("flags", sampled["full"], sampled["empty"])] += 1

        if rst_n:
            pyvsc_cov.sample(
                pre_count,
                int(wr_en),
                int(rd_en)
            )  
            # Record requested operations.
            coverage[("request", wr_en, rd_en)] += 1
            coverage[("pre_occupancy", pre_count)] += 1

            # Determine accepted operations using PRE-edge occupancy.
            accepted_wr = bool(wr_en and pre_count < DEPTH)
            accepted_rd = bool(rd_en and pre_count > 0)

            if accepted_wr:
                coverage["accepted_write"] += 1

            if accepted_rd:
                coverage["accepted_read"] += 1

            # Check attempts made at the FIFO boundaries.
            if wr_en and pre_count == DEPTH:
                coverage["write_while_full"] += 1

            if rd_en and pre_count == 0:
                coverage["read_while_empty"] += 1

            # Track simultaneous requests at different occupancies.
            if wr_en and rd_en:
                if pre_count == 0:
                    coverage["simultaneous_at_empty"] += 1
                elif pre_count == DEPTH:
                    coverage["simultaneous_at_full"] += 1
                else:
                    coverage["simultaneous_mid_occupancy"] += 1

        return sampled


    for _ in range(3):
        await step_cycle(rst_n=0)

    await step_cycle(rst_n=1)

    await step_cycle(rd_en=1) 
    coverage["empty_read_test"] += 1

    await step_cycle(wr_en=1, rd_en=1, wr_data=0xA1)
    # coverage["simultaneous_at_empty"] += 1

    for i in range(DEPTH - 1):
        await step_cycle(wr_en=1, wr_data=(0x10 + i))

    coverage["fill_to_full"] += 1

    await step_cycle(wr_en=1, wr_data=0xF0)
    coverage["write_while_full_directed"] += 1



    await step_cycle(wr_en=1, rd_en=1, wr_data=0xDD)
    # coverage["simultaneous_at_full"] += 1

    for _ in range(DEPTH):
        await step_cycle(rd_en=1)

    coverage["drain_to_empty"] += 1

    await step_cycle(rd_en=1)
    coverage["empty_read_after_drain"] += 1

    await step_cycle(wr_en=1, wr_data=0x31)
    await step_cycle(wr_en=1, wr_data=0x32)
    await step_cycle(wr_en=1, rd_en=1, wr_data=0x33)
    await step_cycle(rd_en=1)
    await step_cycle(rd_en=1)
    # coverage["simultaneous_mid_occupancy"] += 1

    for round_num in range(3):
        for i in range(DEPTH):
            await step_cycle(
                wr_en=1,
                wr_data=((round_num * DEPTH + i) & MASK),
            )

        for _ in range(DEPTH):
            await step_cycle(rd_en=1)

    coverage["pointer_wrap_sequences"] += 1

    tx = FifoTransaction()

    random_cov = FifoCoverage()

    dut._log.info(
        "Coverage before random testing: %.2f%%",
        pyvsc_cov.get_coverage()
    )

    with open("coverage_convergence.txt", "w") as f:
        f.write("FIFO Coverage Convergence\n")
        f.write("=========================\n")
    for i in range(500):
        tx.randomize()

        wr = int(tx.wr_en)
        rd = int(tx.rd_en)
        data = int(tx.wr_data)

        dut._log.info(
            "Random transaction %d: wr=%d rd=%d data=0x%02X",
            i, wr, rd, data
        )
        pre_count = scoreboard.model.count

        await step_cycle(
            wr_en=wr,
            rd_en=rd,
            wr_data=data
        )

        random_cov.sample(pre_count, wr, rd)

        if (i + 1) % 50 == 0:
            coverage_value = random_cov.get_coverage()

            message = (
                f"After {i + 1} random transactions: "
                f"{coverage_value:.2f}%"
            )

            dut._log.info(message)

            with open("coverage_convergence.txt", "a") as f:
                f.write(message + "\n")

    dut._log.info(
    "Overall pyvsc functional coverage: %.2f%%",
    pyvsc_cov.get_coverage()
    )

    vsc.report_coverage(details=True)
    dut._log.info("FIFO test completed after %d cycles", cycle_num)
    dut._log.info("Functional coverage counters:")
    for key, value in sorted(coverage.items(), key=lambda item: str(item[0])):
        dut._log.info("  %s : %s", key, value)