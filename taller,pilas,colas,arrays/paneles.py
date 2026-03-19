"""
SebasBank — UI Panels Module
Author  : Sebastian

Contains reusable UI components:
  - build_header()       → top bar with logo + author badge
  - LeftPanel            → stats, balances, transaction form
  - RightPanel           → tabbed view (log, queue, stack, audit)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tema import (BG, BG2, BG3, BORDER, GOLD, GOLD2, ORANGE, RED,
                  GREEN, TEAL, PURPLE, TEXT, MUTED, WHITE,
                  FONT_MONO, FONT_MONO_SM)


# ══════════════════════════════════════════════════════════════════
#  HEADER BAR
# ══════════════════════════════════════════════════════════════════
def build_header(parent: tk.Widget) -> None:
    """Renders the top header bar with logo, subtitle and author badge."""
    hdr = tk.Frame(parent, bg=BG2, height=54)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)

    # Logo
    tk.Label(hdr, text="Sebas", font=("Courier New", 17, "bold"),
             bg=BG2, fg=WHITE).pack(side="left", padx=(20, 0), pady=8)
    tk.Label(hdr, text="Bank", font=("Courier New", 17, "bold"),
             bg=BG2, fg=GOLD).pack(side="left", pady=8)
    tk.Label(hdr,
             text="  ·  Motor de Transacciones Bancarias  ·  Estructuras de Datos",
             font=("Segoe UI", 9), bg=BG2, fg=MUTED).pack(side="left", pady=8)

    # Author badge (right side)
    badge = tk.Frame(hdr, bg=BG3, padx=10, pady=4)
    badge.pack(side="right", padx=(0, 14), pady=8)
    tk.Label(badge, text="✦  Elaborado por: ",
             font=("Courier New", 8), bg=BG3, fg=MUTED).pack(side="left")
    tk.Label(badge, text="Sebastian",
             font=("Courier New", 8, "bold"), bg=BG3, fg=GOLD).pack(side="left")

    # Live indicator
    dot_f = tk.Frame(hdr, bg=BG2)
    dot_f.pack(side="right", padx=16)
    dot = tk.Canvas(dot_f, width=10, height=10, bg=BG2, highlightthickness=0)
    dot.pack(side="left", padx=(0, 6))
    dot.create_oval(1, 1, 9, 9, fill=GREEN, outline="")
    tk.Label(dot_f, text="SISTEMA ACTIVO",
             font=("Courier New", 8), bg=BG2, fg=GREEN).pack(side="left")


# ══════════════════════════════════════════════════════════════════
#  LEFT PANEL — Stats + Balances + Transaction Form
# ══════════════════════════════════════════════════════════════════
class LeftPanel:
    """Left sidebar: engine stats, account balances and transaction form."""

    def __init__(self, parent: tk.Widget, engine, on_enqueue, on_process, on_process_all):
        self._engine       = engine
        self._on_enqueue   = on_enqueue
        self._on_process   = on_process
        self._on_process_all = on_process_all

        self._frame = tk.Frame(parent, bg=BG, width=375)
        self._frame.pack(side="left", fill="y")
        self._frame.pack_propagate(False)

        self._build_stats()
        self._build_balances()
        self._build_form()
        self._build_footer()

    # ── stat cards row ────────────────────────────────────────
    def _build_stats(self):
        wrap = tk.Frame(self._frame, bg=BG2, pady=12)
        wrap.pack(fill="x", padx=12, pady=(12, 6))
        tk.Label(wrap, text="ESTADO DEL MOTOR",
                 font=("Courier New", 8), bg=BG2, fg=MUTED).pack(anchor="w", padx=12)
        row = tk.Frame(wrap, bg=BG2)
        row.pack(fill="x", padx=8, pady=(6, 0))
        self.stat_queue = _stat_card(row, "COLA",   TEAL)
        self.stat_stack = _stat_card(row, "PILA",   PURPLE)
        self.stat_fails = _stat_card(row, "FALLOS", RED)

    # ── account balance rows ──────────────────────────────────
    def _build_balances(self):
        wrap = tk.Frame(self._frame, bg=BG2)
        wrap.pack(fill="x", padx=12, pady=6)
        tk.Label(wrap, text="SALDOS DE CUENTAS",
                 font=("Courier New", 8), bg=BG2, fg=MUTED).pack(anchor="w", padx=12, pady=(10, 4))
        self.balance_labels: dict[str, tk.Label] = {}
        for acct in self._engine.accounts:
            row = tk.Frame(wrap, bg=BG3)
            row.pack(fill="x", padx=10, pady=2)
            tk.Label(row, text=acct, font=FONT_MONO_SM,
                     bg=BG3, fg=MUTED, width=14, anchor="w").pack(side="left", padx=8, pady=6)
            lbl = tk.Label(row, text="$0.00",
                           font=("Courier New", 10, "bold"),
                           bg=BG3, fg=GREEN, anchor="e")
            lbl.pack(side="right", padx=10)
            self.balance_labels[acct] = lbl

    # ── transaction form ──────────────────────────────────────
    def _build_form(self):
        wrap = tk.Frame(self._frame, bg=BG2)
        wrap.pack(fill="x", padx=12, pady=6)
        tk.Label(wrap, text="NUEVA TRANSACCIÓN",
                 font=("Courier New", 8), bg=BG2, fg=MUTED).pack(anchor="w", padx=12, pady=(10, 6))

        # Type radio buttons
        type_row = tk.Frame(wrap, bg=BG2)
        type_row.pack(fill="x", padx=10, pady=(0, 8))
        self.txn_type = tk.StringVar(value="TRANSFERENCIA")
        for label, value in [("Transferencia", "TRANSFERENCIA"),
                              ("Retiro",        "RETIRO"),
                              ("Depósito",      "DEPOSITO")]:
            tk.Radiobutton(type_row, text=label,
                           variable=self.txn_type, value=value,
                           font=("Courier New", 8), bg=BG2, fg=TEXT,
                           selectcolor=BG3, activebackground=BG2,
                           activeforeground=GOLD,
                           command=self._on_type_change).pack(side="left", padx=6)

        # Dynamic account field area
        self._fields_frame = tk.Frame(wrap, bg=BG2)
        self._fields_frame.pack(fill="x", padx=10)
        self._build_transfer_fields()

        # Amount entry
        amt_row = tk.Frame(wrap, bg=BG2)
        amt_row.pack(fill="x", padx=10, pady=8)
        tk.Label(amt_row, text="MONTO  $",
                 font=("Courier New", 8), bg=BG2, fg=MUTED).pack(side="left")
        self.amount_var = tk.StringVar()
        tk.Entry(amt_row, textvariable=self.amount_var,
                 font=FONT_MONO, bg=BG3, fg=GOLD2,
                 insertbackground=GOLD, relief="flat",
                 highlightthickness=1, highlightcolor=GOLD,
                 highlightbackground=BORDER, width=16).pack(side="left", padx=(6, 0))

        # Action buttons
        btn_row = tk.Frame(wrap, bg=BG2)
        btn_row.pack(fill="x", padx=10, pady=(4, 14))
        _btn(btn_row, "+ ENCOLAR",  GOLD,   self._on_enqueue).pack(side="left", padx=(0, 6))
        _btn(btn_row, "▶ PROCESAR", GREEN,  self._on_process).pack(side="left", padx=(0, 6))
        _btn(btn_row, "⚡ TODO",    ORANGE, self._on_process_all).pack(side="left")

    # ── dynamic fields ────────────────────────────────────────
    def _build_transfer_fields(self):
        for w in self._fields_frame.winfo_children():
            w.destroy()
        accounts = list(self._engine.accounts.keys())
        for row_label, attr in [("ORIGEN ", "_src_combo"),
                                 ("DESTINO", "_dst_combo")]:
            r = tk.Frame(self._fields_frame, bg=BG2)
            r.pack(fill="x", pady=2)
            tk.Label(r, text=row_label, font=("Courier New", 8),
                     bg=BG2, fg=MUTED, width=8, anchor="w").pack(side="left")
            combo = ttk.Combobox(r, values=accounts, font=FONT_MONO_SM,
                                 state="readonly", width=14)
            combo.current(0 if attr == "_src_combo" else 1)
            combo.pack(side="left")
            setattr(self, attr, combo)

    def _build_account_field(self):
        for w in self._fields_frame.winfo_children():
            w.destroy()
        accounts = list(self._engine.accounts.keys())
        r = tk.Frame(self._fields_frame, bg=BG2)
        r.pack(fill="x", pady=2)
        tk.Label(r, text="CUENTA ", font=("Courier New", 8),
                 bg=BG2, fg=MUTED, width=8, anchor="w").pack(side="left")
        self._acct_combo = ttk.Combobox(r, values=accounts, font=FONT_MONO_SM,
                                        state="readonly", width=14)
        self._acct_combo.current(0)
        self._acct_combo.pack(side="left")

    def _on_type_change(self):
        if self.txn_type.get() == "TRANSFERENCIA":
            self._build_transfer_fields()
        else:
            self._build_account_field()

    # ── footer ────────────────────────────────────────────────
    def _build_footer(self):
        footer = tk.Frame(self._frame, bg=BG)
        footer.pack(fill="x", padx=12, side="bottom", pady=8)
        tk.Label(footer,
                 text="SebasBank v1.0  ·  © 2026 Sebastian  ·  Estructuras de Datos",
                 font=("Courier New", 7), bg=BG, fg=BORDER).pack()

    # ── refresh (called every second by App) ─────────────────
    def refresh(self):
        self.stat_queue.config(text=str(self._engine.queue.size()))
        self.stat_stack.config(text=str(self._engine.stack.size()))
        self.stat_fails.config(text=str(self._engine.audit.total_failures()))
        for acct, lbl in self.balance_labels.items():
            lbl.config(text=f"${self._engine.accounts.get(acct, 0):,.2f}")

    # ── getters used by App when processing actions ───────────
    def get_form_data(self) -> dict:
        """Returns current form values as a dict."""
        t = self.txn_type.get()
        try:
            amount = float(self.amount_var.get().replace(",", ""))
        except ValueError:
            amount = 0
        data = {"type": t, "amount": amount}
        if t == "TRANSFERENCIA":
            data["src"] = self._src_combo.get()
            data["dst"] = self._dst_combo.get()
        else:
            data["account"] = self._acct_combo.get()
        return data

    def clear_amount(self):
        self.amount_var.set("")


# ══════════════════════════════════════════════════════════════════
#  RIGHT PANEL — Tabbed content area
# ══════════════════════════════════════════════════════════════════
class RightPanel:
    """Right area: tab bar + log / queue / stack / audit views."""

    def __init__(self, parent: tk.Widget, engine):
        self._engine = engine
        self._frame  = tk.Frame(parent, bg=BG)
        self._frame.pack(side="left", fill="both", expand=True)
        self._build_tabs()
        self._build_content()

    # ── tab radio buttons ─────────────────────────────────────
    def _build_tabs(self):
        tab_bar = tk.Frame(self._frame, bg=BG)
        tab_bar.pack(fill="x", padx=12, pady=(12, 0))
        self.tab_var = tk.StringVar(value="log")
        defs = [
            ("log",   "REGISTRO DE EVENTOS",  TEXT),
            ("cola",  "COLA  [FIFO]",         TEAL),
            ("pila",  "PILA  [LIFO]",         PURPLE),
            ("audit", "AUDITORÍA  [ARREGLO]", RED),
        ]
        for val, lbl, col in defs:
            tk.Radiobutton(tab_bar, text=lbl,
                           variable=self.tab_var, value=val,
                           command=self.refresh_tab,
                           font=("Courier New", 8, "bold"),
                           bg=BG, fg=col, selectcolor=BG2,
                           activebackground=BG, activeforeground=col,
                           indicatoron=False, relief="flat",
                           padx=12, pady=6, cursor="hand2",
                           highlightthickness=1,
                           highlightbackground=BORDER).pack(side="left", padx=3)

    # ── content frames ────────────────────────────────────────
    def _build_content(self):
        self._content = tk.Frame(self._frame, bg=BG2)
        self._content.pack(fill="both", expand=True, padx=12, pady=(6, 12))
        self._build_log_panel()
        self._build_queue_panel()
        self._build_stack_panel()
        self._build_audit_panel()
        # show log by default
        self._log_frame.pack(fill="both", expand=True)

    def _build_log_panel(self):
        self._log_frame = tk.Frame(self._content, bg=BG2)
        self._log_text  = tk.Text(self._log_frame,
                                   font=FONT_MONO_SM, bg=BG2, fg=TEXT,
                                   relief="flat", insertbackground=GOLD,
                                   state="disabled", wrap="word",
                                   padx=12, pady=8)
        self._log_text.tag_config("queue",   foreground=TEAL)
        self._log_text.tag_config("info",    foreground=TEXT)
        self._log_text.tag_config("step",    foreground=GREEN)
        self._log_text.tag_config("ok",      foreground=GREEN)
        self._log_text.tag_config("failure", foreground=RED)
        self._log_text.tag_config("rollback",foreground=ORANGE)
        sb = tk.Scrollbar(self._log_frame, command=self._log_text.yview,
                          bg=BG3, troughcolor=BG2)
        sb.pack(side="right", fill="y")
        self._log_text.config(yscrollcommand=sb.set)
        self._log_text.pack(fill="both", expand=True)

    def _build_queue_panel(self):
        self._queue_frame = tk.Frame(self._content, bg=BG2)
        self._queue_tree  = _make_tree(
            self._queue_frame,
            columns=("id", "tipo", "monto", "hora"),
            headings=("ID", "TIPO", "MONTO", "HORA"),
            widths=(120, 120, 100, 80))

    def _build_stack_panel(self):
        self._stack_frame = tk.Frame(self._content, bg=BG2)
        tk.Label(self._stack_frame, text="▼  TOPE DE LA PILA",
                 font=("Courier New", 8), bg=BG2, fg=PURPLE).pack(anchor="w", padx=12, pady=(10, 0))
        self._stack_tree = _make_tree(
            self._stack_frame,
            columns=("pos", "nombre", "desc", "hora"),
            headings=("POS", "PASO", "DESCRIPCIÓN", "HORA"),
            widths=(40, 160, 260, 70))
        tk.Label(self._stack_frame, text="▲  BASE DE LA PILA",
                 font=("Courier New", 8), bg=BG2, fg=MUTED).pack(anchor="w", padx=12, pady=(0, 4))
        tk.Label(self._stack_frame, text="HISTORIAL DE ROLLBACKS",
                 font=("Courier New", 8), bg=BG2, fg=ORANGE).pack(anchor="w", padx=12, pady=(8, 0))
        self._rb_tree = _make_tree(
            self._stack_frame,
            columns=("nombre", "hora_rev"),
            headings=("PASO REVERTIDO", "HORA"),
            widths=(260, 80))

    def _build_audit_panel(self):
        self._audit_frame  = tk.Frame(self._content, bg=BG2)
        cap = self._engine.audit.capacity()
        tk.Label(self._audit_frame,
                 text=f"Arreglo circular de capacidad fija = {cap} celdas",
                 font=("Courier New", 8), bg=BG2, fg=MUTED).pack(anchor="w", padx=12, pady=(10, 4))
        self._audit_canvas = tk.Canvas(self._audit_frame, bg=BG2,
                                       height=62, highlightthickness=0)
        self._audit_canvas.pack(fill="x", padx=12, pady=4)
        self._audit_tree = _make_tree(
            self._audit_frame,
            columns=("idx", "id", "tipo", "razon", "hora"),
            headings=("[i]", "ID", "TIPO", "RAZÓN", "HORA"),
            widths=(40, 110, 110, 200, 80))

    # ── refresh dispatcher ────────────────────────────────────
    def refresh_tab(self):
        tab = self.tab_var.get()
        for f in [self._log_frame, self._queue_frame,
                  self._stack_frame, self._audit_frame]:
            f.pack_forget()
        dispatch = {
            "log":   (self._log_frame,   self._refresh_log),
            "cola":  (self._queue_frame,  self._refresh_queue),
            "pila":  (self._stack_frame,  self._refresh_stack),
            "audit": (self._audit_frame,  self._refresh_audit),
        }
        frame, fn = dispatch[tab]
        frame.pack(fill="both", expand=True)
        fn()

    def show_log(self):
        self.tab_var.set("log")
        self.refresh_tab()

    # ── individual refresh methods ────────────────────────────
    def _refresh_log(self):
        self._log_text.config(state="normal")
        self._log_text.delete("1.0", "end")
        for msg, tag in self._engine.event_log[-80:]:
            self._log_text.insert("end", msg + "\n", tag)
        self._log_text.config(state="disabled")
        self._log_text.see("end")

    def _refresh_queue(self):
        for row in self._queue_tree.get_children():
            self._queue_tree.delete(row)
        for txn in self._engine.queue.peek_all():
            amount = f"${txn.get('monto', 0):,.2f}" if "monto" in txn else "—"
            self._queue_tree.insert("", "end",
                values=(txn["id"], txn["tipo"], amount, txn.get("timestamp", "")))

    def _refresh_stack(self):
        for row in self._stack_tree.get_children():
            self._stack_tree.delete(row)
        for i, step in enumerate(self._engine.stack.peek_all(), 1):
            self._stack_tree.insert("", "end",
                values=(i, step["nombre"], step.get("desc", ""), step.get("exec_time", "")))
        for row in self._rb_tree.get_children():
            self._rb_tree.delete(row)
        for step in self._engine.stack.get_rollbacks()[-8:]:
            self._rb_tree.insert("", "end",
                values=(step["nombre"], step.get("rev_time", "")))

    def _refresh_audit(self):
        failures = self._engine.audit.get_failures()
        cap      = self._engine.audit.capacity()
        c = self._audit_canvas
        c.delete("all")
        cw     = c.winfo_width() or 600
        cell_w = (cw - 20) // cap
        for i in range(cap):
            x0, y0 = 10 + i * cell_w, 8
            x1, y1 = x0 + cell_w - 4, 54
            filled  = i < len(failures)
            c.create_rectangle(x0, y0, x1, y1,
                               fill="#2a1000" if filled else BG3,
                               outline=ORANGE if filled else BORDER, width=1)
            c.create_text((x0+x1)//2, 20, text=f"[{i:02d}]",
                          fill=MUTED, font=("Courier New", 7))
            if filled:
                c.create_text((x0+x1)//2, 38, text=failures[i]["tipo"][:3],
                              fill=ORANGE, font=("Courier New", 8, "bold"))
        for row in self._audit_tree.get_children():
            self._audit_tree.delete(row)
        for i, f in enumerate(failures):
            self._audit_tree.insert("", "end",
                values=(f"[{i:02d}]", f["id"], f["tipo"],
                        f.get("razon", ""), f.get("fail_time", "")))


# ══════════════════════════════════════════════════════════════════
#  SHARED WIDGET HELPERS (module-level, reused by both panels)
# ══════════════════════════════════════════════════════════════════
def _stat_card(parent: tk.Widget, label: str, color: str) -> tk.Label:
    f = tk.Frame(parent, bg=BG3, width=90, height=62)
    f.pack(side="left", padx=4, expand=True, fill="x")
    f.pack_propagate(False)
    val = tk.Label(f, text="0", font=("Courier New", 20, "bold"),
                   bg=BG3, fg=color)
    val.pack(pady=(8, 0))
    tk.Label(f, text=label, font=("Courier New", 7),
             bg=BG3, fg=MUTED).pack()
    return val


def _btn(parent: tk.Widget, text: str, fg: str, cmd) -> tk.Button:
    return tk.Button(parent, text=text, command=cmd,
                     font=("Courier New", 8, "bold"),
                     bg=BG3, fg=fg, activebackground=BG,
                     activeforeground=fg, relief="flat",
                     padx=10, pady=6, cursor="hand2",
                     highlightthickness=1,
                     highlightbackground=BORDER)


def _make_tree(parent, columns, headings, widths) -> ttk.Treeview:
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("S.Treeview",
                    background=BG3, foreground=TEXT,
                    fieldbackground=BG3, rowheight=26,
                    font=FONT_MONO_SM, borderwidth=0)
    style.configure("S.Treeview.Heading",
                    background=BG2, foreground=MUTED,
                    font=("Courier New", 8, "bold"), relief="flat")
    style.map("S.Treeview",
              background=[("selected", BG)],
              foreground=[("selected", GOLD)])
    frame = tk.Frame(parent, bg=BG2)
    frame.pack(fill="both", expand=True, padx=12, pady=6)
    tree = ttk.Treeview(frame, columns=columns,
                        show="headings", style="S.Treeview")
    for col, head, w in zip(columns, headings, widths):
        tree.heading(col, text=head)
        tree.column(col, width=w, anchor="w")
    sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)
    return tree
