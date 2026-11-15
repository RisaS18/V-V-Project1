
import vsc


@vsc.covergroup
class FifoCoverage:
    def __init__(self):
        # Values supplied whenever the coverage model is sampled.
        self.with_sample(
            occupancy=vsc.uint8_t(),
            wr_en=vsc.bit_t(1),
            rd_en=vsc.bit_t(1)
        )

        # Cover every possible FIFO occupancy: 0 through 8.
        self.cp_occupancy = vsc.coverpoint(
            self.occupancy,
            bins={
                f"occupancy_{i}": vsc.bin(i)
                for i in range(9)
            }
        )

        # Cover write enable: disabled and enabled.
        self.cp_write = vsc.coverpoint(
            self.wr_en,
            bins={
                "write_disabled": vsc.bin(0),
                "write_enabled": vsc.bin(1)
            }
        )

        # Cover read enable: disabled and enabled.
        self.cp_read = vsc.coverpoint(
            self.rd_en,
            bins={
                "read_disabled": vsc.bin(0),
                "read_enabled": vsc.bin(1)
            }
        )

        # Group occupancy into empty, middle, and full.
        self.cp_boundary = vsc.coverpoint(
            self.occupancy,
            bins={
                "empty": vsc.bin(0),
                "middle": vsc.bin(1, 2, 3, 4, 5, 6, 7),
                "full": vsc.bin(8)
            }
        )

        # Cross occupancy category with read/write requests.
        self.cross_boundary_requests = vsc.cross([
            self.cp_boundary,
            self.cp_write,
            self.cp_read
        ])


if __name__ == "__main__":
    # Simple standalone test of the coverage model.
    coverage = FifoCoverage()

    coverage.sample(0, 1, 1)
    coverage.sample(4, 1, 1)
    coverage.sample(8, 1, 1)

    print("Coverage model test:")
    print("Overall coverage:", coverage.get_coverage(), "%")
    vsc.report_coverage(details=True)
