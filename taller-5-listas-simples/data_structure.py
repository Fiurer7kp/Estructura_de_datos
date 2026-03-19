# ============================================================
#  MODULE: data_structure.py
#  Contains: Node class and SimpleLinkedList class
#  All logic is pure Python — no external dependencies
# ============================================================

import time as _time


class Node:
    """
    Represents a single task in the linked list.
    Each node holds data and a pointer to the next node.
    """
    def __init__(self, id_: int, task: str,
                 priority: str = "Media",
                 estimated_time: str = ""):
        self.id             = id_
        self.task           = task
        self.priority       = priority        # "Alta" | "Media" | "Baja"
        self.estimated_time = estimated_time  # e.g. "2 horas"
        self.done           = False
        self.created_at     = _time.time()    # Unix timestamp — for elapsed time
        self.next           = None            # ← POINTER to next node


class SimpleLinkedList:
    """
    Singly linked list of task nodes.
    All traversal is done manually via the .next pointer.
    """

    def __init__(self):
        self.head     = None   # pointer to the first node (HEAD)
        self.size     = 0
        self._next_id = 1

    # ── Insert at the end ─────────────────────────────────────
    def insert(self, task: str, priority: str = "Media",
               estimated_time: str = "") -> Node:
        new_node = Node(self._next_id, task, priority, estimated_time)
        self._next_id += 1

        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

        self.size += 1
        return new_node

    # ── Delete by ID ──────────────────────────────────────────
    def delete(self, id_: int) -> bool:
        if self.head is None:
            return False
        if self.head.id == id_:
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next is not None:
            if current.next.id == id_:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    # ── Mark as complete ──────────────────────────────────────
    def complete(self, id_: int) -> bool:
        current = self.head
        while current is not None:
            if current.id == id_:
                current.done = True
                return True
            current = current.next
        return False

    # ── Delete all completed nodes ────────────────────────────
    def clear_completed(self) -> int:
        removed = 0
        while self.head and self.head.done:
            self.head = self.head.next
            self.size -= 1
            removed += 1
        current = self.head
        while current and current.next:
            if current.next.done:
                current.next = current.next.next
                self.size -= 1
                removed += 1
            else:
                current = current.next
        return removed

    # ── Traverse — returns list of nodes ──────────────────────
    def traverse(self) -> list:
        nodes, current = [], self.head
        while current is not None:
            nodes.append(current)
            current = current.next
        return nodes

    # ── Stats ─────────────────────────────────────────────────
    @property
    def total_done(self) -> int:
        return sum(1 for n in self.traverse() if n.done)

    @property
    def total_pending(self) -> int:
        return self.size - self.total_done
