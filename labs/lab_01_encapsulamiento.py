import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="medium",
    app_title="Laboratorio POO 01 — Encapsulamiento e Invariantes",
    css_file="lab_theme.css",
    html_head_file="lab_head.html",
)


@app.cell(hide_code=True)
def _():
    from dataclasses import dataclass
    from typing import Any, Literal
    import inspect
    import marimo as mo

    return Any, Literal, dataclass, inspect, mo


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="poo-lab-banner">
          <div class="poo-lab-nav">
            <div class="poo-badge-row" style="margin-bottom: 0;">
              <span class="poo-chip poo-chip-cyan">Programación I · Unidad VI</span>
              <span class="poo-chip poo-chip-emerald">Python + Pyodide (WASM)</span>
            </div>
            <nav class="poo-lab-nav-links" aria-label="Navegación del laboratorio">
              <a class="poo-nav-link" href="../../../index.html">← Presentación</a>
              <a class="poo-nav-link" href="../../../guia/index.html">📱 Guía Móvil</a>
              <a class="poo-nav-link poo-nav-link-active" href="../../01-encapsulamiento/run/index.html">Lab 01</a>
              <a class="poo-nav-link" href="../../02-herencia-polimorfismo/run/index.html">Lab 02</a>
              <a class="poo-nav-link" href="../../03-patron-strategy/run/index.html">Lab 03</a>
              <a class="poo-nav-link" href="../../04-comparacion-paradigmas/run/index.html">Lab 04</a>
              <a class="poo-nav-link" href="../run/index.html">🎛️ Simulador</a>
              <a class="poo-nav-link" href="../edit/index.html">✏️ Editor</a>
            </nav>
          </div>
          <h2 style="margin: 0.15rem 0 0.45rem 0; font-size: 1.28rem; color: #f8fafc;">
            Laboratorio 01: Encapsulamiento e Invariante de Representación
          </h2>
          <p style="margin: 0; color: #cbd5e1; font-size: 0.91rem; line-height: 1.5;">
            <strong>Problema:</strong> cuando un diccionario mutable se expone sin contrato de validación, cualquier rutina puede dejar saldos negativos inconsistentes.<br/>
            <strong>Solución POO:</strong> la clase <code>CuentaBancaria</code> agrupa estado interno (<code>_saldo</code>) y comportamiento, exigiendo que toda operación pública preserve la <strong>invariante</strong> <code>self._saldo &gt;= 0.0</code>.<br/>
            <strong>Mejora obtenida:</strong> las reglas del dominio se verifican en un único punto contractual en lugar de repetirse en cada llamada externa.
          </p>
        </div>
        """
    )
    return


@app.cell
def _(Any, Literal):
    # ==========================================================================
    # 1. DEFINICIÓN DE CLASES, CONTRATOS Y VARIABLES DE DOMINIO
    # ==========================================================================

    # Definimos los nombres válidos de las operaciones que puede elegir el usuario
    TipoOperacion = Literal[
        "extraccion",
        "deposito",
        "mutacion_externa",
        "transferencia",
    ]

    # --- Caso A: Estructura mutable expuesta sin barrera de validación ---
    # Aquí representamos la cuenta como un simple diccionario (datos sueltos).
    # Cualquier función puede tocar "saldo" directamente sin pedir permiso ni validar reglas.
    def operar_cuenta_diccionario(
        cuenta: dict[str, Any],
        operacion: TipoOperacion,
        monto: float,
        destino: dict[str, Any] | None = None,
    ) -> str:
        """Opera directamente sobre un diccionario expuesto sin validar invariantes."""
        # Si piden extraer, restamos directo sin revisar si alcanza el dinero o si el monto es negativo
        if operacion == "extraccion":
            cuenta["saldo"] = cuenta["saldo"] - monto  # ¡Peligro! Puede dejar el saldo en negativo
            return f"Se ejecutó cuenta['saldo'] -= {monto:,.0f} sin control de invariante."

        # Si piden depositar, sumamos directo sin revisar si el monto era negativo
        if operacion == "deposito":
            cuenta["saldo"] = cuenta["saldo"] + monto  # Si monto es negativo, en realidad resta dinero
            return f"Se ejecutó cuenta['saldo'] += {monto:,.0f} directamente sobre el diccionario."

        # Simulamos que cualquier parte del programa pisa el saldo por error con un número negativo
        if operacion == "mutacion_externa":
            cuenta["saldo"] = -abs(monto) if monto != 0 else -15000.0  # Sobrescribe el valor sin trabas
            return "Código externo reasignó cuenta['saldo'] a un valor negativo."

        # Transferencia directa: resta en una cuenta y suma en la otra sin ninguna verificación
        if operacion == "transferencia" and destino is not None:
            cuenta["saldo"] -= monto   # Descuenta de la cuenta origen aunque no tenga fondos
            destino["saldo"] += monto  # Acredita en la cuenta destino
            return "Transferencia directa entre diccionarios sin validación previa."

        return "Sin cambios."

    # --- Caso B: Clase con encapsulamiento e invariante de representación ---
    # Una 'clase' es un molde que agrupa los DATOS (saldo, titular) junto con las REGLAS (métodos)
    # que protegen esos datos para que nunca queden en un estado inválido.
    class CuentaBancaria:
        """
        Modela una cuenta bancaria sin descubierto.

        Invariante de Representación (regla que NUNCA debe romperse):
            1. self._saldo >= 0.0 tras crear la cuenta y antes/después de cada operación.
            2. self._titular no puede ser un texto vacío.
        """

        # __init__ es el "constructor": se ejecuta automáticamente al crear una nueva cuenta
        # 'self' representa a la cuenta específica que se está creando o usando en ese momento
        def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:
            # 1. Validamos que el nombre del titular no esté vacío (strip quita espacios en blanco)
            if not titular.strip():
                raise ValueError("El titular de la cuenta no puede estar vacío.")
            # 2. Validamos que la cuenta no nazca con deuda (saldo negativo)
            if saldo_inicial < 0.0:
                raise ValueError(
                    f"Invariante rechazada en constructor: saldo inicial (${saldo_inicial:,.2f}) < $0."
                )
            # 3. Guardamos los datos dentro del objeto.
            # El guion bajo inicial (_titular, _saldo) indica que son datos INTERNOS (privados por convención)
            # y que nadie desde afuera debería modificarlos directamente.
            self._titular: str = titular.strip()
            self._saldo: float = float(saldo_inicial)
            self._historial: list[str] = [f"Apertura válida: ${self._saldo:,.2f}"]
            # 4. Comprobamos que la regla de seguridad se cumpla al terminar de crear la cuenta
            self._verificar_invariante()

        # @property convierte un método en un atributo de "solo lectura".
        # Permite leer cuenta.titular desde afuera, pero bloquea intentos de hacer cuenta.titular = "Otro"
        @property
        def titular(self) -> str:
            """Propiedad pública de solo lectura para consultar el titular."""
            return self._titular

        # Permite consultar cuenta.saldo, pero impide hacer cuenta.saldo = -5000 desde afuera
        @property
        def saldo(self) -> float:
            """Expone lectura del saldo sin habilitar reasignación directa."""
            return self._saldo

        # Devolvemos una copia inmutable (tuple) del historial para que nadie pueda borrar movimientos desde afuera
        @property
        def historial(self) -> tuple[str, ...]:
            """Retorna una tupla inmutable para resguardar la lista interna."""
            return tuple(self._historial)

        # Método interno de control: revisa que la regla principal (saldo >= 0) siga intacta
        def _verificar_invariante(self) -> None:
            """Verifica internamente que el estado conserve consistencia."""
            if self._saldo < 0.0:
                raise RuntimeError("Violación interna de invariante: _saldo negativo.")

        # Método público para ingresar dinero de forma segura
        def depositar(self, monto: float) -> None:
            """Acredita un monto positivo preservando la invariante."""
            # Barrera de validación: rechazamos montos negativos o cero lanzando un error (ValueError)
            if monto <= 0.0:
                raise ValueError(
                    f"Depósito rechazado: el monto (${monto:,.2f}) debe ser mayor a $0."
                )
            # Si pasó la validación, recién ahí sumamos al saldo interno y anotamos en el historial
            self._saldo += monto
            self._historial.append(f"Depósito: +${monto:,.2f}")
            self._verificar_invariante()

        # Método público para retirar dinero de forma segura
        def extraer(self, monto: float) -> None:
            """Debita fondos únicamente si no viola la invariante _saldo >= 0."""
            # Barrera 1: no se puede extraer un monto negativo o cero
            if monto <= 0.0:
                raise ValueError(
                    f"Extracción rechazada: el monto (${monto:,.2f}) debe ser mayor a $0."
                )
            # Barrera 2: no se puede sacar más dinero del que hay disponible en la cuenta
            if monto > self._saldo:
                raise ValueError(
                    f"Fondos insuficientes: intento de extraer ${monto:,.2f} con saldo ${self._saldo:,.2f}."
                )
            # Si todo es válido, descontamos el dinero y registramos el movimiento
            self._saldo -= monto
            self._historial.append(f"Extracción: -${monto:,.2f}")
            self._verificar_invariante()

        # Método para transferir entre dos objetos CuentaBancaria distintos
        def transferir_a(self, destino: "CuentaBancaria", monto: float) -> None:
            """Transfiere fondos a otra instancia mediante paso de mensajes."""
            # Evitamos que una cuenta se transfiera dinero a sí misma
            if destino is self:
                raise ValueError("No se puede transferir hacia la misma cuenta.")
            # Reutilizamos los métodos seguros: si self.extraer(monto) falla, se detiene aquí
            # y nunca llega a acreditar dinero falso en la cuenta destino
            self.extraer(monto)
            destino.depositar(monto)
            self._historial.append(f"Transferencia a {destino.titular}: ${monto:,.2f}")

    return CuentaBancaria, TipoOperacion, operar_cuenta_diccionario


@app.cell
def _(CuentaBancaria, TipoOperacion, dataclass, operar_cuenta_diccionario):
    # ==========================================================================
    # 2. BLOQUE DE CONTROL DE FLUJO Y ORQUESTACIÓN COMPARATIVA
    # ==========================================================================

    # Estructura inmutable para empaquetar los resultados de la comparación y mostrarlos en pantalla
    @dataclass(frozen=True)
    class DiagnosticoComparativo:
        saldo_dict_final: float
        dict_corrupto: bool
        detalle_dict: str
        saldo_poo_final: float
        poo_operacion_aceptada: bool
        detalle_poo: str
        identidad_origen_hex: str
        identidad_destino_hex: str | None
        saldo_destino_poo: float | None
        historial_poo: tuple[str, ...]
        guia_observacion: str

    def ejecutar_comparativa(
        saldo_inicial: float,
        operacion: TipoOperacion,
        monto: float,
        incluir_destino: bool,
    ) -> DiagnosticoComparativo:
        """Evalúa el mismo escenario sobre el diccionario expuesto y la clase CuentaBancaria."""
        # --- 1. Probamos primero con el diccionario sin protección ---
        _cuenta_dict = {"titular": "Ana Gómez", "saldo": float(saldo_inicial)}
        _destino_dict = {"titular": "Bruno Díaz", "saldo": 10000.0} if incluir_destino else None
        _op_efectiva: TipoOperacion = (
            "transferencia"
            if (operacion == "transferencia" and incluir_destino)
            else ("extraccion" if operacion == "transferencia" else operacion)
        )
        # Ejecutamos la operación directa sobre el diccionario
        _detalle_dict = operar_cuenta_diccionario(
            _cuenta_dict, _op_efectiva, monto, _destino_dict
        )
        # Detectamos si el diccionario quedó con datos incoherentes (ej. saldo negativo o monto <= 0)
        _dict_corrupto = (
            _cuenta_dict["saldo"] < 0.0
            or (monto <= 0.0 and _op_efectiva in ("deposito", "extraccion", "transferencia"))
        )

        # --- 2. Ahora probamos exactamente lo mismo con objetos de la clase CuentaBancaria ---
        _cuenta_poo = CuentaBancaria("Ana Gómez", saldo_inicial)
        _destino_poo = CuentaBancaria("Bruno Díaz", 10000.0) if incluir_destino else None
        _aceptada = True

        # Usamos try/except para intentar la operación y capturar el error si la clase la rechaza
        try:
            if _op_efectiva == "extraccion":
                _cuenta_poo.extraer(monto)  # Le pedimos al objeto que extraiga el monto
                _detalle_poo = f"Mensaje cuenta.extraer({monto:,.0f}) aceptado. Invariante preservada."
            elif _op_efectiva == "deposito":
                _cuenta_poo.depositar(monto)  # Le pedimos al objeto que deposite el monto
                _detalle_poo = f"Mensaje cuenta.depositar({monto:,.0f}) aceptado. Invariante preservada."
            elif _op_efectiva == "mutacion_externa":
                # Intentamos forzar cuenta.saldo = -X desde afuera; fallará porque saldo es de solo lectura (@property)
                setattr(_cuenta_poo, "saldo", -abs(monto) if monto != 0 else -15000.0)
                _detalle_poo = "Atributo modificado."
            elif _op_efectiva == "transferencia" and _destino_poo is not None:
                _cuenta_poo.transferir_a(_destino_poo, monto)  # Transferencia segura entre dos objetos
                _detalle_poo = (
                    f"Paso de mensajes cuenta.transferir_a(destino, {monto:,.0f}) completado."
                )
        except (ValueError, AttributeError) as _exc:
            # Si la operación violaba alguna regla, la cuenta lanzó un error y su saldo quedó intacto
            _aceptada = False
            _detalle_poo = f"Operación rechazada ({type(_exc).__name__}): {_exc}"

        if _op_efectiva == "mutacion_externa":
            _guia = (
                "En el diccionario expuesto, cuenta['saldo'] = -... sobrescribe el dato. "
                "En CuentaBancaria, @property saldo no define setter y lanza AttributeError, "
                "manteniendo _saldo resguardado."
            )
        elif not _aceptada:
            _guia = (
                "El diccionario aceptó la operación inválida y quedó inconsistente. "
                "La instancia de CuentaBancaria rechazó el mensaje antes de modificar _saldo, "
                "preservando la invariante _saldo >= 0."
            )
        else:
            _guia = (
                "Con datos válidos ambos llegan al mismo saldo numérico, pero CuentaBancaria "
                "centraliza la validación y conserva el historial inmutable en la propia instancia. "
                "Probá deslizar el monto por encima del saldo inicial para observar el rechazo controlado."
            )

        return DiagnosticoComparativo(
            saldo_dict_final=_cuenta_dict["saldo"],
            dict_corrupto=_dict_corrupto,
            detalle_dict=_detalle_dict,
            saldo_poo_final=_cuenta_poo.saldo,
            poo_operacion_aceptada=_aceptada,
            detalle_poo=_detalle_poo,
            identidad_origen_hex=hex(id(_cuenta_poo)),
            identidad_destino_hex=hex(id(_destino_poo)) if _destino_poo else None,
            saldo_destino_poo=_destino_poo.saldo if _destino_poo else None,
            historial_poo=_cuenta_poo.historial,
            guia_observacion=_guia,
        )

    return DiagnosticoComparativo, ejecutar_comparativa


@app.cell(hide_code=True)
def _(mo):
    saldo_inicial_ui = mo.ui.slider(
        start=0,
        stop=100000,
        step=5000,
        value=30000,
        label="Saldo inicial de la cuenta ($)",
        full_width=True,
    )

    operacion_ui = mo.ui.dropdown(
        options={
            "Extracción: extraer(monto) vs. resta directa": "extraccion",
            "Depósito: depositar(monto) vs. suma directa": "deposito",
            "Intento de reasignación externa (cuenta.saldo = -X)": "mutacion_externa",
            "Transferencia entre dos instancias independientes": "transferencia",
        },
        value="Extracción: extraer(monto) vs. resta directa",
        label="Operación a simular",
        full_width=True,
    )

    monto_ui = mo.ui.slider(
        start=-20000,
        stop=80000,
        step=5000,
        value=45000,
        label="Monto de la operación ($) — incluye negativos y sobregiros",
        full_width=True,
    )

    segunda_instancia_ui = mo.ui.switch(
        value=True,
        label="Crear segunda instancia colaboradora (Bruno Díaz)",
    )

    mo.vstack(
        [
            mo.md("### Parámetros Interactivos de Prueba"),
            saldo_inicial_ui,
            monto_ui,
            operacion_ui,
            segunda_instancia_ui,
        ],
        gap=0.65,
    )
    return monto_ui, operacion_ui, saldo_inicial_ui, segunda_instancia_ui


@app.cell(hide_code=True)
def _(
    CuentaBancaria,
    ejecutar_comparativa,
    inspect,
    mo,
    monto_ui,
    operacion_ui,
    operar_cuenta_diccionario,
    saldo_inicial_ui,
    segunda_instancia_ui,
):
    # ==========================================================================
    # 3. BLOQUE DE PRESENTACIÓN Y SALIDA DE RESULTADOS
    # ==========================================================================

    _diag = ejecutar_comparativa(
        saldo_inicial=float(saldo_inicial_ui.value),
        operacion=operacion_ui.value,
        monto=float(monto_ui.value),
        incluir_destino=bool(segunda_instancia_ui.value),
    )

    _badge_dict = (
        '<span class="poo-chip poo-chip-rose">Estado Inválido</span>'
        if _diag.dict_corrupto
        else '<span class="poo-chip poo-chip-amber">Sin Validación de Contrato</span>'
    )
    _card_dict_cls = "poo-card poo-card-danger" if _diag.dict_corrupto else "poo-card"

    _badge_poo = (
        '<span class="poo-chip poo-chip-emerald">Invariante Preservada (Aceptada)</span>'
        if _diag.poo_operacion_aceptada
        else '<span class="poo-chip poo-chip-emerald">Invariante Protegida (Rechazada)</span>'
    )

    _bloque_destino = ""
    if _diag.identidad_destino_hex is not None and _diag.saldo_destino_poo is not None:
        _bloque_destino = f"""
        <div style="margin-top: 0.65rem; padding-top: 0.55rem; border-top: 1px solid rgba(148,163,184,0.18); font-size: 0.82rem; color: #cbd5e1;">
          <strong>2.ª instancia independiente:</strong> <code>id={_diag.identidad_destino_hex}</code>
          · Saldo Bruno Díaz: <code>${_diag.saldo_destino_poo:,.2f}</code>
        </div>
        """

    _historial_items = "".join(
        f"<li style='margin-bottom: 0.2rem;'><code>{evento}</code></li>"
        for evento in _diag.historial_poo
    )

    import html as _html
    import re as _re

    _PATRON_CODIGO = _re.compile(
        r"(cuenta\['saldo'\](?:\s*[-+]?=\s*(?:-\.\.\.|[\d,.-]+))?"
        r"|cuenta\.(?:extraer|depositar|transferir_a)\([^)]*\)"
        r"|@property saldo"
        r"|_saldo\s*&gt;=\s*0"
        r"|\b(?:CuentaBancaria|ValueError|AttributeError|_saldo)\b)"
    )

    def _resaltar_codigo(texto: str) -> str:
        return _PATRON_CODIGO.sub(r"<code>\1</code>", _html.escape(texto, quote=False))

    def _fmt_moneda(valor: float) -> str:
        return f"-${abs(valor):,.2f}" if valor < 0 else f"${valor:,.2f}"

    _salida_html = mo.Html(
        f"""
        <div class="poo-grid-2">
          <div class="{_card_dict_cls}">
            <div class="poo-badge-row">{_badge_dict}</div>
            <h4 style="margin: 0.2rem 0; color: #fda4af;">1. Problema: Diccionario Expuesto</h4>
            <div class="poo-metric" style="color: {'#fb7185' if _diag.dict_corrupto else '#f8fafc'};">
              cuenta["saldo"] = {_fmt_moneda(_diag.saldo_dict_final)}
            </div>
            <p style="font-size: 0.86rem; color: #cbd5e1; margin: 0.35rem 0 0 0;">
              {_resaltar_codigo(_diag.detalle_dict)}
            </p>
          </div>

          <div class="poo-card poo-card-valid">
            <div class="poo-badge-row">{_badge_poo}</div>
            <h4 style="margin: 0.2rem 0; color: #6ee7b7;">2. Solución: Clase <code>CuentaBancaria</code></h4>
            <div class="poo-metric" style="color: #34d399;">
              cuenta.saldo = {_fmt_moneda(_diag.saldo_poo_final)}
            </div>
            <p style="font-size: 0.86rem; color: #cbd5e1; margin: 0.35rem 0;">
              {_resaltar_codigo(_diag.detalle_poo)}
            </p>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.45rem;">
              Identidad de instancia en CPython (<code>id(self)</code>): <code>{_diag.identidad_origen_hex}</code>
            </div>
            <ul style="margin: 0.45rem 0 0 1.1rem; padding: 0; font-size: 0.81rem; color: #cbd5e1;">
              {_historial_items}
            </ul>
            {_bloque_destino}
          </div>
        </div>

        <div class="poo-guide-box">
          <strong>Guía de observación:</strong> {_resaltar_codigo(_diag.guia_observacion)}
        </div>
        """
    )

    _codigo_fuente = "\n".join(
        [
            "# ==========================================================================",
            "# 1. DICCIONARIO EXPUESTO (PROBLEMA: DATOS SUELTOS SIN BARRERA DE VALIDACIÓN)",
            "# ==========================================================================",
            "# Aquí la cuenta es un simple diccionario: {'titular': 'Ana', 'saldo': 30000.0}.",
            "# Cualquier parte del programa puede tocar 'saldo' directamente sin controles.",
            "def operar_cuenta_diccionario(",
            "    cuenta: dict[str, Any],                # Diccionario con los datos sueltos de la cuenta",
            "    operacion: TipoOperacion,              # Nombre de la operación ('extraccion', 'deposito', etc.)",
            "    monto: float,                          # Cantidad de dinero a mover",
            "    destino: dict[str, Any] | None = None, # Segunda cuenta opcional para transferencias",
            ") -> str:",
            "    # Si piden extraer, restamos directo sin revisar si hay fondos suficientes",
            '    if operacion == "extraccion":',
            '        cuenta["saldo"] = cuenta["saldo"] - monto  # ¡Peligro! Puede dejar el saldo negativo',
            "        return f\"Se ejecutó cuenta['saldo'] -= {monto:,.0f} sin control de invariante.\"",
            "",
            "    # Si piden depositar, sumamos directo sin revisar si el monto era un número negativo",
            '    if operacion == "deposito":',
            '        cuenta["saldo"] = cuenta["saldo"] + monto  # Si monto < 0, en realidad resta dinero',
            "        return f\"Se ejecutó cuenta['saldo'] += {monto:,.0f} directamente sobre el diccionario.\"",
            "",
            "    # Simulamos que código externo pisa el saldo directamente con un valor negativo",
            '    if operacion == "mutacion_externa":',
            '        cuenta["saldo"] = -abs(monto) if monto != 0 else -15000.0  # Nada impide esta asignación',
            "        return \"Código externo reasignó cuenta['saldo'] a un valor negativo.\"",
            "",
            "    # Transferencia sin control: descuenta de una y suma en la otra aunque no haya saldo",
            '    if operacion == "transferencia" and destino is not None:',
            '        cuenta["saldo"] -= monto   # Resta en origen sin validar',
            '        destino["saldo"] += monto  # Suma en destino sin validar',
            '        return "Transferencia directa entre diccionarios sin validación previa."',
            "",
            '    return "Sin cambios."',
            "",
            "",
            "# ==========================================================================",
            "# 2. CLASE CON ENCAPSULAMIENTO E INVARIANTE (SOLUCIÓN ORIENTADA A OBJETOS)",
            "# ==========================================================================",
            "# Una 'clase' agrupa los DATOS (_saldo, _titular) junto con las REGLAS (métodos)",
            "# que impiden que la cuenta quede en un estado inválido.",
            "class CuentaBancaria:",
            '    """Invariante (regla que siempre se cumple): self._saldo >= 0.0 y titular no vacío."""',
            "",
            "    # __init__ es el constructor: se ejecuta al crear la cuenta -> CuentaBancaria('Ana', 30000)",
            "    # 'self' representa a esta cuenta específica en memoria",
            "    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:",
            "        # Validamos que el nombre no esté vacío antes de crear el objeto",
            "        if not titular.strip():",
            '            raise ValueError("El titular de la cuenta no puede estar vacío.")',
            "        # Validamos que la cuenta no nazca con deuda (saldo negativo)",
            "        if saldo_inicial < 0.0:",
            '            raise ValueError("Invariante rechazada en constructor: saldo inicial < $0.")',
            "",
            "        # El guion bajo inicial (_titular, _saldo) indica que son atributos INTERNOS:",
            "        # nadie fuera de la clase debe modificarlos directamente.",
            "        self._titular: str = titular.strip()",
            "        self._saldo: float = float(saldo_inicial)",
            '        self._historial: list[str] = [f"Apertura válida: ${self._saldo:,.2f}"]',
            "        self._verificar_invariante()  # Confirmamos que todo inició cumpliendo la regla",
            "",
            "    # @property permite LEER cuenta.titular, pero bloquea hacer cuenta.titular = 'Otro'",
            "    @property",
            "    def titular(self) -> str:",
            "        return self._titular",
            "",
            "    # @property permite LEER cuenta.saldo, pero impide hacer cuenta.saldo = -5000 desde afuera",
            "    @property",
            "    def saldo(self) -> float:",
            '        """Expone lectura del saldo sin habilitar reasignación directa."""',
            "        return self._saldo",
            "",
            "    # Devolvemos una tupla (lista inmodificable) para que nadie borre movimientos del historial",
            "    @property",
            "    def historial(self) -> tuple[str, ...]:",
            '        """Retorna una tupla inmutable para resguardar la lista interna."""',
            "        return tuple(self._historial)",
            "",
            "    # Método interno de seguridad que comprueba que el saldo jamás sea menor a $0",
            "    def _verificar_invariante(self) -> None:",
            "        if self._saldo < 0.0:",
            '            raise RuntimeError("Violación interna de invariante: _saldo negativo.")',
            "",
            "    # Único camino válido para ingresar dinero: primero valida y luego suma",
            "    def depositar(self, monto: float) -> None:",
            "        if monto <= 0.0:  # Rechaza depósitos negativos o de $0",
            '            raise ValueError("Depósito rechazado: el monto debe ser mayor a $0.")',
            "        self._saldo += monto  # Recién aquí modifica el saldo interno",
            '        self._historial.append(f"Depósito: +${monto:,.2f}")',
            "        self._verificar_invariante()",
            "",
            "    # Único camino válido para retirar dinero: verifica que el monto sea positivo y alcance el saldo",
            "    def extraer(self, monto: float) -> None:",
            "        if monto <= 0.0:  # No se permite extraer $0 ni números negativos",
            '            raise ValueError("Extracción rechazada: el monto debe ser mayor a $0.")',
            "        if monto > self._saldo:  # Si pide más de lo que tiene, rechaza la operación",
            '            raise ValueError("Fondos insuficientes para realizar la extracción.")',
            "        self._saldo -= monto  # Descuenta de forma segura",
            '        self._historial.append(f"Extracción: -${monto:,.2f}")',
            "        self._verificar_invariante()",
            "",
            "    # Transferencia segura entre dos objetos CuentaBancaria distintos",
            '    def transferir_a(self, destino: "CuentaBancaria", monto: float) -> None:',
            "        if destino is self:  # Evita transferir hacia la misma cuenta",
            '            raise ValueError("No se puede transferir hacia la misma cuenta.")',
            "        # Primero intenta extraer de esta cuenta; si no alcanza, lanza error y NO toca 'destino'",
            "        self.extraer(monto)",
            "        # Solo si la extracción fue exitosa, deposita el dinero en la segunda cuenta",
            "        destino.depositar(monto)",
            '        self._historial.append(f"Transferencia a {destino.titular}: ${monto:,.2f}")',
        ]
    )

    _acordeon_codigo = mo.accordion(
        {
            "Ver código Python completo y anotaciones de tipos": mo.md(
                f"```python\n{_codigo_fuente}\n```"
            ),
            "Notas de precisión conceptual (Encapsulamiento, Memoria y Python)": mo.md(
                """
                - **Visibilidad en Python (`_saldo` vs. `__saldo`):** Python no posee modificadores de acceso estrictos en compilación como `private` en C++ o Java. El prefijo simple `_saldo` es la convención oficial (PEP 8) para indicar un atributo interno. El doble guion inicial `__saldo` aplica *name mangling* (renombrándolo a `_CuentaBancaria__saldo`) para evitar colisiones accidentales en subclases, pero no impide el acceso deliberado.
                - **Modularidad procedural vs. POO:** la programación procedural también permite encapsular mediante módulos o tipos abstractos de datos; lo característico de la POO es reunir estado e invariantes dentro de cada instancia y operar mediante métodos ligados a `self`.
                - **Almacenamiento de objetos:** aunque CPython gestiona sus objetos dinámicamente en memoria administrada, en POO en general la ubicación física depende del lenguaje y compilador (por ejemplo, instancias en pila o por valor en C++ y `struct` en C#).
                """
            ),
        }
    )

    mo.vstack([_salida_html, _acordeon_codigo], gap=0.9)
    return


@app.cell
def _(CuentaBancaria, mo):
    # ==========================================================================
    # 4. ZONA DE EXPERIMENTACIÓN ABIERTA (PARA EDITAR EN MODO SANDBOX)
    # ==========================================================================
    cuenta_prueba = CuentaBancaria(titular="Laboratorio Grupo POO", saldo_inicial=25000.0)
    cuenta_prueba.depositar(10000.0)
    cuenta_prueba.extraer(8000.0)

    # Descomentá en Modo Editor para verificar cómo responde la invariante:
    # cuenta_prueba.extraer(99999.0)

    mo.md(
        f"""
        #### Celda de prueba rápida (editable en Modo Editor)
        - **Titular:** `{cuenta_prueba.titular}` | **Saldo actual:** `${cuenta_prueba.saldo:,.2f}`
        - **Movimientos ({len(cuenta_prueba.historial)}):** `{list(cuenta_prueba.historial)}`
        """
    )
    return (cuenta_prueba,)


if __name__ == "__main__":
    app.run()
