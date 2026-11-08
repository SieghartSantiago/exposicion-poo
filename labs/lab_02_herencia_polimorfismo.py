import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="medium",
    app_title="Laboratorio POO 02 — Clases, Herencia y Polimorfismo",
    css_file="lab_theme.css",
    html_head_file="lab_head.html",
)


@app.cell(hide_code=True)
def _():
    from abc import ABC, abstractmethod
    from dataclasses import dataclass
    import inspect
    import marimo as mo

    return ABC, abstractmethod, dataclass, inspect, mo


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="poo-lab-banner">
          <div class="poo-lab-nav">
            <div class="poo-badge-row" style="margin-bottom: 0;">
              <span class="poo-chip poo-chip-cyan">Programación I · Unidad VI</span>
              <span class="poo-chip poo-chip-indigo">Herencia y Despacho Dinámico</span>
            </div>
            <nav class="poo-lab-nav-links" aria-label="Navegación del laboratorio">
              <a class="poo-nav-link" href="../../../index.html">← Presentación</a>
              <a class="poo-nav-link" href="../../../guia/index.html">📱 Guía Móvil</a>
              <a class="poo-nav-link" href="../../01-encapsulamiento/run/index.html">Lab 01</a>
              <a class="poo-nav-link poo-nav-link-active" href="../../02-herencia-polimorfismo/run/index.html">Lab 02</a>
              <a class="poo-nav-link" href="../../03-patron-strategy/run/index.html">Lab 03</a>
              <a class="poo-nav-link" href="../../04-comparacion-paradigmas/run/index.html">Lab 04</a>
              <a class="poo-nav-link" href="../run/index.html">🎛️ Simulador</a>
              <a class="poo-nav-link" href="../edit/index.html">✏️ Editor</a>
            </nav>
          </div>
          <h2 style="margin: 0.15rem 0 0.45rem 0; font-size: 1.28rem; color: #f8fafc;">
            Laboratorio 02: Clases, Herencia y Despacho Dinámico
          </h2>
          <p style="margin: 0; color: #cbd5e1; font-size: 0.91rem; line-height: 1.5;">
            <strong>Problema:</strong> centralizar el cálculo de tarifas logísticas con bloques <code>if/elif tipo == ...</code> obliga a modificar y volver a probar la función principal cada vez que aparece una nueva modalidad de envío.<br/>
            <strong>Solución POO:</strong> definir el contrato abstracto <code>Envio</code> y especializar subclases cohesivas (<code>EnvioEstandar</code>, <code>EnvioExpres</code>, <code>EnvioRefrigerado</code>) invocadas mediante <strong>despacho dinámico</strong>.<br/>
            <strong>Mejora obtenida:</strong> el procesador del lote recorre cualquier colección heterogénea de envíos sin conocer sus clases concretas, permitiendo agregar nuevas modalidades sin alterar el código cliente.
          </p>
        </div>
        """
    )
    return


@app.cell
def _(ABC, abstractmethod):
    # ==========================================================================
    # 1. DEFINICIÓN DE CLASES, JERARQUÍA Y ENFOQUE CONDICIONAL RÍGIDO
    # ==========================================================================

    # --- Caso A (Problema): Función acoplada a todos los tipos concretos ---
    # Aquí una sola función intenta conocer y calcular TODAS las modalidades de envío.
    # Si mañana la empresa agrega "EnvioMaritimo", hay que abrir y modificar esta función.
    def cotizar_con_condicionales(
        modalidad: str,
        peso_kg: float,
        distancia_km: float,
        recargo_frio: float = 0.0,
    ) -> float:
        """Estructura condicional rígida: crece y se acopla ante cada nuevo tipo."""
        if modalidad == "estandar":
            # Tarifa base $2500 + $420 por kg + $18 por km
            return 2500.0 + peso_kg * 420.0 + distancia_km * 18.0
        elif modalidad == "expres":
            # Tarifa rápida con un 20 % de recargo por urgencia (* 1.20)
            return (3800.0 + peso_kg * 550.0 + distancia_km * 32.0) * 1.20
        elif modalidad == "refrigerado":
            # Tarifa especial que suma un costo extra por mantener la cadena de frío
            return 4600.0 + peso_kg * 600.0 + distancia_km * 28.0 + recargo_frio
        # Si alguien pasa un tipo no previsto, el programa falla
        raise ValueError(f"Modalidad desconocida en if/elif: {modalidad}")

    # --- Caso B (Solución POO): Jerarquía con contrato común y despacho dinámico ---
    # Envio hereda de ABC (Abstract Base Class = Clase Base Abstracta).
    # Funciona como una "plantilla general": define qué datos y métodos tiene cualquier envío,
    # pero delega la fórmula del precio a cada tipo de envío específico (subclases).
    class Envio(ABC):
        """
        Clase base abstracta que define el contrato de todo envío logístico.
        Invariante (regla de validez): peso_kg > 0 y distancia_km > 0.
        """

        # Constructor común para todos los envíos: guarda código, peso y distancia
        def __init__(self, codigo: str, peso_kg: float, distancia_km: float) -> None:
            # Validamos que ningún paquete tenga peso o distancia cero o negativa
            if peso_kg <= 0.0 or distancia_km <= 0.0:
                raise ValueError("Peso y distancia deben ser estrictamente positivos.")
            # Guardamos los datos protegidos con guion bajo (_) dentro del objeto
            self._codigo: str = codigo
            self._peso_kg: float = float(peso_kg)
            self._distancia_km: float = float(distancia_km)

        # Propiedades (@property) para poder consultar los datos sin permitir sobrescribirlos
        @property
        def codigo(self) -> str:
            return self._codigo

        @property
        def peso_kg(self) -> float:
            return self._peso_kg

        @property
        def distancia_km(self) -> float:
            return self._distancia_km

        # @abstractmethod significa "método obligatorio":
        # obliga a que cada subclase (Estándar, Exprés, Refrigerado) escriba su propia versión.
        @abstractmethod
        def modalidad(self) -> str:
            """Nombre legible de la modalidad concreta."""

        @abstractmethod
        def calcular_costo(self) -> float:
            """Cada subtipo calcula su tarifa preservando el contrato común."""

    # Subclase 1: EnvioEstandar "hereda" de Envio (recibe código, peso y distancia automáticamente)
    class EnvioEstandar(Envio):
        """Especialización terrestre estándar."""

        # Cumple el contrato indicando el nombre de su modalidad
        def modalidad(self) -> str:
            return "Terrestre Estándar"

        # Cumple el contrato aplicando la fórmula de costo del envío terrestre común
        def calcular_costo(self) -> float:
            return 2500.0 + self.peso_kg * 420.0 + self.distancia_km * 18.0

    # Subclase 2: EnvioExpres también hereda de Envio, pero agrega un dato propio (factor_urgencia)
    class EnvioExpres(Envio):
        """Especialización prioritaria en 24 h con factor de urgencia."""

        def __init__(
            self,
            codigo: str,
            peso_kg: float,
            distancia_km: float,
            factor_urgencia: float = 1.20,
        ) -> None:
            # super().__init__(...) llama al constructor de la clase padre (Envio)
            # para reutilizar la validación y el guardado de código, peso y distancia
            super().__init__(codigo, peso_kg, distancia_km)
            # Además validamos el dato exclusivo de los envíos exprés
            if factor_urgencia < 1.0:
                raise ValueError("El factor de urgencia no puede ser menor a 1.0.")
            self._factor_urgencia = factor_urgencia

        def modalidad(self) -> str:
            return "Aéreo Exprés 24h"

        # Calcula su costo base y lo multiplica por el recargo de urgencia (ej. 1.20 = +20 %)
        def calcular_costo(self) -> float:
            _base = 3800.0 + self.peso_kg * 550.0 + self.distancia_km * 32.0
            return _base * self._factor_urgencia

    # Subclase 3: EnvioRefrigerado hereda de Envio y agrega la temperatura requerida
    class EnvioRefrigerado(Envio):
        """Especialización con control térmico activo (cadena de frío)."""

        def __init__(
            self,
            codigo: str,
            peso_kg: float,
            distancia_km: float,
            temperatura_c: float = 4.0,
        ) -> None:
            # Reutilizamos la inicialización de la clase base Envio
            super().__init__(codigo, peso_kg, distancia_km)
            # Guardamos la temperatura requerida para este envío refrigerado
            self._temperatura_c = temperatura_c

        def modalidad(self) -> str:
            return f"Cadena de Frío ({self._temperatura_c:.1f} °C)"

        # Calcula el costo sumando un plus mayor si requiere ultracongelado (<= 0 °C)
        def calcular_costo(self) -> float:
            _recargo_termico = 3200.0 if self._temperatura_c <= 0.0 else 1800.0
            return (
                4600.0
                + self.peso_kg * 600.0
                + self.distancia_km * 28.0
                + _recargo_termico
            )

    return (
        Envio,
        EnvioEstandar,
        EnvioExpres,
        EnvioRefrigerado,
        cotizar_con_condicionales,
    )


@app.cell
def _(Envio, dataclass):
    # ==========================================================================
    # 2. BLOQUE DE CONTROL DE FLUJO POLIMÓRFICO (DESPACHO DINÁMICO)
    # ==========================================================================

    # Estructura de datos simple para guardar el detalle de cada fila de la tabla visual
    @dataclass(frozen=True)
    class RegistroDespacho:
        codigo: str
        clase_concreta: str
        metodo_invocado: str
        modalidad: str
        costo: float
        id_instancia: str

    def procesar_lote_envios(lote: list[Envio]) -> tuple[list[RegistroDespacho], float]:
        """
        Procesa cualquier lista de subtipos de Envio sin ningún if/elif ni isinstance.
        Python resuelve _envio.calcular_costo() en tiempo de ejecución (late binding).
        """
        _registros: list[RegistroDespacho] = []  # Lista donde guardaremos el resultado de cada envío
        _total = 0.0                             # Acumulador para sumar la facturación total del lote

        # Recorremos cada objeto del lote sin importar si es Estándar, Exprés o Refrigerado
        for _envio in lote:
            # ¡MAGIA DEL POLIMORFISMO! Llamamos siempre al mismo método calcular_costo().
            # Python detecta automáticamente de qué clase es '_envio' y ejecuta su fórmula correspondiente.
            _costo = _envio.calcular_costo()
            _total += _costo
            # Obtenemos el nombre de la clase concreta (ej. "EnvioExpres") solo para mostrarlo en la tabla
            _clase = type(_envio).__name__
            _registros.append(
                RegistroDespacho(
                    codigo=_envio.codigo,
                    clase_concreta=_clase,
                    metodo_invocado=f"{_clase}.calcular_costo(self)",
                    modalidad=_envio.modalidad(),
                    costo=_costo,
                    id_instancia=hex(id(_envio)),
                )
            )
        return _registros, _total

    return RegistroDespacho, procesar_lote_envios


@app.cell(hide_code=True)
def _(mo):
    peso_ui = mo.ui.slider(
        start=1,
        stop=40,
        step=1,
        value=8,
        label="Peso del paquete (kg)",
        full_width=True,
    )

    distancia_ui = mo.ui.slider(
        start=20,
        stop=1200,
        step=20,
        value=300,
        label="Distancia de recorrido (km)",
        full_width=True,
    )

    congelado_ui = mo.ui.switch(
        value=False,
        label="Requerir ultracongelado (-18 °C) en envío refrigerado",
    )

    incluir_segundo_estandar_ui = mo.ui.switch(
        value=True,
        label="Agregar segunda instancia `EnvioEstandar` independiente (doble peso)",
    )

    mo.vstack(
        [
            mo.md("### Parámetros del Lote Heterogéneo de Objetos"),
            peso_ui,
            distancia_ui,
            congelado_ui,
            incluir_segundo_estandar_ui,
        ],
        gap=0.65,
    )
    return congelado_ui, distancia_ui, incluir_segundo_estandar_ui, peso_ui


@app.cell(hide_code=True)
def _(
    Envio,
    EnvioEstandar,
    EnvioExpres,
    EnvioRefrigerado,
    congelado_ui,
    distancia_ui,
    incluir_segundo_estandar_ui,
    inspect,
    mo,
    peso_ui,
    procesar_lote_envios,
):
    # ==========================================================================
    # 3. BLOQUE DE PRESENTACIÓN Y TRAZA DE DESPACHO DINÁMICO
    # ==========================================================================
    _peso = float(peso_ui.value)
    _dist = float(distancia_ui.value)
    _temp = -18.0 if congelado_ui.value else 4.0

    _lote: list[Envio] = [
        EnvioEstandar("ENV-101", peso_kg=_peso, distancia_km=_dist),
        EnvioExpres("ENV-102", peso_kg=_peso, distancia_km=_dist, factor_urgencia=1.20),
        EnvioRefrigerado("ENV-103", peso_kg=_peso, distancia_km=_dist, temperatura_c=_temp),
    ]
    if incluir_segundo_estandar_ui.value:
        _lote.append(
            EnvioEstandar("ENV-104", peso_kg=_peso * 2.0, distancia_km=_dist)
        )

    _trazas, _total_lote = procesar_lote_envios(_lote)

    _filas_html = "".join(
        f"""
        <tr>
          <td><code>{r.codigo}</code></td>
          <td><span class="poo-chip poo-chip-indigo">{r.clase_concreta}</span></td>
          <td><code>{r.metodo_invocado}</code></td>
          <td>{r.modalidad}</td>
          <td style="font-family: JetBrains Mono, monospace; font-weight: 700; color: #34d399;">
            ${r.costo:,.2f}
          </td>
        </tr>
        """
        for r in _trazas
    )

    _panel = mo.Html(
        f"""
        <div class="poo-card poo-card-valid">
          <div class="poo-badge-row">
            <span class="poo-chip poo-chip-emerald">Despacho Dinámico Activo</span>
            <span class="poo-chip poo-chip-cyan">{len(_trazas)} instancias en lote</span>
          </div>
          <div class="poo-metric" style="color: #34d399;">
            Facturación Total del Lote = ${_total_lote:,.2f}
          </div>
          <p style="margin: 0.25rem 0 0.5rem 0; font-size: 0.86rem; color: #cbd5e1;">
            La función <code>procesar_lote_envios(lote)</code> ejecuta exactamente la misma expresión
            <code>_envio.calcular_costo()</code> en cada iteración; el método concreto se selecciona
            en tiempo de ejecución según la clase real del objeto receptor:
          </p>
          <div class="poo-table-wrap">
            <table class="poo-table">
              <thead>
                <tr>
                  <th>Instancia</th>
                  <th>Tipo en Ejecución</th>
                  <th>Enlace Dinámico Resuelto</th>
                  <th>Estado Propio</th>
                  <th>Tarifa</th>
                </tr>
              </thead>
              <tbody>
                {_filas_html}
              </tbody>
            </table>
          </div>
        </div>

        <div class="poo-guide-box">
          <strong>Guía de observación:</strong> notá cómo <code>ENV-101</code> y <code>ENV-104</code> pertenecen a la misma clase (<code>EnvioEstandar</code>), pero conservan estados independientes (<code>_peso_kg</code> distinto) y producen tarifas diferentes. Al mismo tiempo, <code>procesar_lote_envios</code> no utiliza ningún <code>if/elif</code> por tipo.
        </div>
        """
    )

    _codigo_jerarquia = "\n".join(
        [
            "# ==========================================================================",
            "# 1. CONTRATO ABSTRACTO Y SUBCLASES (HERENCIA Y SUBTIPADO)",
            "# ==========================================================================",
            "# Envio hereda de ABC (Clase Base Abstracta): funciona como una plantilla general.",
            "# Define qué datos comparten todos los envíos y qué métodos son obligatorios.",
            "class Envio(ABC):",
            '    """Clase base abstracta. Invariante: peso_kg > 0 y distancia_km > 0."""',
            "",
            "    # Constructor común: valida y guarda los datos básicos de cualquier envío",
            "    def __init__(self, codigo: str, peso_kg: float, distancia_km: float) -> None:",
            "        # Si el peso o la distancia son 0 o negativos, rechazamos crear el envío",
            "        if peso_kg <= 0.0 or distancia_km <= 0.0:",
            '            raise ValueError("Peso y distancia deben ser estrictamente positivos.")',
            "        # Guardamos los atributos internos (con guion bajo para protegerlos)",
            "        self._codigo: str = codigo",
            "        self._peso_kg: float = float(peso_kg)",
            "        self._distancia_km: float = float(distancia_km)",
            "",
            "    # @property expone los datos en modo 'solo lectura' (ej. envio.peso_kg)",
            "    @property",
            "    def codigo(self) -> str:",
            "        return self._codigo",
            "",
            "    @property",
            "    def peso_kg(self) -> float:",
            "        return self._peso_kg",
            "",
            "    @property",
            "    def distancia_km(self) -> float:",
            "        return self._distancia_km",
            "",
            "    # @abstractmethod obliga a que cada tipo de envío hijo escriba estos dos métodos:",
            "    @abstractmethod",
            "    def modalidad(self) -> str: ...",
            "",
            "    @abstractmethod",
            "    def calcular_costo(self) -> float: ...",
            "",
            "",
            "# Subclase 1: hereda de Envio y define la tarifa estándar terrestre",
            "class EnvioEstandar(Envio):",
            "    def modalidad(self) -> str:",
            '        return "Terrestre Estándar"',
            "",
            "    # Fórmula propia: costo fijo ($2500) + $420 por kilo + $18 por kilómetro",
            "    def calcular_costo(self) -> float:",
            "        return 2500.0 + self.peso_kg * 420.0 + self.distancia_km * 18.0",
            "",
            "",
            "# Subclase 2: hereda de Envio y suma un factor de urgencia (por defecto +20 %)",
            "class EnvioExpres(Envio):",
            "    def __init__(",
            "        self, codigo: str, peso_kg: float, distancia_km: float, factor_urgencia: float = 1.20",
            "    ) -> None:",
            "        # super().__init__ llama al constructor de Envio para validar peso y distancia",
            "        super().__init__(codigo, peso_kg, distancia_km)",
            "        if factor_urgencia < 1.0:",
            '            raise ValueError("El factor de urgencia no puede ser menor a 1.0.")',
            "        self._factor_urgencia = factor_urgencia  # Atributo exclusivo de EnvioExpres",
            "",
            "    def modalidad(self) -> str:",
            '        return "Aéreo Exprés 24h"',
            "",
            "    # Fórmula propia: calcula la base aérea y la multiplica por el factor de urgencia",
            "    def calcular_costo(self) -> float:",
            "        base = 3800.0 + self.peso_kg * 550.0 + self.distancia_km * 32.0",
            "        return base * self._factor_urgencia",
            "",
            "",
            "# Subclase 3: hereda de Envio y agrega control de temperatura para cadena de frío",
            "class EnvioRefrigerado(Envio):",
            "    def __init__(",
            "        self, codigo: str, peso_kg: float, distancia_km: float, temperatura_c: float = 4.0",
            "    ) -> None:",
            "        super().__init__(codigo, peso_kg, distancia_km)",
            "        self._temperatura_c = temperatura_c  # Temperatura objetivo en grados Celsius",
            "",
            "    def modalidad(self) -> str:",
            '        return f"Cadena de Frío ({self._temperatura_c:.1f} °C)"',
            "",
            "    # Fórmula propia: suma un recargo térmico mayor si requiere congelación (<= 0 °C)",
            "    def calcular_costo(self) -> float:",
            "        recargo = 3200.0 if self._temperatura_c <= 0.0 else 1800.0",
            "        return 4600.0 + self.peso_kg * 600.0 + self.distancia_km * 28.0 + recargo",
            "",
            "",
            "# ==========================================================================",
            "# 2. DESPACHADOR POLIMÓRFICO (SIN IF/ELIF NI ISINSTANCE)",
            "# ==========================================================================",
            "# Esta función recibe una lista mezclada de envíos (Estándar, Exprés, Refrigerado).",
            "# No necesita preguntar de qué tipo es cada uno: solo les pide 'calcular_costo()'.",
            "def procesar_lote_envios(lote: list[Envio]) -> tuple[list[RegistroDespacho], float]:",
            '    """Resuelve envio.calcular_costo() en tiempo de ejecución (late binding)."""',
            "    registros: list[RegistroDespacho] = []",
            "    total = 0.0",
            "",
            "    for envio in lote:",
            "        # Despacho dinámico: Python ejecuta el calcular_costo() de la clase real de 'envio'",
            "        costo = envio.calcular_costo()",
            "        total += costo",
            "        clase = type(envio).__name__  # Nombre de la clase real (solo para mostrar en tabla)",
            "        registros.append(",
            "            RegistroDespacho(",
            "                codigo=envio.codigo,",
            "                clase_concreta=clase,",
            '                metodo_invocado=f"{clase}.calcular_costo(self)",',
            "                modalidad=envio.modalidad(),",
            "                costo=costo,",
            "                id_instancia=hex(id(envio)),  # Dirección única del objeto en memoria",
            "            )",
            "        )",
            "    return registros, total",
        ]
    )

    _acordeon = mo.accordion(
        {
            "Ver código fuente de la jerarquía y del despachador polimórfico": mo.md(
                f"```python\n{_codigo_jerarquia}\n```"
            ),
            "Notas de precisión conceptual (Subtipado, Despacho Dinámico y Composición)": mo.md(
                """
                - **Herencia vs. Subtipado:** heredar código (subclase) solo constituye un subtipado válido si la subclase respeta las invariantes y el contrato esperado por cualquier cliente de `Envio` (Principio de Sustitución de Liskov).
                - **Despacho dinámico vs. otras formas de polimorfismo:** aquí observamos *polimorfismo de subtipado* con enlace tardío (*late binding*). Se diferencia del *polimorfismo paramétrico* (`list[T]`, genéricos) y del *polimorfismo ad-hoc* (sobrecarga de operadores como `+`).
                """
            ),
        }
    )

    mo.vstack([_panel, _acordeon], gap=0.9)
    return


@app.cell
def _(Envio, EnvioEstandar, EnvioExpres, mo, procesar_lote_envios):
    # ==========================================================================
    # 4. ZONA DE EXPERIMENTACIÓN ABIERTA (MODO SANDBOX EDITABLE)
    # ==========================================================================
    # Extensión abierta (OCP): creamos un nuevo subtipo SIN tocar procesar_lote_envios
    class EnvioDronUrbano(Envio):
        """Nuevo subtipo experimental para paquetes livianos de corta distancia."""

        def modalidad(self) -> str:
            return "Dron Autónomo Urbano"

        def calcular_costo(self) -> float:
            return 1900.0 + self.peso_kg * 300.0 + self.distancia_km * 12.0

    lote_experimental: list[Envio] = [
        EnvioEstandar("EXP-01", peso_kg=3.0, distancia_km=25.0),
        EnvioExpres("EXP-02", peso_kg=3.0, distancia_km=25.0),
        EnvioDronUrbano("DRON-03", peso_kg=3.0, distancia_km=25.0),
    ]
    trazas_exp, total_exp = procesar_lote_envios(lote_experimental)

    mo.md(
        f"""
        #### Celda de prueba rápida (editable en Modo Editor)
        - **Nuevo subtipo agregado sin modificar el procesador:** `EnvioDronUrbano`
        - **Tarifa Dron (`DRON-03`):** `${trazas_exp[-1].costo:,.2f}` | **Total lote prueba (`3` envíos):** `${total_exp:,.2f}`
        """
    )
    return EnvioDronUrbano, lote_experimental, total_exp, trazas_exp


if __name__ == "__main__":
    app.run()
