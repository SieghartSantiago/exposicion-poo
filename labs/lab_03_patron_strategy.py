import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="medium",
    app_title="Laboratorio POO 03 — Patrón Strategy e Intercambio Dinámico",
    css_file="lab_theme.css",
    html_head_file="lab_head.html",
)


@app.cell(hide_code=True)
def _():
    from dataclasses import dataclass
    from typing import Protocol
    import inspect
    import marimo as mo

    return Protocol, dataclass, inspect, mo


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="poo-lab-banner">
          <div class="poo-lab-nav">
            <div class="poo-badge-row" style="margin-bottom: 0;">
              <span class="poo-chip poo-chip-cyan">Programación I · Unidad VI</span>
              <span class="poo-chip poo-chip-emerald">Patrón Strategy · Composición</span>
            </div>
            <nav class="poo-lab-nav-links" aria-label="Navegación del laboratorio">
              <a class="poo-nav-link" href="../../../index.html">← Presentación</a>
              <a class="poo-nav-link" href="../../../guia/index.html">📱 Guía Móvil</a>
              <a class="poo-nav-link" href="../../01-encapsulamiento/run/index.html">Lab 01</a>
              <a class="poo-nav-link" href="../../02-herencia-polimorfismo/run/index.html">Lab 02</a>
              <a class="poo-nav-link poo-nav-link-active" href="../../03-patron-strategy/run/index.html">Lab 03</a>
              <a class="poo-nav-link" href="../../04-comparacion-paradigmas/run/index.html">Lab 04</a>
              <a class="poo-nav-link" href="../run/index.html">🎛️ Simulador</a>
              <a class="poo-nav-link" href="../edit/index.html">✏️ Editor</a>
            </nav>
          </div>
          <h2 style="margin: 0.15rem 0 0.45rem 0; font-size: 1.28rem; color: #f8fafc;">
            Laboratorio 03: Patrón Strategy e Intercambio de Comportamientos
          </h2>
          <p style="margin: 0; color: #cbd5e1; font-size: 0.91rem; line-height: 1.5;">
            <strong>Problema:</strong> incrustar todas las promociones comerciales dentro de <code>Pedido.calcular_total()</code> mediante ramas <code>if/elif</code> acopla el pedido a reglas cambiantes y dificulta probar cada política por separado.<br/>
            <strong>Solución POO:</strong> extraer la familia de algoritmos tras el contrato <code>EstrategiaDescuento</code> y componer el objeto <code>Pedido</code> con una referencia intercambiable en tiempo de ejecución.<br/>
            <strong>Mejora obtenida:</strong> un mismo pedido puede cambiar de estrategia dinámicamente sin recrearse ni modificar la clase <code>Pedido</code> (Principio Abierto/Cerrado + delegación).
          </p>
        </div>
        """
    )
    return


@app.cell
def _(Protocol, dataclass):
    # ==========================================================================
    # 1. DEFINICIÓN DE CONTRATO DE ESTRATEGIA Y ALGORITMOS INTERCAMBIABLES
    # ==========================================================================

    # Representa un renglón del carrito de compras (ej. 12 unidades a $4500 cada una)
    # frozen=True significa que una vez creado el renglón, sus datos no pueden alterarse por accidente
    @dataclass(frozen=True)
    class LineaPedido:
        producto: str
        precio_unitario: float
        cantidad: int

        # Se ejecuta automáticamente al crear el renglón para validar que precio y cantidad sean > 0
        def __post_init__(self) -> None:
            if self.precio_unitario <= 0.0 or self.cantidad <= 0:
                raise ValueError("Precio unitario y cantidad deben ser mayores a cero.")

        # Calcula el precio total de este renglón (precio * cantidad)
        @property
        def subtotal(self) -> float:
            return self.precio_unitario * self.cantidad

    # --- Caso A (Problema): Función monolítica acoplada con múltiples if/elif ---
    # Aquí todas las promociones viven amontonadas dentro de una sola función.
    # Cada vez que marketing inventa una promoción nueva, hay que tocar esta función.
    def liquidar_pedido_acoplado(
        subtotal: float,
        cantidad_total: int,
        codigo_estrategia: str,
        tope_reintegro: float = 8000.0,
    ) -> float:
        """Cada nueva promoción obliga a editar esta misma rutina condicional."""
        if codigo_estrategia == "regular":
            return subtotal  # Sin descuento
        elif codigo_estrategia == "estudiante":
            return subtotal * 0.85  # Cobra el 85 % (15 % de descuento)
        elif codigo_estrategia == "mayorista":
            # Si lleva 10 o más unidades cobra el 80 % (20 % desc.), si no el 92 % (8 % desc.)
            return subtotal * (0.80 if cantidad_total >= 10 else 0.92)
        elif codigo_estrategia == "reintegro":
            # Descuenta el 25 %, pero con un límite máximo (tope) de devolución
            return subtotal - min(subtotal * 0.25, tope_reintegro)
        raise ValueError(f"Promoción no soportada: {codigo_estrategia}")

    # --- Caso B (Solución POO): Patrón Strategy con Protocol y delegación ---
    # Protocol define un "contrato" o interfaz: cualquier clase que tenga los métodos
    # 'nombre()' y 'calcular_descuento()' sirve como estrategia de descuento,
    # sin siquiera necesitar heredar de una clase padre común.
    class EstrategiaDescuento(Protocol):
        """Contrato estructural: cualquier objeto con estos métodos es una estrategia válida."""

        def nombre(self) -> str: ...

        def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float: ...

    # Estrategia 1: No aplica ningún descuento (devuelve $0 de ahorro)
    class SinDescuento:
        def nombre(self) -> str:
            return "Tarifa Regular (0 %)"

        def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float:
            return 0.0

    # Estrategia 2: Aplica un porcentaje fijo (por defecto 15 % = 0.15) para estudiantes
    class DescuentoEstudiante:
        def __init__(self, porcentaje: float = 0.15) -> None:
            # Validamos que el porcentaje esté en un rango razonable (entre 0 % y 90 %)
            if not (0.0 <= porcentaje <= 0.90):
                raise ValueError("El porcentaje debe estar entre 0 % y 90 %.")
            self._porcentaje = porcentaje

        def nombre(self) -> str:
            return f"Beneficio Estudiante ({self._porcentaje * 100:.0f} %)"

        # Devuelve cuánto dinero se descuenta sobre el subtotal
        def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float:
            return subtotal * self._porcentaje

    # Estrategia 3: Descuento por volumen según la cantidad total de unidades compradas
    class EscalaMayorista:
        """Aplica 20 % desde 10 unidades o 8 % en compras menores."""

        def nombre(self) -> str:
            return "Escala Mayorista (8 % / 20 % desde 10 u.)"

        def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float:
            # Si lleva 10 o más unidades aplica 20 % (0.20); si lleva menos, aplica 8 % (0.08)
            _alicuota = 0.20 if cantidad_total >= 10 else 0.08
            return subtotal * _alicuota

    # Estrategia 4: Reintegro bancario con tope máximo (ej. 25 % de ahorro con tope de $8.000)
    class ReintegroConTope:
        def __init__(self, porcentaje: float = 0.25, tope: float = 8000.0) -> None:
            if tope < 0.0:
                raise ValueError("El tope de reintegro no puede ser negativo.")
            self._porcentaje = porcentaje
            self._tope = tope

        def nombre(self) -> str:
            return f"Promoción Bancaria (25 % con tope ${self._tope:,.0f})"

        def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float:
            # min(...) elige el menor entre el 25 % del subtotal y el tope máximo permitido
            return min(subtotal * self._porcentaje, self._tope)

    return (
        DescuentoEstudiante,
        EscalaMayorista,
        EstrategiaDescuento,
        LineaPedido,
        ReintegroConTope,
        SinDescuento,
        liquidar_pedido_acoplado,
    )


@app.cell
def _(EstrategiaDescuento, LineaPedido):
    # ==========================================================================
    # 2. CLASE CONTEXTO (PEDIDO) QUE DELEGA EL CÁLCULO A LA ESTRATEGIA ACTIVA
    # ==========================================================================

    # La clase Pedido NO tiene ningún 'if/elif' de promociones.
    # En su lugar, guarda un objeto 'estrategia' adentro (composición) y le pide a ese objeto
    # que calcule el descuento cuando hace falta (delegación).
    class Pedido:
        """
        Contexto del patrón Strategy.
        Conserva sus ítems y delega el descuento en self._estrategia.
        """

        def __init__(self, cliente: str, estrategia: EstrategiaDescuento) -> None:
            self._cliente: str = cliente
            self._lineas: list[LineaPedido] = []          # Lista de productos cargados en el pedido
            self._estrategia: EstrategiaDescuento = estrategia  # Estrategia de descuento enchufada

        # Agrega un nuevo producto con su precio y cantidad a la lista del pedido
        def agregar_item(self, producto: str, precio_unitario: float, cantidad: int) -> None:
            self._lineas.append(LineaPedido(producto, precio_unitario, cantidad))

        # Permite cambiar la promoción en cualquier momento sin recrear el pedido ni perder sus productos
        def cambiar_estrategia(self, nueva_estrategia: EstrategiaDescuento) -> None:
            """Permite intercambiar el comportamiento en caliente en tiempo de ejecución."""
            self._estrategia = nueva_estrategia

        # Consulta el nombre de la promoción que está enchufada actualmente
        @property
        def estrategia_actual(self) -> str:
            return self._estrategia.nombre()

        # Suma las unidades de todos los renglones del pedido
        @property
        def cantidad_unidades(self) -> int:
            return sum(linea.cantidad for linea in self._lineas)

        # Suma los subtotales de todos los renglones (total sin descuento)
        @property
        def subtotal_bruto(self) -> float:
            return sum(linea.subtotal for linea in self._lineas)

        # DELEGACIÓN: el pedido no hace la cuenta del descuento por sí mismo,
        # sino que le delega el cálculo a su estrategia activa (self._estrategia)
        def descuento_aplicado(self) -> float:
            return self._estrategia.calcular_descuento(
                self.subtotal_bruto, self.cantidad_unidades
            )

        # Resta el descuento al subtotal bruto (asegurando con max que nunca dé menos de $0)
        def total_neto(self) -> float:
            return max(0.0, self.subtotal_bruto - self.descuento_aplicado())

    return (Pedido,)


@app.cell(hide_code=True)
def _(mo):
    estrategia_ui = mo.ui.dropdown(
        options={
            "Beneficio Estudiante (15 %)": "estudiante",
            "Escala Mayorista (8 % o 20 % desde 10 unidades)": "mayorista",
            "Promoción Bancaria (25 % con tope configurable)": "reintegro",
            "Tarifa Regular (0 % sin descuento)": "regular",
        },
        value="Beneficio Estudiante (15 %)",
        label="Estrategia inyectada en `Pedido`",
        full_width=True,
    )

    precio_ui = mo.ui.slider(
        start=1500,
        stop=15000,
        step=500,
        value=4500,
        label="Precio unitario del artículo ($)",
        full_width=True,
    )

    cantidad_ui = mo.ui.slider(
        start=1,
        stop=25,
        step=1,
        value=12,
        label="Cantidad de unidades en el pedido",
        full_width=True,
    )

    tope_ui = mo.ui.slider(
        start=2000,
        stop=20000,
        step=1000,
        value=8000,
        label="Tope máximo de reintegro bancario ($)",
        full_width=True,
    )

    mo.vstack(
        [
            mo.md("### Controles de Simulación e Intercambio de Estrategia"),
            estrategia_ui,
            precio_ui,
            cantidad_ui,
            tope_ui,
        ],
        gap=0.65,
    )
    return cantidad_ui, estrategia_ui, precio_ui, tope_ui


@app.cell(hide_code=True)
def _(
    DescuentoEstudiante,
    EscalaMayorista,
    EstrategiaDescuento,
    Pedido,
    ReintegroConTope,
    SinDescuento,
    cantidad_ui,
    estrategia_ui,
    inspect,
    mo,
    precio_ui,
    tope_ui,
):
    # ==========================================================================
    # 3. BLOQUE DE PRESENTACIÓN: SUSTITUCIÓN EN VIVO SOBRE LA MISMA INSTANCIA
    # ==========================================================================
    _catalogo: dict[str, EstrategiaDescuento] = {
        "regular": SinDescuento(),
        "estudiante": DescuentoEstudiante(0.15),
        "mayorista": EscalaMayorista(),
        "reintegro": ReintegroConTope(0.25, float(tope_ui.value)),
    }

    _pedido = Pedido("Comisión Programación I", _catalogo[estrategia_ui.value])
    _pedido.agregar_item(
        "Licencia Kit Laboratorio", float(precio_ui.value), int(cantidad_ui.value)
    )

    _bruto = _pedido.subtotal_bruto
    _desc_activo = _pedido.descuento_aplicado()
    _neto_activo = _pedido.total_neto()
    _nombre_activo = _pedido.estrategia_actual
    _id_pedido = hex(id(_pedido))

    # Evaluar todas las estrategias sobre la MISMA instancia cambiando estrategia en caliente
    _comparativa_filas = ""
    for _clave, _est in _catalogo.items():
        _pedido.cambiar_estrategia(_est)
        _es_activa = _clave == estrategia_ui.value
        _estilo = "background: rgba(56, 189, 248, 0.12);" if _es_activa else ""
        _marca = " ◀ activa" if _es_activa else ""
        _comparativa_filas += f"""
        <tr style="{_estilo}">
          <td><strong>{_pedido.estrategia_actual}</strong>{_marca}</td>
          <td style="font-family: JetBrains Mono, monospace; color: #fda4af;">-${_pedido.descuento_aplicado():,.2f}</td>
          <td style="font-family: JetBrains Mono, monospace; font-weight: 700; color: #34d399;">${_pedido.total_neto():,.2f}</td>
        </tr>
        """

    _salida = mo.Html(
        f"""
        <div class="poo-grid-2">
          <div class="poo-card">
            <div class="poo-badge-row">
              <span class="poo-chip poo-chip-cyan">Contexto Pedido ({_id_pedido})</span>
            </div>
            <h4 style="margin: 0.2rem 0; color: #f8fafc;">Estado del <code>Pedido</code></h4>
            <div class="poo-metric" style="color: #e2e8f0;">
              Subtotal Bruto = ${_bruto:,.2f}
            </div>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin: 0;">
              Unidades totales: <code>{_pedido.cantidad_unidades}</code> · Precio unitario: <code>${float(precio_ui.value):,.2f}</code>
            </p>
          </div>

          <div class="poo-card poo-card-valid">
            <div class="poo-badge-row">
              <span class="poo-chip poo-chip-emerald">Estrategia Delegada</span>
            </div>
            <h4 style="margin: 0.2rem 0; color: #6ee7b7;">{_nombre_activo}</h4>
            <div class="poo-metric" style="color: #34d399;">
              Total Neto = ${_neto_activo:,.2f}
            </div>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin: 0;">
              Ahorro calculado por el objeto colaborador: <code>-${_desc_activo:,.2f}</code>
            </p>
          </div>
        </div>

        <div class="poo-table-wrap">
          <table class="poo-table">
            <thead>
              <tr>
                <th>Intercambio dinámico sobre el mismo <code>Pedido</code></th>
                <th>Descuento Delegado</th>
                <th>Total Final</th>
              </tr>
            </thead>
            <tbody>
              {_comparativa_filas}
            </tbody>
          </table>
        </div>

        <div class="poo-guide-box">
          <strong>Guía de observación:</strong> la tabla se construye llamando a <code>pedido.cambiar_estrategia(...)</code> cuatro veces sobre la <strong>misma instancia</strong> de <code>Pedido</code> (<code>id={_id_pedido}</code>). Esto demuestra composición y delegación en tiempo de ejecución sin usar herencia para cada combinación comercial.
        </div>
        """
    )

    _codigo_strategy = "\n".join(
        [
            "# ==========================================================================",
            "# 1. CONTRATO ESTRUCTURAL (PROTOCOL) Y ESTRATEGIAS CONCRETAS",
            "# ==========================================================================",
            "# Protocol define un 'contrato': cualquier clase que implemente los métodos",
            "# 'nombre' y 'calcular_descuento' puede enchufarse dentro de un Pedido.",
            "class EstrategiaDescuento(Protocol):",
            '    """Contrato estructural: cualquier objeto con estos métodos es una estrategia válida."""',
            "",
            "    def nombre(self) -> str: ...",
            "",
            "    def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float: ...",
            "",
            "",
            "# Estrategia 1: sin promoción (el descuento es $0)",
            "class SinDescuento:",
            "    def nombre(self) -> str:",
            '        return "Tarifa Regular (0 %)"',
            "",
            "    def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float:",
            "        return 0.0",
            "",
            "",
            "# Estrategia 2: descuento porcentual fijo para estudiantes (por defecto 15 % = 0.15)",
            "class DescuentoEstudiante:",
            "    def __init__(self, porcentaje: float = 0.15) -> None:",
            "        # Validamos que el porcentaje esté entre 0 % y 90 %",
            "        if not (0.0 <= porcentaje <= 0.90):",
            '            raise ValueError("El porcentaje debe estar entre 0 % y 90 %.")',
            "        self._porcentaje = porcentaje",
            "",
            "    def nombre(self) -> str:",
            '        return f"Beneficio Estudiante ({self._porcentaje * 100:.0f} %)"',
            "",
            "    # Multiplica el subtotal por el porcentaje de beneficio",
            "    def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float:",
            "        return subtotal * self._porcentaje",
            "",
            "",
            "# Estrategia 3: descuento por cantidad de unidades (20 % desde 10 unidades, o 8 % si son menos)",
            "class EscalaMayorista:",
            "    def nombre(self) -> str:",
            '        return "Escala Mayorista (8 % / 20 % desde 10 u.)"',
            "",
            "    def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float:",
            "        # Elige 20 % (0.20) si supera o iguala 10 unidades; de lo contrario aplica 8 % (0.08)",
            "        alicuota = 0.20 if cantidad_total >= 10 else 0.08",
            "        return subtotal * alicuota",
            "",
            "",
            "# Estrategia 4: promoción bancaria del 25 % pero con un tope máximo de dinero a devolver",
            "class ReintegroConTope:",
            "    def __init__(self, porcentaje: float = 0.25, tope: float = 8000.0) -> None:",
            "        if tope < 0.0:",
            '            raise ValueError("El tope de reintegro no puede ser negativo.")',
            "        self._porcentaje = porcentaje",
            "        self._tope = tope  # Límite máximo de ahorro en pesos",
            "",
            "    def nombre(self) -> str:",
            '        return f"Promoción Bancaria (25 % con tope ${self._tope:,.0f})"',
            "",
            "    # min(...) devuelve el menor valor entre el 25 % calculado y el tope permitido",
            "    def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float:",
            "        return min(subtotal * self._porcentaje, self._tope)",
            "",
            "",
            "# ==========================================================================",
            "# 2. CLASE CONTEXTO (PEDIDO) CON COMPOSICIÓN Y DELEGACIÓN",
            "# ==========================================================================",
            "# Pedido NO tiene bloques if/elif para calcular descuentos:",
            "# guarda un objeto estrategia en 'self._estrategia' y le delega el cálculo.",
            "class Pedido:",
            '    """Contexto del patrón Strategy: delega el descuento en self._estrategia."""',
            "",
            "    def __init__(self, cliente: str, estrategia: EstrategiaDescuento) -> None:",
            "        self._cliente: str = cliente",
            "        self._lineas: list[LineaPedido] = []                # Lista de productos del carrito",
            "        self._estrategia: EstrategiaDescuento = estrategia  # Estrategia activa enchufada",
            "",
            "    # Agrega un producto con su precio y cantidad al carrito",
            "    def agregar_item(self, producto: str, precio_unitario: float, cantidad: int) -> None:",
            "        self._lineas.append(LineaPedido(producto, precio_unitario, cantidad))",
            "",
            "    # Permite reemplazar la estrategia en vivo sin modificar ni recrear el pedido",
            "    def cambiar_estrategia(self, nueva_estrategia: EstrategiaDescuento) -> None:",
            '        """Intercambia el algoritmo en caliente en tiempo de ejecución."""',
            "        self._estrategia = nueva_estrategia",
            "",
            "    @property",
            "    def estrategia_actual(self) -> str:",
            "        return self._estrategia.nombre()  # Pregunta el nombre a la estrategia actual",
            "",
            "    @property",
            "    def cantidad_unidades(self) -> int:",
            "        return sum(linea.cantidad for linea in self._lineas)  # Suma todas las unidades",
            "",
            "    @property",
            "    def subtotal_bruto(self) -> float:",
            "        return sum(linea.subtotal for linea in self._lineas)  # Suma el total sin descuento",
            "",
            "    # Delegación: el pedido le pide a su estrategia interna que calcule el descuento",
            "    def descuento_aplicado(self) -> float:",
            "        return self._estrategia.calcular_descuento(",
            "            self.subtotal_bruto, self.cantidad_unidades",
            "        )",
            "",
            "    # Calcula el total final a pagar restando el descuento al subtotal bruto",
            "    def total_neto(self) -> float:",
            "        return max(0.0, self.subtotal_bruto - self.descuento_aplicado())",
        ]
    )

    _acordeon = mo.accordion(
        {
            "Ver código completo del contrato `Protocol` y la clase `Pedido`": mo.md(
                f"```python\n{_codigo_strategy}\n```"
            )
        }
    )

    mo.vstack([_salida, _acordeon], gap=0.9)
    return


@app.cell
def _(Pedido, SinDescuento, mo):
    # ==========================================================================
    # 4. ZONA DE EXPERIMENTACIÓN ABIERTA (MODO SANDBOX EDITABLE)
    # ==========================================================================
    class DescuentoDocenteInvestigador:
        """Nueva estrategia creada sin heredar ni modificar la clase Pedido."""

        def nombre(self) -> str:
            return "Convenio Docente / Investigador (18 %)"

        def calcular_descuento(self, subtotal: float, cantidad_total: int) -> float:
            return subtotal * 0.18

    pedido_sandbox = Pedido("Grupo TP POO", SinDescuento())
    pedido_sandbox.agregar_item("Bibliografía Técnica", 20000.0, 2)
    total_inicial_sbx = pedido_sandbox.total_neto()

    # Intercambiamos la estrategia en tiempo de ejecución:
    pedido_sandbox.cambiar_estrategia(DescuentoDocenteInvestigador())
    total_con_estrategia_sbx = pedido_sandbox.total_neto()

    mo.md(
        f"""
        #### Celda de prueba rápida (editable en Modo Editor)
        - **Antes del cambio (`SinDescuento`):** `${total_inicial_sbx:,.2f}`
        - **Después de `cambiar_estrategia(DescuentoDocenteInvestigador())`:** `${total_con_estrategia_sbx:,.2f}`
        """
    )
    return (
        DescuentoDocenteInvestigador,
        pedido_sandbox,
        total_con_estrategia_sbx,
        total_inicial_sbx,
    )


if __name__ == "__main__":
    app.run()
