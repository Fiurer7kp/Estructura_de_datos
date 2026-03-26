# 🚀 CI/CD Simulator — Pipeline de Integración y Despliegue
**Autor:** Sebastian Coral | Ing. de Software  
**Materia:** Estructuras de Datos — Cuarto Semestre  
**Docente:** Jhonatan Andres Mideros Narvaez

---

## Estructuras de datos implementadas

| Estructura | Uso en el proyecto |
|---|---|
| **Array** | 4 agentes de ejecución fijos (Ubuntu, Windows, macOS, Alpine) |
| **Queue (Cola)** | Recepción FIFO de Jobs de compilación |
| **Stack (Pila)** | Historial de despliegues para Rollback de Emergencia |
| **List (Lista nativa)** | Visor de Logs con filtrado y búsqueda |
| **Singly Linked List** | Etapas del Pipeline (Checkout → Deploy) |

---

## Instalación y ejecución

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estructura del proyecto

```
cicd_simulator/
├── app.py                  # Frontend Streamlit
├── requirements.txt
├── README.md
└── backend/
    ├── __init__.py
    ├── data_structures.py  # Array, Queue, Stack, List, Linked List
    └── engine.py           # Lógica de negocio / orquestación
```
