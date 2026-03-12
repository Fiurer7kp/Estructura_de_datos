"""
╔══════════════════════════════════════════════════════════════════╗
║   SebasBank — Banking Transaction Engine                         ║
║   Author  : Sebastian                                            ║
║   Subject : Data Structures — Queues · Stacks · Arrays          ║
║   Run     : python main.py                                       ║
╚══════════════════════════════════════════════════════════════════╝

Project structure:
  main.py        ← entry point (this file) — starts the app
  motor.py       ← banking engine logic
  estructuras.py ← Queue, Stack, Array data structures
  paneles.py     ← all GUI panels and widgets
  tema.py        ← colors and fonts
"""

import tkinter as tk
from tkinter import messagebox
from motor import BankingEngine
from paneles import build_header, LeftPanel, RightPanel


# ══════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════
class SebasBankApp(tk.Tk):
    """Main window — wires together the engine and UI panels."""

    def __init__(self):
        super().__init__()
        self.engine = BankingEngine()
        self.title("SebasBank — Motor de Transacciones Bancarias")
        self.configure(bg="#0e0a00")
        self.geometry("1200x760")
        self.minsize(1000, 650)

        # Build UI
        build_header(self)
        body = tk.Frame(self, bg="#0e0a00")
        body.pack(fill="both", expand=True)

        self.left  = LeftPanel(body, self.engine,
                               on_enqueue      = self._on_enqueue,
                               on_process      = self._on_process,
                               on_process_all  = self._on_process_all)

        self.right = RightPanel(body, self.engine)

        # Start refresh loop
        self._refresh()

    # ── refresh cycle (every second) ─────────────────────────
    def _refresh(self):
        self.left.refresh()
        self.right.refresh_tab()
        self.after(1000, self._refresh)

    # ── user actions ─────────────────────────────────────────
    def _on_enqueue(self):
        """Validate inputs and enqueue a new transaction."""
        data = self.left.get_form_data()

        if data["amount"] <= 0:
            messagebox.showerror("Error de entrada",
                                 "Por favor ingresa un monto válido mayor a cero.")
            return

        if data["type"] == "TRANSFERENCIA":
            if data["src"] == data["dst"]:
                messagebox.showerror("Error de entrada",
                                     "La cuenta de origen y destino no pueden ser iguales.")
                return
            self.engine.request("TRANSFERENCIA",
                                origen=data["src"],
                                destino=data["dst"],
                                monto=data["amount"])
        else:
            self.engine.request(data["type"],
                                cuenta=data["account"],
                                monto=data["amount"])

        self.left.clear_amount()
        self.right.show_log()

    def _on_process(self):
        """Process the next transaction from the queue."""
        res = self.engine.process_next()
        self.right.show_log()
        if not res["ok"] and res["msg"] == "Cola vacía.":
            messagebox.showwarning("Cola vacía",
                                   "No hay transacciones pendientes en la cola.")

    def _on_process_all(self):
        """Process every transaction currently in the queue."""
        if self.engine.queue.is_empty():
            messagebox.showinfo("Cola vacía",
                                "No hay transacciones en la cola de procesamiento.")
            return
        total = self.engine.queue.size()
        for _ in range(total):
            if self.engine.queue.is_empty():
                break
            self.engine.process_next()
        self.right.show_log()
        messagebox.showinfo("Procesamiento completo",
                            f"Se procesaron {total} transacción(es) exitosamente.")


# ══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = SebasBankApp()
    app.mainloop()
