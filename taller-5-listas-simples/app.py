# ============================================================
#  MODULE: app.py
#  Contains: Main App window — layout, input bar, render loop
# ============================================================

import tkinter as tk
import time

from data_structure import SimpleLinkedList
from widgets import StatCard, TaskCard
from theme import (
    BG, SURFACE, SURFACE2, BORDER,
    ACCENT, RED, AMBER, GREEN,
    TEXT, MUTED, WHITE,
    PRIORITY_COLOR,
    FONT_MONO_SM, FONT_MONO_MD, FONT_MONO_LG,
    FONT_UI_MD, FONT_UI_LG, FONT_UI_TITLE
)


class App(tk.Tk):
    """
    Main application window.
    Manages the UI layout and delegates all data operations
    to the SimpleLinkedList instance.
    """

    def __init__(self):
        super().__init__()
        self.linked_list = SimpleLinkedList()

        self.title("Taller — Listas Simples con Punteros")
        self.geometry("1100x740")
        self.minsize(900, 620)
        self.configure(bg=BG)

        self._build_header()
        self._build_input_bar()
        self._build_stats_bar()
        self._build_pointer_chain()
        self._build_list_area()
        self._build_log_bar()

        self._render()
        self._tick()   # start real-time clock

    # ══════════════════════════════════════════════════════════
    #  LAYOUT SECTIONS
    # ══════════════════════════════════════════════════════════

    def _build_header(self):
        """Top bar: badge, title, live clock, author."""
        hdr = tk.Frame(self, bg=SURFACE,
                       highlightbackground=BORDER,
                       highlightthickness=1, pady=12)
        hdr.pack(fill="x")

        # Badge
        badge = tk.Frame(hdr, bg=ACCENT, padx=10, pady=4)
        badge.pack(side="left", padx=14)
        tk.Label(badge, text="¡Hala Madrid, hasta el final! ⚪🏆",
                 bg=ACCENT, fg=WHITE,
                 font=FONT_MONO_LG).pack()

        # Title
        tk.Label(hdr, text="Taller — Gestor de Tareas con Punteros",
                 bg=SURFACE, fg=TEXT,
                 font=FONT_UI_TITLE).pack(side="left", padx=10)

        # Right side: clock + author stacked
        right = tk.Frame(hdr, bg=SURFACE)
        right.pack(side="right", padx=16)

        self._clock_lbl = tk.Label(right, text="",
                                   bg=SURFACE, fg=ACCENT,
                                   font=("Courier", 18, "bold"))
        self._clock_lbl.pack(anchor="e")

        tk.Label(right, text="Elaborado por Sebastian",
                 bg=SURFACE, fg=MUTED,
                 font=FONT_UI_MD).pack(anchor="e")

    def _build_input_bar(self):
        """Input field, priority selector, time estimate, insert button."""
        bar = tk.Frame(self, bg=SURFACE,
                       highlightbackground=BORDER,
                       highlightthickness=1, pady=12)
        bar.pack(fill="x")

        # Row 1 — task + priority + button
        row1 = tk.Frame(bar, bg=SURFACE)
        row1.pack(padx=18, fill="x")

        self._entry = tk.Entry(row1, bg=SURFACE2, fg=MUTED,
                               insertbackground=TEXT,
                               font=FONT_UI_LG,
                               relief="flat",
                               highlightbackground=BORDER,
                               highlightthickness=1, bd=8)
        self._entry.insert(0, "Escribe una tarea...")
        self._entry.pack(side="left", fill="x", expand=True, ipady=6)
        self._entry.bind("<FocusIn>",  self._placeholder_clear)
        self._entry.bind("<FocusOut>", self._placeholder_restore)
        self._entry.bind("<Return>",   lambda _: self._do_insert())

        tk.Label(row1, text="Prioridad:", bg=SURFACE, fg=MUTED,
                 font=FONT_UI_MD).pack(side="left", padx=(12, 4))

        self._priority_var = tk.StringVar(value="Media")
        for priority, (color, _) in PRIORITY_COLOR.items():
            tk.Radiobutton(row1, text=priority,
                           variable=self._priority_var, value=priority,
                           bg=SURFACE, fg=color,
                           activebackground=SURFACE,
                           selectcolor=SURFACE2,
                           activeforeground=color,
                           font=(*FONT_UI_MD[:1], FONT_UI_MD[1], "bold"),
                           cursor="hand2"
                           ).pack(side="left", padx=3)

        tk.Button(row1, text="+ Insertar Nodo",
                  command=self._do_insert,
                  bg=ACCENT, fg=WHITE,
                  font=FONT_MONO_LG,
                  relief="flat", bd=0,
                  activebackground=ACCENT,
                  cursor="hand2",
                  padx=14, pady=7
                  ).pack(side="left", padx=(12, 0))

        # "Limpiar completadas" button
        tk.Button(row1, text="🗑  Limpiar completadas",
                  command=self._do_clear_completed,
                  bg=SURFACE2, fg=RED,
                  font=FONT_UI_MD,
                  relief="flat", bd=0,
                  highlightbackground=BORDER,
                  highlightthickness=1,
                  activebackground=SURFACE2,
                  cursor="hand2",
                  padx=12, pady=7
                  ).pack(side="left", padx=(10, 0))

        # Row 2 — estimated time
        row2 = tk.Frame(bar, bg=SURFACE)
        row2.pack(padx=18, fill="x", pady=(10, 0))

        tk.Label(row2, text="⏱  Tiempo estimado:",
                 bg=SURFACE, fg=MUTED,
                 font=FONT_UI_MD).pack(side="left", padx=(0, 8))

        self._time_entry = tk.Entry(row2, bg=SURFACE2, fg=TEXT,
                                    insertbackground=TEXT,
                                    font=FONT_UI_MD,
                                    relief="flat",
                                    highlightbackground=BORDER,
                                    highlightthickness=1, bd=6,
                                    width=22)
        self._time_entry.pack(side="left", ipady=4)

        tk.Label(row2, text="(ej: 1 hora, 30 min, 2 días)",
                 bg=SURFACE, fg=MUTED,
                 font=FONT_UI_MD).pack(side="left", padx=(8, 0))

        self._time_hint = tk.Label(row2, text="",
                                   bg=SURFACE, fg=ACCENT,
                                   font=(*FONT_UI_MD[:1], FONT_UI_MD[1], "bold"))
        self._time_hint.pack(side="left", padx=(14, 0))
        self._priority_var.trace_add("write", self._update_time_hint)
        self._update_time_hint()

    def _build_stats_bar(self):
        """Summary stat cards + progress bar."""
        frame = tk.Frame(self, bg=BG, pady=10)
        frame.pack(fill="x", padx=18)

        self._stat_total   = StatCard(frame, "TOTAL NODOS",  "0",    ACCENT)
        self._stat_pending = StatCard(frame, "PENDIENTES",   "0",    RED)
        self._stat_done    = StatCard(frame, "COMPLETADAS",  "0",    GREEN)
        self._stat_head    = StatCard(frame, "HEAD APUNTA A","NULL", ACCENT)

        for card in (self._stat_total, self._stat_pending,
                     self._stat_done,  self._stat_head):
            card.pack(side="left", padx=(0, 10))

        # Progress bar (right side of stats row)
        prog_frame = tk.Frame(frame, bg=SURFACE,
                              highlightbackground=BORDER,
                              highlightthickness=1,
                              padx=16, pady=10)
        prog_frame.pack(side="left", padx=(0, 10), fill="y")

        tk.Label(prog_frame, text="PROGRESO", bg=SURFACE, fg=MUTED,
                 font=FONT_MONO_SM).pack()

        bar_bg = tk.Frame(prog_frame, bg=BORDER,
                          height=14, width=180)
        bar_bg.pack(pady=(4, 0))
        bar_bg.pack_propagate(False)

        self._progress_bar = tk.Frame(bar_bg, bg=GREEN, height=14, width=0)
        self._progress_bar.pack(side="left", fill="y")

        self._progress_lbl = tk.Label(prog_frame, text="0%",
                                      bg=SURFACE, fg=GREEN,
                                      font=FONT_MONO_MD)
        self._progress_lbl.pack()

    def _build_pointer_chain(self):
        """Visual horizontal chain: HEAD → [#1] → [#2] → NULL"""
        self._chain_frame = tk.Frame(self, bg=BG)
        self._chain_frame.pack(fill="x", padx=18, pady=(0, 6))

    def _build_list_area(self):
        """Scrollable area that holds TaskCard widgets."""
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        self._canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(outer, orient="vertical",
                                 command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._list_inner = tk.Frame(self._canvas, bg=BG)
        self._canvas_win = self._canvas.create_window(
            (0, 0), window=self._list_inner, anchor="nw")

        self._list_inner.bind("<Configure>", lambda e:
            self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>", lambda e:
            self._canvas.itemconfig(self._canvas_win, width=e.width))
        self._canvas.bind_all("<MouseWheel>", lambda e:
            self._canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    def _build_log_bar(self):
        """Bottom status bar showing the last operation + uptime."""
        bar = tk.Frame(self, bg=SURFACE,
                       highlightbackground=BORDER,
                       highlightthickness=1, pady=7)
        bar.pack(fill="x", side="bottom")

        tk.Label(bar, text="LOG ›", bg=SURFACE, fg=MUTED,
                 font=FONT_MONO_MD).pack(side="left", padx=14)

        self._log_label = tk.Label(bar,
                                   text="Lista inicializada — HEAD → NULL",
                                   bg=SURFACE, fg=GREEN,
                                   font=FONT_MONO_SM)
        self._log_label.pack(side="left")

        self._uptime_lbl = tk.Label(bar, text="",
                                    bg=SURFACE, fg=MUTED,
                                    font=FONT_MONO_SM)
        self._uptime_lbl.pack(side="right", padx=16)
        self._start_time = time.time()

    # ══════════════════════════════════════════════════════════
    #  REAL-TIME CLOCK & UPTIME
    # ══════════════════════════════════════════════════════════

    def _tick(self):
        """Updates clock and uptime every second."""
        now = time.strftime("%H:%M:%S")
        self._clock_lbl.config(text=now)

        elapsed = int(time.time() - self._start_time)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        self._uptime_lbl.config(
            text=f"Sesión activa: {h:02d}:{m:02d}:{s:02d}")

        self.after(1000, self._tick)

    # ══════════════════════════════════════════════════════════
    #  OPERATIONS
    # ══════════════════════════════════════════════════════════

    def _do_insert(self):
        text = self._entry.get().strip()
        if not text or text == "Escribe una tarea...":
            self._entry.focus()
            return
        priority  = self._priority_var.get()
        estimated = self._time_entry.get().strip()
        node      = self.linked_list.insert(text, priority, estimated)

        self._entry.delete(0, "end")
        self._time_entry.delete(0, "end")
        self._entry.focus()

        addr = hex(0x1000 + node.id * 64)
        self._log(f"insert()  nodo #{node.id} @ {addr}  prioridad={priority}  .next → NULL")
        self._render()

    def _do_complete(self, id_: int):
        self.linked_list.complete(id_)
        self._log(f"complete()  nodo #{id_}  .done = True")
        self._render()

    def _do_delete(self, id_: int):
        if self.linked_list.delete(id_):
            self._log(f"delete()  nodo #{id_} eliminado — puntero anterior reenlazado")
        self._render()

    def _do_clear_completed(self):
        removed = self.linked_list.clear_completed()
        if removed:
            self._log(f"clear_completed()  {removed} nodo(s) eliminados")
        else:
            self._log("clear_completed()  no hay tareas completadas")
        self._render()

    # ══════════════════════════════════════════════════════════
    #  RENDER
    # ══════════════════════════════════════════════════════════

    def _render(self):
        """Rebuild the entire list view and update all stat widgets."""
        nodes = self.linked_list.traverse()

        # Stats
        total   = self.linked_list.size
        done    = self.linked_list.total_done
        pending = self.linked_list.total_pending

        self._stat_total.set(str(total))
        self._stat_pending.set(str(pending))
        self._stat_done.set(str(done))
        head_txt = f"nodo #{self.linked_list.head.id}" \
                   if self.linked_list.head else "NULL"
        self._stat_head.set(head_txt)

        # Progress bar
        pct = int((done / total) * 100) if total > 0 else 0
        self._progress_bar.config(width=int(180 * pct / 100))
        self._progress_lbl.config(text=f"{pct}%",
                                  fg=GREEN if pct == 100 else AMBER if pct > 0 else MUTED)

        # Pointer chain
        for w in self._chain_frame.winfo_children():
            w.destroy()
        if nodes:
            tk.Label(self._chain_frame, text="HEAD",
                     bg=BG, fg=ACCENT,
                     font=FONT_MONO_MD).pack(side="left")
            for node in nodes:
                tk.Label(self._chain_frame, text=" → ",
                         bg=BG, fg=MUTED,
                         font=FONT_MONO_SM).pack(side="left")
                color = GREEN if node.done else TEXT
                tk.Label(self._chain_frame, text=f"[#{node.id}]",
                         bg=BG, fg=color,
                         font=FONT_MONO_MD).pack(side="left")
            tk.Label(self._chain_frame, text=" → NULL",
                     bg=BG, fg=RED,
                     font=FONT_MONO_MD).pack(side="left")

        # Task cards
        for w in self._list_inner.winfo_children():
            w.destroy()

        if not nodes:
            tk.Label(self._list_inner,
                     text="\n\n⬡   Lista vacía — HEAD apunta a NULL\n",
                     bg=BG, fg=MUTED,
                     font=FONT_UI_LG).pack(pady=40)
            return

        for i, node in enumerate(nodes):
            TaskCard(self._list_inner, node,
                     is_head=(i == 0),
                     on_complete=self._do_complete,
                     on_delete=self._do_delete
                     ).pack(fill="x", pady=(0, 8))

    # ══════════════════════════════════════════════════════════
    #  HELPERS
    # ══════════════════════════════════════════════════════════

    def _log(self, message: str):
        ts = time.strftime("%H:%M:%S")
        self._log_label.config(text=f"[{ts}]  {message}")

    def _placeholder_clear(self, _):
        if self._entry.get() == "Escribe una tarea...":
            self._entry.delete(0, "end")
            self._entry.config(fg=TEXT)

    def _placeholder_restore(self, _):
        if not self._entry.get():
            self._entry.insert(0, "Escribe una tarea...")
            self._entry.config(fg=MUTED)

    def _update_time_hint(self, *_):
        hints = {
            "Alta":  "⚠  Alta prioridad — define un tiempo corto",
            "Media": "📋  Tiempo razonable para esta tarea",
            "Baja":  "🕐  Sin urgencia — estima con calma",
        }
        color_map = {"Alta": RED, "Media": AMBER, "Baja": GREEN}
        prio = self._priority_var.get()
        self._time_hint.config(text=hints.get(prio, ""),
                               fg=color_map.get(prio, ACCENT))
