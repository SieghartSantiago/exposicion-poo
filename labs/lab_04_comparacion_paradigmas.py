import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="medium",
    app_title="Laboratorio POO 04 — Comparación Multiparadigma en Python",
    css_file="lab_theme.css",
    html_head_file="lab_head.html",
)


@app.cell(hide_code=True)
def _():
    from dataclasses import dataclass
    from functools import reduce
    from typing import Callable, Iterable
    import inspect
    import marimo as mo

    return Callable, Iterable, dataclass, inspect, mo, reduce


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="poo-lab-banner">
          <div class="poo-lab-nav">
            <div class="poo-badge-row" style="margin-bottom: 0;">
              <span class="poo-chip poo-chip-cyan">Programación I · Unidad VI</span>
              <span class="poo-chip poo-chip-amber">Imperativo · POO · Funcional</span>
            </div>
            <nav class="poo-lab-nav-links" aria-label="Navegación del laboratorio">
              <a class="poo-nav-link" href="../../../index.html">← Presentación</a>
              <a class="poo-nav-link" href="../../../guia/index.html">📱 Guía Móvil</a>
              <a class="poo-nav-link" href="../../01-encapsulamiento/run/index.html">Lab 01</a>
              <a class="poo-nav-link" href="../../02-herencia-polimorfismo/run/index.html">Lab 02</a>
              <a class="poo-nav-link" href="../../03-patron-strategy/run/index.html">Lab 03</a>
              <a class="poo-nav-link poo-nav-link-active" href="../../04-comparacion-paradigmas/run/index.html">Lab 04</a>
              <a class="poo-nav-link" href="../run/index.html">🎛️ Simulador</a>
              <a class="poo-nav-link" href="../edit/index.html">✏️ Editor</a>
            </nav>
          </div>
          <h2 style="margin: 0.15rem 0 0.45rem 0; font-size: 1.28rem; color: #f8fafc;">
            Laboratorio 04: Un Mismo Problema en Tres Paradigmas
          </h2>
          <p style="margin: 0; color: #cbd5e1; font-size: 0.91rem; line-height: 1.5;">
            <strong>Problema común:</strong> procesar un lote de ventas crudas, descartar operaciones canceladas o por debajo de un monto mínimo, aplicar una alícuota impositiva y obtener la recaudación neta.<br/>
            <strong>Objetivo académico:</strong> contrastar cómo organizan la solución los enfoques <strong>Imperativo</strong>, <strong>Orientado a Objetos</strong> y <strong>Funcional</strong> en Python, verificando que los tres comparten complejidad asintótica <code>O(n)</code> y analizando sus compromisos reales sin declarar un ganador universal.
          </p>
        </div>
        """
    )
    return


@app.cell
def _(Callable, Iterable, dataclass, reduce):
    # ==========================================================================
    # 1. DEFINICIÓN DEL MISMO PROBLEMA EN TRES PARADIGMAS (PYTHON)
    # ==========================================================================
    # Cada registro crudo es un diccionario como: {"id": "V-001", "monto": 5000.0, "activa": True}
    RegistroCrudo = dict[str, object]

    # --------------------------------------------------------------------------
    # ENFOQUE A: IMPERATIVO / PROCEDURAL (Bucle explícito y estado mutable local)
    # --------------------------------------------------------------------------
    # En este estilo le damos a la computadora instrucciones paso a paso:
    # creamos variables contadoras en 0 y las vamos modificando dentro de un ciclo 'for'.
    def liquidar_imperativo(
        registros: list[RegistroCrudo],
        minimo: float,
        alicuota_impuesto: float,
    ) -> tuple[float, int, int]:
        """Recorre secuencialmente mutando acumuladores locales paso a paso."""
        # Inicializamos las variables que irán cambiando (mutando) vuelta tras vuelta
        total_neto = 0.0
        aprobadas = 0
        descartadas = 0

        # Recorremos la lista de ventas fila por fila
        for fila in registros:
            # Extraemos los datos del diccionario actual
            activa = bool(fila.get("activa", False))
            monto = float(fila.get("monto", 0.0))

            # Si la venta está inactiva, no supera el mínimo o tiene monto inválido (<= 0), la descartamos
            if not activa or monto < minimo or monto <= 0.0:
                descartadas += 1  # Sumamos 1 al contador de descartadas
                continue          # Saltamos directamente a la siguiente fila del ciclo

            # Si llegó hasta aquí es válida: le sumamos el impuesto (ej. * 1.21) y acumulamos
            total_neto += monto * (1.0 + alicuota_impuesto)
            aprobadas += 1

        # Devolvemos el total redondeado a 2 decimales y las cantidades finales
        return round(total_neto, 2), aprobadas, descartadas

    # --------------------------------------------------------------------------
    # ENFOQUE B: ORIENTADO A OBJETOS (Entidad con invariante + servicio cohesivo)
    # --------------------------------------------------------------------------
    # En POO dividimos el problema en objetos con responsabilidades claras:
    # 1. VentaConfirmada: representa una venta individual que se valida a sí misma al crearse.
    # 2. ProcesadorVentasPOO: coordina la liquidación aplicando las reglas del negocio.
    class VentaConfirmada:
        """Entidad de dominio que garantiza monto > 0 desde su construcción."""

        def __init__(self, id_venta: str, monto_base: float) -> None:
            # Invariante: un objeto VentaConfirmada jamás puede existir con monto 0 o negativo
            if monto_base <= 0.0:
                raise ValueError(f"Venta {id_venta} rechazada: monto <= 0.")
            self._id_venta = id_venta
            self._monto_base = float(monto_base)

        @property
        def monto_base(self) -> float:
            return self._monto_base

        # Cada venta sabe calcular su propio importe final con impuestos incluidos
        def importe_con_impuesto(self, alicuota: float) -> float:
            return self._monto_base * (1.0 + alicuota)

    class ProcesadorVentasPOO:
        """Encapsula la política impositiva y el umbral de aceptación."""

        # Guardamos la configuración (monto mínimo e impuesto) dentro del procesador
        def __init__(self, minimo: float, alicuota_impuesto: float) -> None:
            self._minimo = minimo
            self._alicuota = alicuota_impuesto

        def liquidar(self, registros: Iterable[RegistroCrudo]) -> tuple[float, int, int]:
            ventas_validas: list[VentaConfirmada] = []  # Lista donde guardaremos los objetos válidos
            descartadas = 0

            for fila in registros:
                # Filtramos ventas inactivas o por debajo del mínimo configurado
                if not bool(fila.get("activa", False)):
                    descartadas += 1
                    continue
                monto = float(fila.get("monto", 0.0))
                if monto < self._minimo:
                    descartadas += 1
                    continue
                # Intentamos crear el objeto VentaConfirmada; si el monto es <= 0, la propia clase lanza ValueError
                try:
                    ventas_validas.append(
                        VentaConfirmada(str(fila.get("id", "?")), monto)
                    )
                except ValueError:
                    descartadas += 1

            # Pedimos a cada objeto VentaConfirmada su importe con impuesto y sumamos todos
            total = sum(v.importe_con_impuesto(self._alicuota) for v in ventas_validas)
            return round(total, 2), len(ventas_validas), descartadas

    # --------------------------------------------------------------------------
    # ENFOQUE C: FUNCIONAL (Datos inmutables + funciones puras de orden superior)
    # --------------------------------------------------------------------------
    # En el paradigma funcional evitamos modificar variables existentes (no hay contadores += 1).
    # En su lugar, transformamos colecciones inmutables encadenando funciones (filter -> map -> reduce).
    @dataclass(frozen=True)  # frozen=True impide modificar los datos del evento una vez creado
    class EventoVentaInmutable:
        id_venta: str
        monto: float
        activa: bool

    # Función que devuelve otra función (lambda) configurada para decidir si una venta es válida
    def construir_filtro_validez(
        minimo: float,
    ) -> Callable[[EventoVentaInmutable], bool]:
        """Función de orden superior (clausura pura) sin estado mutable."""
        return lambda ev: ev.activa and ev.monto > 0.0 and ev.monto >= minimo

    def liquidar_funcional(
        registros: Iterable[RegistroCrudo],
        minimo: float,
        alicuota_impuesto: float,
    ) -> tuple[float, int, int]:
        """Pipeline declarativo filter -> map -> reduce sin mutación de variables."""
        # Paso 1: Convertimos los diccionarios crudos en una tupla inmutable de eventos
        eventos: tuple[EventoVentaInmutable, ...] = tuple(
            EventoVentaInmutable(
                id_venta=str(r.get("id", "?")),
                monto=float(r.get("monto", 0.0)),
                activa=bool(r.get("activa", False)),
            )
            for r in registros
        )
        # Paso 2 (filter): Nos quedamos únicamente con los eventos que cumplen la regla de validez
        es_valida = construir_filtro_validez(minimo)
        validas = tuple(filter(es_valida, eventos))

        # Paso 3 (map): Transformamos cada venta válida en su monto final con impuesto
        montos_finales = map(lambda ev: ev.monto * (1.0 + alicuota_impuesto), validas)

        # Paso 4 (reduce): Sumamos todos los montos finales partiendo desde 0.0
        total = reduce(lambda acc, x: acc + x, montos_finales, 0.0)
        return round(total, 2), len(validas), len(eventos) - len(validas)

    return (
        EventoVentaInmutable,
        ProcesadorVentasPOO,
        RegistroCrudo,
        VentaConfirmada,
        construir_filtro_validez,
        liquidar_funcional,
        liquidar_imperativo,
    )


@app.cell
def _(RegistroCrudo):
    # ==========================================================================
    # 2. GENERADOR DETERMINISTA DE LOTES DE PRUEBA
    # ==========================================================================
    # Genera una lista de ventas de prueba para alimentar a los 3 paradigmas con los mismos datos
    def generar_lote_ventas(
        cantidad: int, incluir_registros_invalidos: bool
    ) -> list[RegistroCrudo]:
        _lote: list[RegistroCrudo] = []
        for _idx in range(1, cantidad + 1):
            # Cada 5 filas inyectamos un monto negativo (-$1200) si el switch está activo
            if incluir_registros_invalidos and _idx % 5 == 0:
                _lote.append({"id": f"V-{_idx:03d}", "monto": -1200.0, "activa": True})
            # Cada 4 filas simulamos una operación anulada/inactiva (activa: False)
            elif _idx % 4 == 0:
                _lote.append({"id": f"V-{_idx:03d}", "monto": 4500.0, "activa": False})
            # El resto son ventas activas con montos positivos variados
            else:
                _lote.append(
                    {
                        "id": f"V-{_idx:03d}",
                        "monto": float(1500 + (_idx * 850) % 14000),
                        "activa": True,
                    }
                )
        return _lote

    return (generar_lote_ventas,)


@app.cell(hide_code=True)
def _(mo):
    tamano_lote_ui = mo.ui.slider(
        start=6,
        stop=120,
        step=6,
        value=24,
        label="Tamaño del lote de entrada `n` (cantidad de filas)",
        full_width=True,
    )

    minimo_ui = mo.ui.slider(
        start=0,
        stop=10000,
        step=1000,
        value=3000,
        label="Monto mínimo requerido para liquidar ($)",
        full_width=True,
    )

    impuesto_ui = mo.ui.slider(
        start=0,
        stop=30,
        step=3,
        value=21,
        label="Alícuota impositiva (%)",
        full_width=True,
    )

    invalidos_ui = mo.ui.switch(
        value=True,
        label="Inyectar registros corruptos con montos negativos en el lote",
    )

    mo.vstack(
        [
            mo.md("### Parámetros Comunes para los Tres Paradigmas"),
            tamano_lote_ui,
            minimo_ui,
            impuesto_ui,
            invalidos_ui,
        ],
        gap=0.65,
    )
    return impuesto_ui, invalidos_ui, minimo_ui, tamano_lote_ui


@app.cell(hide_code=True)
def _(
    ProcesadorVentasPOO,
    generar_lote_ventas,
    impuesto_ui,
    inspect,
    invalidos_ui,
    liquidar_funcional,
    liquidar_imperativo,
    minimo_ui,
    mo,
    tamano_lote_ui,
):
    # ==========================================================================
    # 3. BLOQUE DE PRESENTACIÓN Y CONTRASTE DE TRADE-OFFS
    # ==========================================================================
    _n = int(tamano_lote_ui.value)
    _min = float(minimo_ui.value)
    _iva = float(impuesto_ui.value) / 100.0
    _datos = generar_lote_ventas(_n, bool(invalidos_ui.value))

    _tot_imp, _ok_imp, _desc_imp = liquidar_imperativo(_datos, _min, _iva)
    _tot_poo, _ok_poo, _desc_poo = ProcesadorVentasPOO(_min, _iva).liquidar(_datos)
    _tot_fun, _ok_fun, _desc_fun = liquidar_funcional(_datos, _min, _iva)

    _coinciden = (_tot_imp == _tot_poo == _tot_fun) and (_ok_imp == _ok_poo == _ok_fun)

    _html = mo.Html(
        f"""
        <div class="poo-grid-3">
          <div class="poo-card">
            <div class="poo-badge-row">
              <span class="poo-chip poo-chip-amber">1. Imperativo</span>
            </div>
            <div class="poo-metric" style="color: #fde68a;">${_tot_imp:,.2f}</div>
            <p style="font-size: 0.82rem; color: #cbd5e1; margin: 0;">
              Válidas: <code>{_ok_imp}</code> · Descartadas: <code>{_desc_imp}</code><br/>
              <strong>Foco:</strong> control explícito paso a paso y mínima sobrecarga de estructuras.
            </p>
          </div>

          <div class="poo-card poo-card-valid">
            <div class="poo-badge-row">
              <span class="poo-chip poo-chip-indigo">2. Orientado a Objetos</span>
            </div>
            <div class="poo-metric" style="color: #34d399;">${_tot_poo:,.2f}</div>
            <p style="font-size: 0.82rem; color: #cbd5e1; margin: 0;">
              Válidas: <code>{_ok_poo}</code> · Descartadas: <code>{_desc_poo}</code><br/>
              <strong>Foco:</strong> entidades con invariante propia y extensión mediante contratos.
            </p>
          </div>

          <div class="poo-card">
            <div class="poo-badge-row">
              <span class="poo-chip poo-chip-cyan">3. Funcional</span>
            </div>
            <div class="poo-metric" style="color: #7dd3fc;">${_tot_fun:,.2f}</div>
            <p style="font-size: 0.82rem; color: #cbd5e1; margin: 0;">
              Válidas: <code>{_ok_fun}</code> · Descartadas: <code>{_desc_fun}</code><br/>
              <strong>Foco:</strong> inmutabilidad, funciones puras y composición de transformaciones.
            </p>
          </div>
        </div>

        <div class="poo-table-wrap">
          <table class="poo-table">
            <thead>
              <tr>
                <th>Dimensión Técnica</th>
                <th>Imperativo</th>
                <th>Orientado a Objetos</th>
                <th>Funcional</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Complejidad Temporal</strong></td>
                <td><code>O(n)</code> ({_n} lecturas)</td>
                <td><code>O(n)</code> ({_n} lecturas)</td>
                <td><code>O(n)</code> ({_n} lecturas)</td>
              </tr>
              <tr>
                <td><strong>Manejo del Estado</strong></td>
                <td>Acumuladores mutables locales</td>
                <td>Encapsulado con invariante por objeto</td>
                <td>Sin mutación (tuplas y valores nuevos)</td>
              </tr>
              <tr>
                <td><strong>Cuándo elegirlo</strong></td>
                <td>Scripts directos, lazos numéricos simples</td>
                <td>Dominios ricos con reglas e interfaces cambiantes</td>
                <td>Pipelines de datos, concurrencia y pruebas puras</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="poo-guide-box">
          <strong>Verificación de equivalencia ({'EXACTA ✓' if _coinciden else 'DIFERENCIA'}):</strong>
          los tres paradigmas arriban exactamente a <code>${_tot_poo:,.2f}</code> recorriendo las <code>{_n}</code> filas en tiempo lineal <code>O(n)</code>. Python es multiparadigma: en sistemas reales es habitual combinar objetos en la arquitectura de módulos con transformaciones funcionales dentro de sus métodos.
        </div>
        """
    )

    _codigo_paradigmas = "\n".join(
        [
            "# ==========================================================================",
            "# 1. ENFOQUE IMPERATIVO / PROCEDURAL (BUCLE Y ACUMULADORES MUTABLES)",
            "# ==========================================================================",
            "# Le indica a la computadora el paso a paso: crea contadores en 0 y los va",
            "# modificando vuelta por vuelta dentro de un ciclo 'for'.",
            "def liquidar_imperativo(",
            "    registros: list[RegistroCrudo],",
            "    minimo: float,",
            "    alicuota_impuesto: float,",
            ") -> tuple[float, int, int]:",
            "    # Variables que irán cambiando (mutando) a medida que recorremos la lista",
            "    total_neto = 0.0",
            "    aprobadas = 0",
            "    descartadas = 0",
            "",
            "    for fila in registros:",
            "        # Leemos los datos sueltos de cada diccionario",
            '        activa = bool(fila.get("activa", False))',
            '        monto = float(fila.get("monto", 0.0))',
            "",
            "        # Si está anulada, no alcanza el mínimo o el monto es <= 0, la descartamos",
            "        if not activa or monto < minimo or monto <= 0.0:",
            "            descartadas += 1  # Incrementa el contador de descartadas",
            "            continue          # Salta a la siguiente fila sin sumar al total",
            "",
            "        # Si es válida, sumamos el monto más el impuesto (ej. * 1.21) al acumulador",
            "        total_neto += monto * (1.0 + alicuota_impuesto)",
            "        aprobadas += 1",
            "",
            "    return round(total_neto, 2), aprobadas, descartadas",
            "",
            "",
            "# ==========================================================================",
            "# 2. ENFOQUE ORIENTADO A OBJETOS (ENTIDAD CON INVARIANTE + SERVICIO)",
            "# ==========================================================================",
            "# Divide responsabilidades en dos clases:",
            "# - VentaConfirmada: protege sus propios datos (impide que exista una venta con monto <= 0).",
            "# - ProcesadorVentasPOO: guarda la configuración impositiva y coordina la liquidación.",
            "class VentaConfirmada:",
            '    """Entidad de dominio que garantiza monto > 0 desde su construcción."""',
            "",
            "    def __init__(self, id_venta: str, monto_base: float) -> None:",
            "        # Regla invariante: si el monto es 0 o negativo, rechaza crear el objeto",
            "        if monto_base <= 0.0:",
            '            raise ValueError(f"Venta {id_venta} rechazada: monto <= 0.")',
            "        self._id_venta = id_venta",
            "        self._monto_base = float(monto_base)",
            "",
            "    # El propio objeto sabe calcular su precio final con impuesto",
            "    def importe_con_impuesto(self, alicuota: float) -> float:",
            "        return self._monto_base * (1.0 + alicuota)",
            "",
            "",
            "class ProcesadorVentasPOO:",
            "    def __init__(self, minimo: float, alicuota_impuesto: float) -> None:",
            "        self._minimo = minimo              # Umbral mínimo guardado en el procesador",
            "        self._alicuota = alicuota_impuesto # Porcentaje de impuesto guardado en el procesador",
            "",
            "    def liquidar(self, registros: Iterable[RegistroCrudo]) -> tuple[float, int, int]:",
            "        ventas_validas: list[VentaConfirmada] = []",
            "        descartadas = 0",
            "",
            "        for fila in registros:",
            '            if not bool(fila.get("activa", False)):',
            "                descartadas += 1",
            "                continue",
            '            monto = float(fila.get("monto", 0.0))',
            "            if monto < self._minimo:",
            "                descartadas += 1",
            "                continue",
            "            # Intentamos construir el objeto VentaConfirmada; si el monto es <= 0, lanza ValueError",
            "            try:",
            '                ventas_validas.append(VentaConfirmada(str(fila.get("id", "?")), monto))',
            "            except ValueError:",
            "                descartadas += 1",
            "",
            "        # Le pedimos a cada objeto VentaConfirmada su importe final y los sumamos",
            "        total = sum(v.importe_con_impuesto(self._alicuota) for v in ventas_validas)",
            "        return round(total, 2), len(ventas_validas), descartadas",
            "",
            "",
            "# ==========================================================================",
            "# 3. ENFOQUE FUNCIONAL (DATOS INMUTABLES + FUNCIONES PURAS)",
            "# ==========================================================================",
            "# No modifica variables existentes (no usa '+= 1' ni '.append()').",
            "# En su lugar, pasa datos inmutables por una tubería de funciones: filter -> map -> reduce.",
            "@dataclass(frozen=True)  # frozen=True hace que el registro sea inmodificable (inmutable)",
            "class EventoVentaInmutable:",
            "    id_venta: str",
            "    monto: float",
            "    activa: bool",
            "",
            "",
            "# Devuelve una función de evaluación (lambda) que responde True solo si la venta es válida",
            "def construir_filtro_validez(minimo: float) -> Callable[[EventoVentaInmutable], bool]:",
            "    return lambda ev: ev.activa and ev.monto > 0.0 and ev.monto >= minimo",
            "",
            "",
            "def liquidar_funcional(",
            "    registros: Iterable[RegistroCrudo],",
            "    minimo: float,",
            "    alicuota_impuesto: float,",
            ") -> tuple[float, int, int]:",
            "    # 1. Transformamos los diccionarios de entrada en una tupla inmutable de eventos",
            "    eventos = tuple(",
            "        EventoVentaInmutable(",
            '            id_venta=str(r.get("id", "?")),',
            '            monto=float(r.get("monto", 0.0)),',
            '            activa=bool(r.get("activa", False)),',
            "        )",
            "        for r in registros",
            "    )",
            "    # 2. filter: filtra y conserva únicamente los eventos que cumplen la condición",
            "    validas = tuple(filter(construir_filtro_validez(minimo), eventos))",
            "",
            "    # 3. map: a cada venta válida le aplica el cálculo del impuesto",
            "    montos_finales = map(lambda ev: ev.monto * (1.0 + alicuota_impuesto), validas)",
            "",
            "    # 4. reduce: acumula todos los montos finales sumándolos desde 0.0",
            "    total = reduce(lambda acc, x: acc + x, montos_finales, 0.0)",
            "    return round(total, 2), len(validas), len(eventos) - len(validas)",
        ]
    )

    _acordeon = mo.accordion(
        {
            "Comparar el código Python completo de las 3 implementaciones": mo.md(
                f"```python\n{_codigo_paradigmas}\n```"
            )
        }
    )

    mo.vstack([_html, _acordeon], gap=0.9)
    return


@app.cell
def _(ProcesadorVentasPOO, liquidar_funcional, liquidar_imperativo, mo):
    # ==========================================================================
    # 4. ZONA DE EXPERIMENTACIÓN ABIERTA (MODO SANDBOX EDITABLE)
    # ==========================================================================
    muestra_manual = [
        {"id": "M-01", "monto": 10000.0, "activa": True},
        {"id": "M-02", "monto": -500.0, "activa": True},
        {"id": "M-03", "monto": 5000.0, "activa": True},
    ]

    res_imp = liquidar_imperativo(muestra_manual, minimo=1000.0, alicuota_impuesto=0.21)
    res_poo = ProcesadorVentasPOO(minimo=1000.0, alicuota_impuesto=0.21).liquidar(muestra_manual)
    res_fun = liquidar_funcional(muestra_manual, minimo=1000.0, alicuota_impuesto=0.21)

    assert res_imp == res_poo == res_fun

    mo.md(
        f"""
        #### Celda de prueba rápida (editable en Modo Editor)
        - **Resultado verificado en los 3 paradigmas (`total, válidas, descartadas`):** `{res_poo}`
        """
    )
    return muestra_manual, res_fun, res_imp, res_poo


if __name__ == "__main__":
    app.run()
