# ============================================================
#  MODULE: theme.py
#  Contains: Color palette and font configuration
#  Light theme — clean, professional, high contrast
# ============================================================

# ── Backgrounds ───────────────────────────────────────────
BG         = "#F4F6FB"   # page background
SURFACE    = "#FFFFFF"   # card / panel surface
SURFACE2   = "#EEF1F8"   # input background / secondary surface
BORDER     = "#D0D7E8"   # borders

# ── Accent colors ─────────────────────────────────────────
ACCENT     = "#4F46E5"   # indigo — primary action
ACCENT_LT  = "#EEF2FF"   # indigo light — badge fill

# ── Semantic colors ───────────────────────────────────────
RED        = "#E53E3E"   # high priority / danger
RED_LT     = "#FFF5F5"
AMBER      = "#D97706"   # medium priority / warning
AMBER_LT   = "#FFFBEB"
GREEN      = "#059669"   # low priority / success
GREEN_LT   = "#ECFDF5"

# ── Text ──────────────────────────────────────────────────
TEXT       = "#1A202C"   # primary text
MUTED      = "#718096"   # secondary / placeholder text
WHITE      = "#FFFFFF"

# ── Priority mapping ──────────────────────────────────────
PRIORITY_COLOR = {
    "Alta":  (RED,   RED_LT),
    "Media": (AMBER, AMBER_LT),
    "Baja":  (GREEN, GREEN_LT),
}

# ── Fonts (Courier for monospace sections) ────────────────
FONT_MONO_SM   = ("Courier", 9)
FONT_MONO_MD   = ("Courier", 10, "bold")
FONT_MONO_LG   = ("Courier", 12, "bold")
FONT_MONO_XL   = ("Courier", 22, "bold")

FONT_UI_SM     = ("Segoe UI", 9)
FONT_UI_MD     = ("Segoe UI", 11)
FONT_UI_LG     = ("Segoe UI", 13, "bold")
FONT_UI_XL     = ("Segoe UI", 15, "bold")
FONT_UI_TITLE  = ("Segoe UI", 16, "bold")
