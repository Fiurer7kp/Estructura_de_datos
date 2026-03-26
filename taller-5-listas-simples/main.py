# ============================================================
#  ENTRY POINT: main.py
#  Run this file to launch the application:
#      python main.py
#
#  Project structure:
#      main.py            ← entry point (this file)
#      app.py             ← main window & layout
#      widgets.py         ← reusable UI components
#      data_structure.py  ← Node + SimpleLinkedList
#      theme.py           ← colors & fonts
# ============================================================

from app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
