
from transaction import FifoTransaction

tx = FifoTransaction()

for i in range(10):
    tx.randomize()
    print(f"Transaction {i}: {tx.display()}")
