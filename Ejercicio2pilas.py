"""
SISTEMA DE DESPACHO Y FACTURACION - Si el cliente quiere un producto que esta bloqueado por otros, 
se le cobra el bloqueador antes de llegar al producto deseado.
Si el cliente acepta mover los productos porque estan al fondo de la de la bodega se aplica el metodo PILA. 
"""
"""
CODIGO ELABORADO POR: JOHN SEBASTIAN CORAL UNIGARRO
"""

# ─────────────────────────────────────────────
#  CLASE PRODUCTO
# ─────────────────────────────────────────────
class Product:
    TAX_RATE = 0.19  

    def __init__(self, name: str, base_price: float, weight_kg: float):
        self.name        = name
        self.base_price  = base_price
        self.weight_kg   = weight_kg

    def get_final_price(self) -> float:
        """Retorna el precio con IVA incluido."""
        return self.base_price * (1 + self.TAX_RATE)

    def get_tax(self) -> float:
        """Retorna solo el valor del IVA."""
        return self.base_price * self.TAX_RATE

    def __repr__(self):
        return (f"Product({self.name!r}, "
                f"base=${self.base_price:.2f}, "
                f"final=${self.get_final_price():.2f})")


# ─────────────────────────────────────────────
#  CLASE WAREHOUSE - la pila con logica de cobro
# ─────────────────────────────────────────────
class Warehouse:
    def __init__(self, warehouse_name: str = "bodega de construcción"):
        self.warehouse_name  = warehouse_name
        self._stack: list[Product] = []   # el fondo es el indice 0, el tope es el ultimo
        self.net_total       = 0.0        # suma de precios base despachados
        self.tax_total       = 0.0        # suma del IVA acumulado
        self._receipt: list[dict] = []    # registro de items para la factura final

    # ── CARGA ──────────────────────────────────
    def push(self, product: Product, quantity: int = 1):
        """Apila N unidades de un producto en la pila."""
        for _ in range(quantity):
            self._stack.append(product)
        print(f"  Stacked  ->  {quantity}x {product.name} "
              f"(base price: ${product.base_price:,.0f} each)")

    # ── CONSULTA ───────────────────────────────
    def peek(self) -> Product | None:
        """Mira que hay en el tope sin retirar el elemento."""
        return self._stack[-1] if self._stack else None

    def is_empty(self) -> bool:
        """Verifica si la pila esta vacia."""
        return len(self._stack) == 0

    def show_status(self):
        """Imprime el estado actual de la pila, de arriba hacia abajo."""
        print(f"\n{'-'*45}")
        print(f"  Warehouse status: {self.warehouse_name}")
        print(f"{'-'*45}")
        if self.is_empty():
            print("  The warehouse is empty.")
        else:
            for i, product in enumerate(reversed(self._stack)):
                # el primer elemento de la lista invertida es el tope
                level = "^ TOP" if i == 0 else f"  {i}"
                print(f"  [{level}]  {product.name}  --  ${product.base_price:,.0f} + TAX")
        print(f"{'-'*45}")

    # ── DESPACHO INTELIGENTE ───────────────────
    def dispatch(self, desired_product: str, desired_quantity: int):
        """
        El cliente pide N unidades de un producto especifico.
        Si hay productos bloqueando el acceso, se avisa al cliente
        y se cobran obligatoriamente antes de llegar al producto deseado.
        """
        print(f"\n{'='*45}")
        print(f"  ORDER: {desired_quantity}x {desired_product}")
        print(f"{'='*45}")

        if self.is_empty():
            print("  WARNING: The warehouse is empty. Nothing to dispatch.")
            return

        # 1. Identificar cuantos productos bloquean el acceso al producto deseado
        blockers = []
        target_found = []   # posiciones del producto deseado desde el tope

        # invertimos la lista para recorrer de tope a fondo
        reversed_stack = list(reversed(self._stack))

        found = 0
        for i, product in enumerate(reversed_stack):
            if product.name == desired_product and found < desired_quantity:
                target_found.append(i)
                found += 1
                if found == desired_quantity:
                    break
            elif not target_found:
                # aun no hemos encontrado el primer objetivo, este es un bloqueante
                blockers.append(product)

        # verificar si hay suficientes unidades del producto pedido
        if found < desired_quantity:
            print(f"  WARNING: Only {found} unit(s) of '{desired_product}' "
                  f"available in warehouse (requested {desired_quantity}).")
            if found == 0:
                return

        # 2. Avisar al cliente sobre los productos que bloquean el acceso
        if blockers:
            print(f"\n  CONFLICTO DE PASILLO:")
            print(f"  para alcanzar '{desired_product}', Los siguientes elementos deben ser")
            print(f"  Se eliminará primero (y se agregará a su factura):\n")

            # contar cuantos de cada producto bloquean el acceso
            blocker_count: dict[str, int] = {}
            for b in blockers:
                blocker_count[b.name] = blocker_count.get(b.name, 0) + 1

            for name, qty in blocker_count.items():
                price_ref = next(b for b in blockers if b.name == name)
                print(f"     * {qty}x {name}  ->  "
                      f"${price_ref.get_final_price():,.0f} each (with TAX)")

            # pedir confirmacion al cliente antes de proceder
            confirm = input("\n  ¿El cliente acepta pagar los bloqueadores? (s/n) (y/n): ").strip().lower()
            if confirm != 'y':
                print("  Operation cancelled by the customer.")
                return

        # 3. Despachar todos los items hasta llegar a las unidades pedidas
        items_to_dispatch = len(blockers) + desired_quantity
        print(f"\n  DISPATCHING {items_to_dispatch} ITEM(S):\n")

        for _ in range(items_to_dispatch):
            if self.is_empty():
                break

            # extraer el elemento del tope de la pila
            item = self._stack.pop()
            final_price = item.get_final_price()
            tax_amount  = item.get_tax()

            # acumular totales de la factura
            self.net_total  += item.base_price
            self.tax_total  += tax_amount
            self._receipt.append({
                "name":       item.name,
                "base_price": item.base_price,
                "tax":        tax_amount,
                "total":      final_price,
            })

            # marcar si el item es parte del pedido o una maniobra obligatoria
            item_type = "MANEUVER" if item.name != desired_product else "ORDER   "
            print(f"  [{item_type}]  {item.name:22s}  "
                  f"Base: ${item.base_price:>10,.0f}  |  "
                  f"TAX: ${tax_amount:>10,.0f}  |  "
                  f"Total: ${final_price:>10,.0f}")

    # ── FACTURA FINAL ──────────────────────────
    def print_receipt(self):
        """Imprime el ticket de cierre con el desglose completo de la factura."""
        print(f"\n{'='*68}")
        print(f"  INVOICE  --  {self.warehouse_name}")
        print(f"{'='*68}")
        print(f"  {'PRODUCT':<24} {'BASE PRICE':>12}  {'TAX (19%)':>12}  {'TOTAL':>12}")
        print(f"  {'-'*62}")
        for item in self._receipt:
            print(f"  {item['name']:<24} "
                  f"${item['base_price']:>11,.0f}  "
                  f"${item['tax']:>11,.0f}  "
                  f"${item['total']:>11,.0f}")
        print(f"  {'-'*62}")
        grand_total = self.net_total + self.tax_total
        print(f"  {'NET SUBTOTAL':<24} ${self.net_total:>11,.0f}")
        print(f"  {'TOTAL TAX':<24} ${self.tax_total:>11,.0f}")
        print(f"  {'-'*62}")
        print(f"  {'TOTAL TO PAY':<24} ${grand_total:>11,.0f}")
        print(f"{'='*68}\n")


# ─────────────────────────────────────────────
#  EJECUCION  -  Caso de estudio completo
# ─────────────────────────────────────────────
if __name__ == "__main__":

    # ─────────────────────────────────────────
    #  CATALOGO DE PRODUCTOS (bodega real)
    #  nombre del producto     precio_base   peso_kg
    # ─────────────────────────────────────────
    cement        = Product("Cemento 50kg",         28_500,  50.0)
    lime          = Product("Cal Hidratada 25kg",   12_800,  25.0)
    brick         = Product("Ladrillo Tolete",          350,   2.8)  # precio por unidad
    rebar         = Product("Varilla 1/2\" x6m",    18_900,   9.0)
    sand          = Product("Arena de Rio (bulto)",  8_500,  40.0)
    gravel        = Product("Gravilla (bulto)",      9_200,  40.0)
    block         = Product("Bloque #5",             1_650,   8.5)
    zinc_roof     = Product("Teja Zinc Cal. 26",    32_000,   4.2)
    wire_mesh     = Product("Malla Electrosoldada", 45_000,  15.0)
    nail          = Product("Puntilla 2\" (lb)",     2_100,   0.5)

    # ─────────────────────────────────────────
    #  CREAR BODEGA Y CARGAR EL PASILLO
    #  el primer producto apilado queda en el fondo del pasillo
    # ─────────────────────────────────────────
    warehouse = Warehouse("bodega de construccion Central")

    print("\n  LOADING WAREHOUSE (stack order: bottom -> top):\n")
    warehouse.push(cement,    quantity=8)
    warehouse.push(sand,      quantity=6)
    warehouse.push(gravel,    quantity=4)
    warehouse.push(rebar,     quantity=5)
    warehouse.push(brick,     quantity=10)
    warehouse.push(block,     quantity=6)
    warehouse.push(lime,      quantity=3)
    warehouse.push(zinc_roof, quantity=4)
    warehouse.push(wire_mesh, quantity=2)
    warehouse.push(nail,      quantity=3)   # tope de la pila - el mas facil de sacar

    # ─────────────────────────────────────────
    #  ESTADO INICIAL DE LA BODEGA
    # ─────────────────────────────────────────
    warehouse.show_status()

    # ─────────────────────────────────────────
    #  EL CLIENTE PIDE CEMENTO (esta en el fondo)
    # ─────────────────────────────────────────
    warehouse.dispatch(desired_product="Cemento 50kg", desired_quantity=3)

    # ─────────────────────────────────────────
    #  ESTADO FINAL Y TICKET DE FACTURA
    # ─────────────────────────────────────────
    warehouse.show_status()
    warehouse.print_receipt()