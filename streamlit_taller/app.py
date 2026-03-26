"""
CI/CD Simulator — Panel de Control
Autor: Sebastian Coral | Ing. de Software
"""
import streamlit as st, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from backend.engine import CICDEngine

# ── Config ────────────────────────────────────
st.set_page_config(
    page_title="CI/CD Simulator | Sebastian Coral",
    page_icon="🚀", layout="wide",
)

# ── CSS ───────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background:#0d1117; }
[data-testid="stSidebar"]          { background:#161b22; border-right:1px solid #30363d; }
.block-container { padding-top:1.2rem; }
h1,h2,h3 { color:#e6edf3!important; }

.card {
    background:#161b22; border:1px solid #30363d;
    border-radius:10px; padding:.9rem 1.1rem; margin-bottom:.5rem;
}
.card-label { font-size:.7rem; color:#8b949e; text-transform:uppercase; letter-spacing:.08em; }
.card-val   { font-size:1.7rem; font-weight:700; color:#e6edf3; }

.agent-idle { background:#1f6feb18; border:1px solid #1f6feb55; border-radius:8px;
              padding:.4rem .9rem; color:#58a6ff; margin:.2rem 0; display:block; }
.agent-busy { background:#f7853318; border:1px solid #f7853355; border-radius:8px;
              padding:.4rem .9rem; color:#f78533; margin:.2rem 0; display:block; }

.stage { text-align:center; padding:.5rem .3rem; border-radius:8px; }
.stage-pending { color:#8b949e; background:#21262d; }
.stage-running { color:#d29922; background:#2d2204; border:1px solid #d2992244; font-weight:700; }
.stage-success { color:#3fb950; background:#0d2414; border:1px solid #3fb95044; }
.stage-failed  { color:#f85149; background:#2d0f0e; border:1px solid #f8514944; }

.log-console {
    background:#0d1117; border:1px solid #30363d; border-radius:8px;
    padding:.9rem; font-family:'Courier New',monospace; font-size:.76rem;
    max-height:280px; overflow-y:auto;
}
.log-INFO    { color:#58a6ff; margin:.05rem 0; }
.log-SUCCESS { color:#3fb950; margin:.05rem 0; }
.log-WARNING { color:#d29922; margin:.05rem 0; }
.log-ERROR   { color:#f85149; margin:.05rem 0; }

.job-row    { display:flex; justify-content:space-between; align-items:center; }
.pill-active  { background:#1f6feb; color:#fff; padding:.15rem .65rem;
                border-radius:20px; font-size:.75rem; font-weight:700; }
.pill-prev    { background:#30363d; color:#8b949e; padding:.15rem .65rem;
                border-radius:20px; font-size:.75rem; }
.divider { border-top:1px solid #30363d; margin:.8rem 0; }
</style>
""", unsafe_allow_html=True)

# ── State ─────────────────────────────────────
if "engine" not in st.session_state:
    st.session_state.engine = CICDEngine()
engine: CICDEngine = st.session_state.engine

# ── Sidebar ───────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 CI/CD Simulator")
    st.caption("**Sebastian Coral** | Ing. de Software")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("#### ➕ Encolar Job")
    dev    = st.text_input("Desarrollador", placeholder="ej. dev-alice", label_visibility="collapsed")
    branch = st.selectbox("Branch", ["main","develop","feature/login","feature/dashboard","hotfix/bug-42"], label_visibility="collapsed")
    if st.button("📤 Encolar Job", use_container_width=True, type="primary"):
        if dev.strip(): engine.submit_job(dev.strip(), branch); st.success("Job encolado ✓")
        else:           st.warning("Ingresa un nombre de desarrollador")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("#### ▶ Ejecución")
    if st.button("⚡ Ejecutar Pipeline", use_container_width=True):
        events = engine.run_pipeline()
        types  = [e["type"] for e in events]
        if   "deployed"        in types: st.success("Pipeline exitoso 🎉")
        elif "pipeline_failed" in types: st.error("Pipeline falló ✗")
        elif not events:                 st.info("Cola vacía o sin agentes libres")
        st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("#### ⏪ Rollback")
    if st.button("🚨 Rollback de Emergencia", use_container_width=True, type="secondary"):
        removed, restored = engine.emergency_rollback()
        if removed: st.warning(f"Revertido: {removed['version']} → {restored['version']}")
        else:       st.error("No hay versión anterior en el stack")
        st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🗑️ Limpiar Logs", use_container_width=True):
            engine.logs.clear(); st.rerun()
    with c2:
        if st.button("🔄 Reset", use_container_width=True):
            del st.session_state["engine"]; st.rerun()

# ── Header ────────────────────────────────────
st.markdown("# 🛠️ Pipeline de Integración y Despliegue")
st.caption("Simulador CI/CD — Estructuras de Datos en acción &nbsp;|&nbsp; *Sebastian Coral, Ing. de Software*")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
busy    = sum(1 for a in engine.agents if a["status"] == "busy")
current = engine.deploy_stack.peek()

for col, label, value in [
    (k1, "📋 Jobs en Cola",        engine.job_queue.size()),
    (k2, "⚙️ Agentes Ocupados",    f"{busy}/{len(engine.agents)}"),
    (k3, "📦 Versiones en Stack",  engine.deploy_stack.size()),
    (k4, "🏷️ Versión Activa",      current["version"] if current else "—"),
]:
    col.markdown(f'<div class="card"><div class="card-label">{label}</div>'
                 f'<div class="card-val">{value}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Agents | Stages ───────────────────────────
col_a, col_p = st.columns([1, 2])

with col_a:
    st.markdown("### 🖥️ Agentes de Ejecución")
    st.caption("Array de 4 servidores virtuales")
    for a in engine.agents:
        css = "agent-busy" if a["status"] == "busy" else "agent-idle"
        lbl = "OCUPADO" if a["status"] == "busy" else "LIBRE"
        st.markdown(
            f'<span class="{css}">{a["icon"]} <b>{a["name"]}</b>'
            f'<span style="float:right;font-size:.7rem">{lbl}</span></span>',
            unsafe_allow_html=True
        )

with col_p:
    st.markdown("### 🔗 Stages del Pipeline")
    st.caption("Lista Enlazada Simple — cada nodo invoca al siguiente tras éxito")
    stages = engine.pipeline.to_list()
    cols   = st.columns(len(stages))
    icons  = {"pending":"⏳","running":"⚙️","success":"✅","failed":"❌"}
    for col, s in zip(cols, stages):
        col.markdown(
            f'<div class="stage stage-{s.status}">'
            f'{icons.get(s.status,"❓")}<br>'
            f'<b style="font-size:.78rem">{s.name}</b><br>'
            f'<span style="font-size:.65rem;color:#8b949e">{s.description}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Queue | Stack ─────────────────────────────
col_q, col_s = st.columns(2)

with col_q:
    st.markdown("### 📥 Cola de Jobs (Queue)")
    st.caption("FIFO — primer job encolado, primero en ejecutarse")
    jobs = engine.job_queue.to_list()
    if jobs:
        for i, j in enumerate(jobs):
            st.markdown(
                f'<div class="card" style="padding:.55rem 1rem">'
                f'<div class="job-row">'
                f'<span>{"🔜" if i==0 else "⏳"} <b>{j["id"]}</b> — '
                f'{j["developer"]} <code style="font-size:.72rem">{j["branch"]}</code></span>'
                f'<span style="color:#8b949e;font-size:.72rem">{j["timestamp"]}</span>'
                f'</div></div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<p style="color:#8b949e;font-size:.85rem">Cola vacía</p>', unsafe_allow_html=True)

with col_s:
    st.markdown("### 📦 Stack de Despliegues")
    st.caption("LIFO — la cima es la versión activa en producción")
    deploys = engine.deploy_stack.to_list()
    if deploys:
        for d in deploys:
            pill = "pill-active" if d["status"] == "active" else "pill-prev"
            st.markdown(
                f'<div class="card" style="padding:.55rem 1rem">'
                f'<div class="job-row">'
                f'<span><span class="{pill}">{d["version"]}</span> '
                f'<span style="color:#8b949e;font-size:.8rem">← {d["job_id"]}</span></span>'
                f'<span style="color:#8b949e;font-size:.72rem">{d["deployed"]}</span>'
                f'</div></div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<p style="color:#8b949e;font-size:.85rem">Sin despliegues aún</p>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Logs ──────────────────────────────────────
st.markdown("### 📄 Visor de Logs en Tiempo Real")
st.caption("Lista nativa — registros filtrables y buscables")

lc1, lc2 = st.columns([1, 3])
with lc1:
    lvl = st.selectbox("Nivel", ["ALL","INFO","SUCCESS","WARNING","ERROR"], label_visibility="collapsed")
with lc2:
    srch = st.text_input("Buscar...", placeholder="Filtrar mensajes...", label_visibility="collapsed")

logs = engine.logs.filter(lvl, srch)
lines = "\n".join(
    f'<div class="log-{l["level"]}">[{l["time"]}] {l["icon"]} '
    f'<b>{l["level"]}</b> <span style="color:#8b949e">[{l["source"]}]</span> {l["message"]}</div>'
    for l in reversed(logs[-120:])
) or "<span style='color:#8b949e'>Sin registros</span>"

st.markdown(f'<div class="log-console">{lines}</div>', unsafe_allow_html=True)
st.caption(f"Total: {engine.logs.count()} registros | Mostrando: {len(logs)}")
