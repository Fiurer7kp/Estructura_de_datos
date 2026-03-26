"""
CI/CD Simulator - Core Data Structures
Autor: Sebastian Coral | Ing. de Software
"""
from collections import deque
from datetime import datetime
import random

# ── ARRAY — Agentes de Ejecución ──────────────
EXECUTION_AGENTS = [
    {"id": 0, "name": "Ubuntu 22.04",   "icon": "🐧", "status": "idle"},
    {"id": 1, "name": "Windows Server", "icon": "🪟", "status": "idle"},
    {"id": 2, "name": "macOS Ventura",  "icon": "🍎", "status": "idle"},
    {"id": 3, "name": "Alpine Linux",   "icon": "🏔️", "status": "idle"},
]

# ── LINKED LIST — Stages del Pipeline ─────────
class StageNode:
    def __init__(self, name, description, emoji):
        self.name, self.description, self.emoji = name, description, emoji
        self.status = "pending"   # pending | running | success | failed
        self.next   = None

class PipelineLinkedList:
    def __init__(self):
        self.head = None
        for name, desc, emoji in [
            ("Checkout",              "Clona el repositorio",         "📥"),
            ("Instalar Dependencias", "Instala paquetes requeridos",  "📦"),
            ("Linter",                "Analiza calidad del código",   "🔍"),
            ("Pruebas Unitarias",     "Ejecuta suite de tests",       "🧪"),
            ("Despliegue",            "Publica versión en producción","🚀"),
        ]:
            self._append(StageNode(name, desc, emoji))

    def _append(self, node):
        if not self.head: self.head = node
        else:
            cur = self.head
            while cur.next: cur = cur.next
            cur.next = node

    def to_list(self):
        nodes, cur = [], self.head
        while cur: nodes.append(cur); cur = cur.next
        return nodes

    def reset(self):
        for n in self.to_list(): n.status = "pending"

# ── QUEUE — Cola de Jobs ───────────────────────
class JobQueue:
    def __init__(self):
        self._q = deque()
        self._c = 1

    def enqueue(self, developer, branch):
        job = {"id": f"JOB-{self._c:03d}", "developer": developer,
               "branch": branch, "timestamp": datetime.now().strftime("%H:%M:%S")}
        self._q.append(job); self._c += 1
        return job

    def dequeue(self):       return self._q.popleft() if self._q else None
    def peek(self):          return self._q[0] if self._q else None
    def size(self):          return len(self._q)
    def to_list(self):       return list(self._q)

# ── STACK — Historial de Despliegues ──────────
class DeploymentStack:
    def __init__(self): self._s = []

    def push(self, version, job_id):
        if self._s: self._s[-1]["status"] = "previous"
        deploy = {"version": version, "job_id": job_id,
                  "deployed": datetime.now().strftime("%H:%M:%S"), "status": "active"}
        self._s.append(deploy)
        return deploy

    def rollback(self):
        if len(self._s) < 2: return None, None
        removed = self._s.pop()
        self._s[-1]["status"] = "active"
        return removed, self._s[-1]

    def peek(self):     return self._s[-1] if self._s else None
    def size(self):     return len(self._s)
    def to_list(self):  return list(reversed(self._s))

# ── LIST — Visor de Logs ───────────────────────
class LogViewer:
    ICONS = {"INFO": "🔵", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}

    def __init__(self): self._logs = []

    def add(self, message, level="INFO", source="system"):
        entry = {"time": datetime.now().strftime("%H:%M:%S"), "level": level,
                 "icon": self.ICONS.get(level,"🔵"), "source": source, "message": message}
        self._logs.append(entry)
        return entry

    def filter(self, level="ALL", search=""):
        r = self._logs
        if level != "ALL": r = [l for l in r if l["level"] == level]
        if search:         r = [l for l in r if search.lower() in l["message"].lower()]
        return r

    def clear(self):  self._logs.clear()
    def count(self):  return len(self._logs)
