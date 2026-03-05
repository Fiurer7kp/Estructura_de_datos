"""
SebasBank — Banking Engine Module
Author  : Sebastian
Subject : Data Structures — Queues · Stacks · Arrays

Orchestrates the 3 data structures to process banking transactions:
  - Transfers  (uses Stack for step tracking + rollback)
  - Withdrawals
  - Deposits
"""

import random
from datetime import datetime
from estructuras import ProcessingQueue, CompensationStack, AuditArray


# ══════════════════════════════════════════════════════════════════
#  BANKING ENGINE — Orchestrates the 3 data structures
# ══════════════════════════════════════════════════════════════════
FAILURE_RATE = 0.25   # 25% simulated random failure rate

class BankingEngine:
    """Core engine that wires together Queue, Stack and Array."""

    def __init__(self):
        self.queue = ProcessingQueue()
        self.stack = CompensationStack()
        self.audit = AuditArray(capacity=8)
        self.accounts: dict[str, float] = {
            "4001-AAAA": 5_000.00,
            "4001-BBBB": 12_000.00,
            "4001-CCCC":    800.00,
            "4001-DDDD": 30_000.00,
        }
        self.event_log: list[tuple[str, str]] = []   # (message, color_tag)

    # ── internal log helper ───────────────────────────────────
    def _log(self, msg: str, tag: str = "info") -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.event_log.append((f"[{timestamp}]  {msg}", tag))

    # ── public: request a new transaction (enqueue) ───────────
    def request(self, txn_type: str, **kwargs) -> str:
        txn = {"tipo": txn_type, **kwargs}
        tid = self.queue.enqueue(txn)
        self._log(f"ENCOLADA  {tid}  →  {txn_type}", "queue")
        return tid

    # ── public: process next transaction from queue ───────────
    def process_next(self) -> dict:
        if self.queue.is_empty():
            return {"ok": False, "msg": "Cola vacía."}
        txn = self.queue.dequeue()
        self._log(f"PROCESANDO  {txn['id']}  —  {txn['tipo']}", "info")
        if txn["tipo"] == "TRANSFERENCIA":
            return self._transfer(txn)
        elif txn["tipo"] == "RETIRO":
            return self._withdrawal(txn)
        elif txn["tipo"] == "DEPOSITO":
            return self._deposit(txn)
        return {"ok": False, "msg": "Tipo de transacción desconocido."}

    # ── transfer: uses the stack for step tracking ────────────
    def _transfer(self, txn: dict) -> dict:
        src, dst, amount = txn["origen"], txn["destino"], txn["monto"]
        steps = [
            {"nombre": "VALIDAR_FONDOS",    "desc": f"Verificar saldo ≥ ${amount:,.2f}"},
            {"nombre": "DESCONTAR_ORIGEN",  "desc": f"Descontar ${amount:,.2f} de {src}"},
            {"nombre": "ACREDITAR_DESTINO", "desc": f"Acreditar ${amount:,.2f} en {dst}"},
        ]
        for i, step in enumerate(steps):
            # simulate random failure after first step
            if i > 0 and random.random() < FAILURE_RATE:
                self._log(f"  ✗ FALLO en {step['nombre']}", "failure")
                return self._rollback(txn)
            # validate sufficient funds
            if step["nombre"] == "VALIDAR_FONDOS" and self.accounts.get(src, 0) < amount:
                self._log(f"  ✗ Saldo insuficiente en {src}", "failure")
                return self._rollback(txn)
            # push step onto stack
            self.stack.push(step)
            self._log(f"  ✔ {step['nombre']}", "step")
            # apply real account changes
            if step["nombre"] == "DESCONTAR_ORIGEN":
                self.accounts[src] -= amount
            elif step["nombre"] == "ACREDITAR_DESTINO":
                self.accounts[dst] = self.accounts.get(dst, 0) + amount
        self.stack.clear()
        self._log(f"  ✅ Transferencia {txn['id']} COMPLETADA", "ok")
        return {"ok": True, "msg": "Transferencia completada exitosamente.", "txn": txn}

    # ── withdrawal ────────────────────────────────────────────
    def _withdrawal(self, txn: dict) -> dict:
        account, amount = txn["cuenta"], txn["monto"]
        if self.accounts.get(account, 0) < amount:
            self.audit.record_failure({**txn, "razon": "Saldo insuficiente"})
            self._log(f"  ✗ Saldo insuficiente — {txn['id']}", "failure")
            return {"ok": False, "msg": "Saldo insuficiente.", "txn": txn}
        self.accounts[account] -= amount
        self._log(f"  ✅ Retiro {txn['id']} COMPLETADO", "ok")
        return {"ok": True, "msg": f"Retiro de ${amount:,.2f} exitoso.", "txn": txn}

    # ── deposit ───────────────────────────────────────────────
    def _deposit(self, txn: dict) -> dict:
        account, amount = txn["cuenta"], txn["monto"]
        self.accounts[account] = self.accounts.get(account, 0) + amount
        self._log(f"  ✅ Depósito {txn['id']} COMPLETADO", "ok")
        return {"ok": True, "msg": f"Depósito de ${amount:,.2f} exitoso.", "txn": txn}

    # ── rollback: pop all stack steps in reverse order ────────
    def _rollback(self, txn: dict) -> dict:
        self._log("  ⟳ ROLLBACK iniciado...", "rollback")
        while not self.stack.is_empty():
            step = self.stack.pop()
            self._log(f"    ↩ Revertido: {step['nombre']}", "rollback")
            if step["nombre"] == "DESCONTAR_ORIGEN":
                self.accounts[txn["origen"]] += txn["monto"]
            elif step["nombre"] == "ACREDITAR_DESTINO":
                self.accounts[txn["destino"]] -= txn["monto"]
        self.audit.record_failure({**txn, "razon": "Fallo en procesamiento"})
        self._log(f"  ✗ {txn['id']} REVERTIDA — registrada en auditoría", "failure")
        return {"ok": False, "msg": "Transacción fallida. Rollback ejecutado.", "txn": txn}
