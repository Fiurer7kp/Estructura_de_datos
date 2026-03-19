import { useState } from "react";

// ─── Tipos del sistema ────────────────────────────────────────────────────────
type EstadoPedido =
  | "pendiente"
  | "en_revision"
  | "aprobado"
  | "rechazado"
  | "preparando"
  | "despachado"
  | "entregado";

type Rol = "shipping" | "buyer" | "supervisor" | "seller" | "receiver";

interface Pedido {
  id: string;
  producto: string;
  cantidad: number;
  precio: number;
  proveedor: string;
  estado: EstadoPedido;
  rol: Rol;
  fecha: string;
  cotizacionAceptada?: boolean;
  aprobado?: boolean;
}

// ─── Formato moneda colombiana ────────────────────────────────────────────────
const formatCOP = (valor: number): string =>
  new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  }).format(valor);

// ─── Lista inicial de pedidos ─────────────────────────────────────────────────
const pedidosIniciales: Pedido[] = [
  {
    id: "PED-001",
    producto: 'Televisor Samsung 55" QLED',
    cantidad: 5,
    precio: 4850000,
    proveedor: "Éxito",
    estado: "aprobado",
    rol: "supervisor",
    fecha: "2026-03-10",
    cotizacionAceptada: true,
    aprobado: true,
  },
  {
    id: "PED-002",
    producto: "Nevera LG Inverter 360L",
    cantidad: 3,
    precio: 2990000,
    proveedor: "Alkosto",
    estado: "en_revision",
    rol: "buyer",
    fecha: "2026-03-11",
    cotizacionAceptada: false,
    aprobado: false,
  },
  {
    id: "PED-003",
    producto: "Kit Cocina Acero Inoxidable",
    cantidad: 20,
    precio: 389000,
    proveedor: "Jumbo",
    estado: "preparando",
    rol: "seller",
    fecha: "2026-03-09",
    cotizacionAceptada: true,
    aprobado: true,
  },
  {
    id: "PED-004",
    producto: "Silla Gamer RGB Ergonómica",
    cantidad: 4,
    precio: 1250000,
    proveedor: "Unicentro",
    estado: "despachado",
    rol: "shipping",
    fecha: "2026-03-08",
    cotizacionAceptada: true,
    aprobado: true,
  },
  {
    id: "PED-005",
    producto: "Audífonos Sony WH-1000XM5",
    cantidad: 8,
    precio: 1190000,
    proveedor: "Amazon Colombia",
    estado: "pendiente",
    rol: "buyer",
    fecha: "2026-03-12",
    cotizacionAceptada: false,
    aprobado: false,
  },
  {
    id: "PED-006",
    producto: "Impresora Epson EcoTank L3250",
    cantidad: 2,
    precio: 890000,
    proveedor: "Único",
    estado: "entregado",
    rol: "receiver",
    fecha: "2026-03-07",
    cotizacionAceptada: true,
    aprobado: true,
  },
  {
    id: "PED-007",
    producto: "Tablet Samsung Galaxy Tab A9",
    cantidad: 6,
    precio: 1350000,
    proveedor: "Jumbo",
    estado: "en_revision",
    rol: "supervisor",
    fecha: "2026-03-12",
    cotizacionAceptada: false,
    aprobado: false,
  },
  {
    id: "PED-008",
    producto: "Licuadora Oster 1000W",
    cantidad: 15,
    precio: 219000,
    proveedor: "Alkosto",
    estado: "pendiente",
    rol: "buyer",
    fecha: "2026-03-12",
    cotizacionAceptada: false,
    aprobado: false,
  },
];

// ─── Configuración visual de cada estado ──────────────────────────────────────
const estadoConfig: Record<
  EstadoPedido,
  { label: string; color: string; bg: string; dot: string; border: string }
> = {
  pendiente:   { label: "Pendiente",   color: "text-amber-600",   bg: "bg-amber-50",   dot: "bg-amber-400",   border: "border-amber-200"   },
  en_revision: { label: "En Revisión", color: "text-sky-600",     bg: "bg-sky-50",     dot: "bg-sky-400",     border: "border-sky-200"     },
  aprobado:    { label: "Aprobado",    color: "text-emerald-600", bg: "bg-emerald-50", dot: "bg-emerald-400", border: "border-emerald-200" },
  rechazado:   { label: "Rechazado",   color: "text-rose-600",    bg: "bg-rose-50",    dot: "bg-rose-400",    border: "border-rose-200"    },
  preparando:  { label: "Preparando",  color: "text-violet-600",  bg: "bg-violet-50",  dot: "bg-violet-400",  border: "border-violet-200"  },
  despachado:  { label: "Despachado",  color: "text-cyan-600",    bg: "bg-cyan-50",    dot: "bg-cyan-400",    border: "border-cyan-200"    },
  entregado:   { label: "Entregado",   color: "text-teal-600",    bg: "bg-teal-50",    dot: "bg-teal-400",    border: "border-teal-200"    },
};

// ─── Configuración de roles del proceso ──────────────────────────────────────
const rolConfig: Record<Rol, { label: string; icono: string }> = {
  shipping:   { label: "Oficina de Envíos", icono: "🚚" },
  buyer:      { label: "Agente Comprador",  icono: "🛒" },
  supervisor: { label: "Supervisor",        icono: "👔" },
  seller:     { label: "Vendedor",          icono: "🏪" },
  receiver:   { label: "Agente Receptor",   icono: "📦" },
};

// ─── Pasos del diagrama de flujo del proceso ──────────────────────────────────
const pasosFlujo: { paso: number; nombre: string; rol: Rol; icono: string }[] = [
  { paso: 1, nombre: "Requisición",          rol: "shipping",   icono: "📋" },
  { paso: 2, nombre: "Solicitar Cotización", rol: "buyer",      icono: "📨" },
  { paso: 3, nombre: "Evaluar Cotización",   rol: "supervisor", icono: "🔍" },
  { paso: 4, nombre: "Revisión de Oferta",   rol: "seller",     icono: "📊" },
  { paso: 5, nombre: "Preparar Orden",       rol: "buyer",      icono: "✅" },
  { paso: 6, nombre: "Cumplir Orden",        rol: "seller",     icono: "📦" },
  { paso: 7, nombre: "Recibir Producto",     rol: "receiver",   icono: "🏁" },
];

// ─── Mapa de transiciones de estado según el flujo del diagrama ──────────────
const transiciones: Record<EstadoPedido, EstadoPedido> = {
  pendiente:   "en_revision",
  en_revision: "aprobado",
  aprobado:    "preparando",
  preparando:  "despachado",
  despachado:  "entregado",
  rechazado:   "rechazado",
  entregado:   "entregado",
};

// ─── Componente: Etiqueta de estado ──────────────────────────────────────────
const EtiquetaEstado: React.FC<{ estado: EstadoPedido }> = ({ estado }) => {
  const cfg = estadoConfig[estado];
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${cfg.bg} ${cfg.color} ${cfg.border}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${cfg.dot} animate-pulse`} />
      {cfg.label}
    </span>
  );
};

// ─── Componente: Tarjeta de pedido ───────────────────────────────────────────
const TarjetaPedido: React.FC<{
  pedido: Pedido;
  onAvanzar: (id: string) => void;
  onEliminar: (id: string) => void;
}> = ({ pedido, onAvanzar, onEliminar }) => {
  const rol = rolConfig[pedido.rol];
  const total = pedido.cantidad * pedido.precio;
  const puedeAvanzar = !["entregado", "rechazado"].includes(pedido.estado);

  return (
    <div className="group relative bg-white border border-gray-200 rounded-2xl p-5 hover:border-indigo-300 hover:shadow-lg hover:shadow-indigo-100 transition-all duration-300">
      {/* Franja de color según estado */}
      <div className={`absolute inset-x-0 top-0 h-1 rounded-t-2xl ${estadoConfig[pedido.estado].dot}`} />

      {/* Encabezado de la tarjeta */}
      <div className="flex items-start justify-between mb-4 pt-1">
        <div>
          <p className="text-xs text-gray-400 font-mono mb-1">{pedido.id}</p>
          <h3 className="text-gray-800 font-bold text-sm leading-tight">{pedido.producto}</h3>
        </div>
        <EtiquetaEstado estado={pedido.estado} />
      </div>

      {/* Cuadrícula cantidad / total */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="bg-gray-50 rounded-xl p-3 border border-gray-100">
          <p className="text-gray-400 text-xs mb-1">Cantidad</p>
          <p className="text-gray-800 font-bold text-lg">{pedido.cantidad}</p>
          <p className="text-gray-400 text-xs">unidades</p>
        </div>
        <div className="bg-indigo-50 rounded-xl p-3 border border-indigo-100">
          <p className="text-indigo-400 text-xs mb-1">Total</p>
          <p className="text-indigo-600 font-bold text-base">{formatCOP(total)}</p>
          <p className="text-indigo-300 text-xs">COP</p>
        </div>
      </div>

      {/* Información detallada */}
      <div className="space-y-2 mb-4">
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-400">Proveedor</span>
          <span className="text-gray-700 font-semibold">{pedido.proveedor}</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-400">Precio unitario</span>
          <span className="text-gray-600">{formatCOP(pedido.precio)}</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-400">Fecha</span>
          <span className="text-gray-600">{pedido.fecha}</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-400">Responsable</span>
          <span className="text-gray-600">{rol.icono} {rol.label}</span>
        </div>
      </div>

      {/* Indicadores de verificación */}
      <div className="flex items-center gap-3 mb-4 p-2 bg-gray-50 rounded-xl border border-gray-100">
        <div className={`flex items-center gap-1 text-xs font-medium ${pedido.cotizacionAceptada ? "text-emerald-600" : "text-gray-300"}`}>
          <span>{pedido.cotizacionAceptada ? "✓" : "○"}</span>
          <span>Cotización</span>
        </div>
        <div className="w-px h-3 bg-gray-200" />
        <div className={`flex items-center gap-1 text-xs font-medium ${pedido.aprobado ? "text-emerald-600" : "text-gray-300"}`}>
          <span>{pedido.aprobado ? "✓" : "○"}</span>
          <span>Aprobado</span>
        </div>
      </div>

      {/* Botones de acción */}
      <div className="flex gap-2">
        {puedeAvanzar ? (
          <button
            onClick={() => onAvanzar(pedido.id)}
            className="flex-1 py-2 px-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold transition-all duration-200 hover:shadow-md"
          >
            Avanzar proceso →
          </button>
        ) : (
          <div className="flex-1 py-2 text-center text-xs text-gray-400 font-medium bg-gray-50 rounded-xl border border-gray-100">
            {pedido.estado === "entregado" ? "✅ Proceso completado" : "❌ Pedido rechazado"}
          </div>
        )}
        <button
          onClick={() => onEliminar(pedido.id)}
          title="Eliminar este pedido"
          className="py-2 px-3 bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-500 hover:text-rose-600 rounded-xl text-xs font-semibold transition-all duration-200"
        >
          🗑
        </button>
      </div>
    </div>
  );
};

// ─── Componente: Panel de estadísticas generales ──────────────────────────────
const PanelEstadisticas: React.FC<{ pedidos: Pedido[] }> = ({ pedidos }) => {
  const totalValor = pedidos.reduce((s, p) => s + p.cantidad * p.precio, 0);
  const aprobados  = pedidos.filter((p) => p.aprobado).length;
  const enCurso    = pedidos.filter((p) => !["entregado", "rechazado"].includes(p.estado)).length;
  const entregados = pedidos.filter((p) => p.estado === "entregado").length;

  const tarjetas = [
    { etiqueta: "Total pedidos", valor: String(pedidos.length),                        icono: "📋", acento: "border-l-gray-400",    fondo: "bg-gray-50"    },
    { etiqueta: "Aprobados",     valor: String(aprobados),                              icono: "✅", acento: "border-l-emerald-400", fondo: "bg-emerald-50" },
    { etiqueta: "En curso",      valor: String(enCurso),                               icono: "⚡", acento: "border-l-sky-400",     fondo: "bg-sky-50"     },
    { etiqueta: "Entregados",    valor: String(entregados),                             icono: "🏁", acento: "border-l-teal-400",    fondo: "bg-teal-50"    },
    { etiqueta: "Valor total",   valor: `${(totalValor / 1000000).toFixed(1)}M COP`,   icono: "💰", acento: "border-l-indigo-400",  fondo: "bg-indigo-50"  },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-5 gap-3 mb-8">
      {tarjetas.map((t) => (
        <div key={t.etiqueta} className={`${t.fondo} border border-gray-200 border-l-4 ${t.acento} rounded-2xl p-4`}>
          <div className="text-xl mb-1">{t.icono}</div>
          <p className="text-gray-800 font-bold text-xl">{t.valor}</p>
          <p className="text-gray-500 text-xs mt-0.5">{t.etiqueta}</p>
        </div>
      ))}
    </div>
  );
};

// ─── Componente: Diagrama de flujo del proceso ───────────────────────────────
const DiagramaFlujo: React.FC = () => (
  <div className="bg-white border border-gray-200 rounded-2xl p-6 mb-8 shadow-sm">
    <h2 className="text-gray-800 font-bold text-sm mb-5 flex items-center gap-2">
      <span className="w-2 h-2 rounded-full bg-indigo-500" />
      Diagrama de flujo — Gestión de pedidos en tienda
    </h2>
    <div className="flex items-center gap-1 overflow-x-auto pb-2">
      {pasosFlujo.map((paso, i) => (
        <div key={paso.paso} className="flex items-center gap-1 flex-shrink-0">
          <div className="flex flex-col items-center gap-1">
            <div className="w-12 h-12 rounded-xl bg-indigo-50 border-2 border-indigo-200 flex items-center justify-center text-xl shadow-sm">
              {paso.icono}
            </div>
            <p className="text-gray-600 text-xs text-center max-w-16 leading-tight font-medium">{paso.nombre}</p>
            <span className="text-gray-400 text-xs text-center max-w-16 leading-tight">{rolConfig[paso.rol].label}</span>
          </div>
          {i < pasosFlujo.length - 1 && (
            <div className="flex items-center gap-0.5 mb-8">
              <div className="w-5 h-px bg-indigo-300" />
              <span className="text-indigo-400 text-sm font-bold">›</span>
            </div>
          )}
        </div>
      ))}
    </div>
  </div>
);

// ─── Componente raíz de la aplicación ────────────────────────────────────────
export default function GestionPedidos() {
  const [pedidos, setPedidos]         = useState<Pedido[]>(pedidosIniciales);
  const [filtroEstado, setFiltroEstado] = useState<EstadoPedido | "todos">("todos");
  const [filtroRol, setFiltroRol]     = useState<Rol | "todos">("todos");
  const [busqueda, setBusqueda]       = useState("");
  const [mostrarFlujo, setMostrarFlujo] = useState(true);

  // Avanza el estado de un pedido siguiendo el flujo definido en el diagrama
  const avanzarPedido = (id: string) => {
    setPedidos((prev) =>
      prev.map((p) =>
        p.id !== id ? p : {
          ...p,
          estado: transiciones[p.estado],
          cotizacionAceptada: ["aprobado", "preparando", "despachado", "entregado"].includes(transiciones[p.estado]) || p.cotizacionAceptada,
          aprobado:           ["preparando", "despachado", "entregado"].includes(transiciones[p.estado]) || p.aprobado,
        }
      )
    );
  };

  // Agrega un nuevo pedido vacío al inicio de la lista
  const agregarPedido = () => {
    const nuevo: Pedido = {
      id: `PED-${String(pedidos.length + 1).padStart(3, "0")}`,
      producto: "Nuevo Producto",
      cantidad: 1,
      precio: 150000,
      proveedor: "Éxito",
      estado: "pendiente",
      rol: "buyer",
      fecha: new Date().toISOString().split("T")[0],
      cotizacionAceptada: false,
      aprobado: false,
    };
    setPedidos((prev) => [nuevo, ...prev]);
  };

  // Elimina un pedido de la lista por su identificador
  const eliminarPedido = (id: string) => {
    setPedidos((prev) => prev.filter((p) => p.id !== id));
  };

  // Aplica los filtros activos sobre la lista de pedidos
  const pedidosFiltrados = pedidos.filter((p) => {
    const coincideEstado   = filtroEstado === "todos" || p.estado === filtroEstado;
    const coincideRol      = filtroRol    === "todos" || p.rol    === filtroRol;
    const coincideBusqueda =
      p.producto.toLowerCase().includes(busqueda.toLowerCase()) ||
      p.proveedor.toLowerCase().includes(busqueda.toLowerCase()) ||
      p.id.toLowerCase().includes(busqueda.toLowerCase());
    return coincideEstado && coincideRol && coincideBusqueda;
  });

  return (
    <div className="min-h-screen bg-white" style={{ fontFamily: "'DM Sans', system-ui, sans-serif" }}>

      {/* Barra de navegación superior */}
      <div className="bg-white border-b border-gray-100 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-sm font-bold">G</div>
            <span className="font-bold text-gray-800 text-sm">Gestión de Pedidos</span>
          </div>
          <span className="text-xs text-gray-400 font-mono">{pedidos.length} pedidos en lista</span>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-10">

        {/* Encabezado principal */}
        <div className="flex items-start justify-between mb-10">
          <div>
            <div className="inline-flex items-center gap-2 bg-indigo-50 border border-indigo-200 rounded-full px-3 py-1 mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse" />
              <span className="text-indigo-600 text-xs font-semibold tracking-wider uppercase">Taller de Listas · TypeScript</span>
            </div>
            <h1 className="text-4xl font-black text-gray-900 mb-1">
              Gestión de{" "}
              <span className="bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">
                Pedidos
              </span>
            </h1>
            <p className="text-gray-400 text-sm">
              Elaborado por <span className="text-indigo-500 font-bold">Sebastián</span> 😄
            </p>
          </div>

          {/* Botones principales */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                if (pedidos.length > 0) eliminarPedido(pedidos[0].id);
              }}
              disabled={pedidos.length === 0}
              className="flex items-center gap-2 bg-white hover:bg-rose-50 border border-rose-200 hover:border-rose-300 text-rose-500 hover:text-rose-600 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              🗑️ Eliminar pedido
            </button>
            <button
              onClick={agregarPedido}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 hover:shadow-lg hover:shadow-indigo-200 hover:-translate-y-0.5"
            >
              <span className="text-lg leading-none">+</span> Nuevo pedido
            </button>
          </div>
        </div>

        {/* Panel de estadísticas */}
        <PanelEstadisticas pedidos={pedidos} />

        {/* Botón para mostrar u ocultar el diagrama de flujo */}
        <button
          onClick={() => setMostrarFlujo(!mostrarFlujo)}
          className="flex items-center gap-2 text-gray-500 hover:text-indigo-600 text-sm mb-4 transition-colors font-medium"
        >
          <span
            className="inline-block transition-transform duration-200"
            style={{ transform: mostrarFlujo ? "rotate(90deg)" : "rotate(0deg)" }}
          >
            ›
          </span>
          {mostrarFlujo ? "Ocultar diagrama de flujo" : "Ver diagrama de flujo"}
        </button>

        {mostrarFlujo && <DiagramaFlujo />}

        {/* Barra de filtros y búsqueda */}
        <div className="flex flex-wrap gap-3 mb-6 p-4 bg-gray-50 rounded-2xl border border-gray-100">
          <input
            type="text"
            placeholder="Buscar por producto, proveedor o código..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="bg-white border border-gray-200 rounded-xl px-4 py-2 text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 w-72"
          />

          <select
            value={filtroEstado}
            onChange={(e) => setFiltroEstado(e.target.value as EstadoPedido | "todos")}
            className="bg-white border border-gray-200 rounded-xl px-4 py-2 text-sm text-gray-600 focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
          >
            <option value="todos">Todos los estados</option>
            {Object.entries(estadoConfig).map(([k, v]) => (
              <option key={k} value={k}>{v.label}</option>
            ))}
          </select>

          <select
            value={filtroRol}
            onChange={(e) => setFiltroRol(e.target.value as Rol | "todos")}
            className="bg-white border border-gray-200 rounded-xl px-4 py-2 text-sm text-gray-600 focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
          >
            <option value="todos">Todos los responsables</option>
            {Object.entries(rolConfig).map(([k, v]) => (
              <option key={k} value={k}>{v.icono} {v.label}</option>
            ))}
          </select>

          <div className="ml-auto flex items-center gap-2 text-gray-400 text-sm">
            <span className="font-bold text-indigo-600">{pedidosFiltrados.length}</span>
            <span>pedidos encontrados</span>
          </div>
        </div>

        {/* Cuadrícula de tarjetas de pedidos */}
        {pedidosFiltrados.length === 0 ? (
          <div className="text-center py-24 text-gray-400">
            <p className="text-5xl mb-4">📭</p>
            <p className="font-semibold text-gray-500">No se encontraron pedidos</p>
            <p className="text-sm mt-1">Intenta cambiar los filtros o agrega un nuevo pedido</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {pedidosFiltrados.map((pedido) => (
              <TarjetaPedido
                key={pedido.id}
                pedido={pedido}
                onAvanzar={avanzarPedido}
                onEliminar={eliminarPedido}
              />
            ))}
          </div>
        )}

        {/* Pie de página */}
        <div className="mt-14 pt-6 border-t border-gray-100 flex items-center justify-between text-xs text-gray-300">
          <span>Taller de Listas · TypeScript + React + Tailwind CSS</span>
          <span className="font-mono">Lista&lt;Pedido&gt; · {pedidos.length} elementos</span>
        </div>
      </div>
    </div>
  );
}