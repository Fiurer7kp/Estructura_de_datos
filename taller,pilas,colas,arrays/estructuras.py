"""
SebasBank — Data Structures Module
Author  : Sebastian
Subject : Data Structures — Queues · Stacks · Arrays

Contains the 3 core data structures used by the banking engine:
  - ProcessingQueue  (FIFO)
  - CompensationStack (LIFO)
  - AuditArray        (fixed-size circular buffer)
"""

from collections import deque
from datetime import datetime
import random


# ══════════════════════════════════════════════════════════════════
#  DATA STRUCTURE 1 — QUEUE (FIFO)
#  Purpose: Receive incoming transactions without losing any request.
#           If the server is busy, transactions wait here in order.
# ══════════════════════════════════════════════════════════════════
class ProcessingQueue:
    """FIFO queue for incoming banking transactions."""

    def __init__(self):
        self._queue: deque = deque()

    def enqueue(self, txn: dict) -> str:
        txn_id           = f"TXN-{random.randint(10000, 99999)}"
        txn["id"]        = txn_id
        txn["timestamp"] = datetime.now().strftime("%H:%M:%S")
        txn["status"]    = "PENDING"
        self._queue.append(txn)
        return txn_id

    def dequeue(self) -> dict | None:
        return self._queue.popleft() if not self.is_empty() else None

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def size(self) -> int:
        return len(self._queue)

    def peek_all(self) -> list:
        return list(self._queue)


# ══════════════════════════════════════════════════════════════════
#  DATA STRUCTURE 2 — STACK (LIFO)
#  Purpose: Track steps of a transfer so they can be undone
#           in reverse order (rollback) if any step fails.
#  Steps:   VALIDATE_FUNDS → DEBIT_SOURCE → CREDIT_DEST
# ══════════════════════════════════════════════════════════════════
class CompensationStack:
    """LIFO stack for transaction step compensation and rollback."""

    def __init__(self):
        self._stack: list     = []
        self._rollbacks: list = []

    def push(self, step: dict) -> None:
        step["exec_time"] = datetime.now().strftime("%H:%M:%S")
        self._stack.append(step)

    def pop(self) -> dict | None:
        if self.is_empty():
            return None
        step = self._stack.pop()
        step["rev_time"] = datetime.now().strftime("%H:%M:%S")
        self._rollbacks.append(step)
        return step

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def size(self) -> int:
        return len(self._stack)

    def peek_all(self) -> list:
        return list(reversed(self._stack))   # top first

    def get_rollbacks(self) -> list:
        return list(self._rollbacks)

    def clear(self) -> None:
        self._stack.clear()


# ══════════════════════════════════════════════════════════════════
#  DATA STRUCTURE 3 — FIXED-SIZE ARRAY (circular buffer)
#  Purpose: Store the last N failed transactions for audit.
#           Fixed size prevents unbounded memory growth.
# ══════════════════════════════════════════════════════════════════
class AuditArray:
    """Fixed-capacity circular array for failed transaction auditing."""

    def __init__(self, capacity: int = 8):
        self._cap   = capacity
        self._data: list = [None] * capacity   # fixed array
        self._total = 0

    def record_failure(self, txn: dict) -> None:
        txn["fail_time"] = datetime.now().strftime("%H:%M:%S")
        self._data[self._total % self._cap] = txn
        self._total += 1

    def get_failures(self) -> list:
        if self._total == 0:
            return []
        if self._total <= self._cap:
            return [d for d in self._data if d is not None]
        start = self._total % self._cap
        order = self._data[start:] + self._data[:start]
        return [d for d in order if d is not None]

    def total_failures(self) -> int:
        return self._total

    def capacity(self) -> int:
        return self._cap
