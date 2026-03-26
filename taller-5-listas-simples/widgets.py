# ============================================================
#  MODULE: widgets.py
#  Contains: Reusable Tkinter widget components
#  - StatCard  : summary number card
#  - TaskCard  : individual node card with actions
# ============================================================

import time
import tkinter as tk
from theme import (
    SURFACE, SURFACE2, BORDER, ACCENT, ACCENT_LT,
    TEXT, MUTED, WHITE, RED, GREEN, AMBER,
    PRIORITY_COLOR,
    FONT_MONO_SM, FONT_MONO_MD, FONT_MONO_LG, FONT_MONO_XL,
    FONT_UI_SM, FONT_UI_MD, FONT_UI_LG, FONT_UI_XL
)


def _elapsed(created_at: float) -> str:
    """Returns a human-readable elapsed time string."""
    seconds = int(time.time() - created_at)
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}min"
    elif seconds < 86400:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        return f"{h}h {m}min"
    else:
        d = seconds // 86400
        h = (seconds % 86400) // 3600
        return f"{d}d {h}h"


# ── Stat Card ─────────────────────────────────────────────────
class StatCard(tk.Frame):
    """Displays a label + large numeric/text value."""
    def __init__(self, parent, label: str, value: str,
                 color: str, **kw):
        super().__init__(parent, bg=SURFACE,
                         highlightbackground=BORDER,
                         highlightthickness=1,
                         padx=20, pady=10, **kw)
        tk.Label(self, text=label, bg=SURFACE, fg=MUTED,
                 font=FONT_MONO_SM).pack()
        self._value_lbl = tk.Label(self, text=value,
                                   bg=SURFACE, fg=color,
                                   font=FONT_MONO_XL)
        self._value_lbl.pack()

    def set(self, value: str):
        self._value_lbl.config(text=value)


# ── Badge helper ──────────────────────────────────────────────
def make_badge(parent, text: str, fg: str, bg: str):
    f = tk.Frame(parent, bg=bg, padx=8, pady=2)
    f.pack(side="left", padx=(0, 6))
    tk.Label(f, text=text, bg=bg, fg=fg,
             font=FONT_MONO_SM).pack()
    return f


# ── Task Card ─────────────────────────────────────────────────
class TaskCard(tk.Frame):
    """
    Visual representation of a single Node.
    Shows task data, elapsed time, pointer info, and action buttons.
    """
    def __init__(self, parent, node, is_head: bool,
                 on_complete, on_delete, **kw):
        super().__init__(parent, bg=SURFACE,
                         highlightbackground=BORDER,
                         highlightthickness=1, **kw)
        self.node        = node
        self.on_complete = on_complete
        self.on_delete   = on_delete
        self._build(is_head)
        self.bind("<Enter>", lambda _: self.configure(highlightbackground=ACCENT))
        self.bind("<Leave>", lambda _: self.configure(highlightbackground=BORDER))

    def _build(self, is_head: bool):
        prio_fg, prio_bg = PRIORITY_COLOR.get(self.node.priority, (ACCENT, ACCENT_LT))

        # Left color stripe
        tk.Frame(self, bg=prio_fg, width=6).pack(side="left", fill="y")

        # Main body
        body = tk.Frame(self, bg=SURFACE)
        body.pack(side="left", fill="both", expand=True, padx=14, pady=12)

        # Row 1 — badges
        badge_row = tk.Frame(body, bg=SURFACE)
        badge_row.pack(anchor="w")
        if is_head:
            make_badge(badge_row, "HEAD", WHITE, ACCENT)
        make_badge(badge_row, self.node.priority, prio_fg, prio_bg)
        if self.node.done:
            make_badge(badge_row, "✓ COMPLETADA", WHITE, GREEN)

        # Row 2 — task title
        tk.Label(body, text=self.node.task,
                 bg=SURFACE, fg=MUTED if self.node.done else TEXT,
                 font=FONT_UI_LG,
                 wraplength=400, justify="left", anchor="w"
                 ).pack(fill="x", pady=(6, 2))

        # Row 3 — estimated time + elapsed
        info_row = tk.Frame(body, bg=SURFACE)
        info_row.pack(anchor="w", pady=(2, 0))

        if self.node.estimated_time:
            tk.Label(info_row,
                     text=f"⏱ Estimado: {self.node.estimated_time}",
                     bg=SURFACE, fg=prio_fg,
                     font=FONT_UI_MD).pack(side="left", padx=(0, 14))

        elapsed = _elapsed(self.node.created_at)
        tk.Label(info_row,
                 text=f"🕐 En lista: {elapsed}",
                 bg=SURFACE, fg=MUTED,
                 font=FONT_UI_MD).pack(side="left")

        # Row 4 — pointer metadata
        addr_self = hex(0x1000 + self.node.id * 64)
        addr_next = hex(0x1000 + (self.node.id + 1) * 64) \
                    if self.node.next else "NULL"
        tk.Label(body,
                 text=f"id=#{self.node.id}   @{addr_self}   .next → {addr_next}",
                 bg=SURFACE, fg=MUTED,
                 font=FONT_MONO_SM).pack(anchor="w", pady=(4, 0))

        # Action buttons
        btn_frame = tk.Frame(self, bg=SURFACE)
        btn_frame.pack(side="right", padx=14, pady=12)

        if not self.node.done:
            self._btn(btn_frame, "✓  Completar", GREEN,
                      lambda: self.on_complete(self.node.id))
        self._btn(btn_frame, "✕  Eliminar", RED,
                  lambda: self.on_delete(self.node.id))

    def _btn(self, parent, text, color, cmd):
        tk.Button(parent, text=text, command=cmd,
                  bg=color, fg=WHITE,
                  font=FONT_MONO_MD,
                  relief="flat", bd=0,
                  activebackground=color,
                  cursor="hand2",
                  padx=10, pady=6
                  ).pack(pady=(0, 6), fill="x")
