import vsc


@vsc.randobj
class FifoTransaction:
    def __init__(self):
        self.wr_en = vsc.rand_bit_t()
        self.rd_en = vsc.rand_bit_t()
        self.wr_data = vsc.rand_uint8_t()

    @vsc.constraint
    def request_distribution(self):
        # Give enabled requests a higher probability.
        vsc.dist(self.wr_en, [
            vsc.weight(0, 2),
            vsc.weight(1, 3)
        ])

        vsc.dist(self.rd_en, [
            vsc.weight(0, 2),
            vsc.weight(1, 3)
        ])

    def display(self):
        return (
            f"wr_en={int(self.wr_en)}, "
            f"rd_en={int(self.rd_en)}, "
            f"wr_data=0x{int(self.wr_data):02X}"
        )