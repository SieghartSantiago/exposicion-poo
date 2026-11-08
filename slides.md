---
theme: default
layout: cover-poo
title: "Programación Orientada a Objetos — Programación I"
info: |
  Exposición interactiva sobre el Paradigma Orientado a Objetos.
  Ingeniería en Informática — Programación I (Unidad VI, 2026).
colorSchema: dark
transition: slide-left
lineNumbers: false
kicker: "Programación I · Ingeniería en Informática"
badge: "Unidad VI · 2026"
footerLeft: "Navegación: → / ← o clic en pasos interactivos"
footerRight: "23 Diapositivas + 4 Laboratorios Python WebAssembly"
---

<h1 style="font-size: 2.5rem; line-height: 1.1; font-weight: 800;">
  Programación Orientada a <span style="color: var(--accent-interface);">Objetos</span>
</h1>

<p style="font-size: 1rem; line-height: 1.5; color: var(--text-secondary); max-width: 46ch;">
  Modelado de software mediante objetos que integran estado interno, comportamiento e invariantes protegidas por contrato.
</p>

<QrAccessModal />

::graphic::

<CoverHeroGraphic />

<!--
Notas de exposición (Diapositiva 1 — Portada):
- Dar la bienvenida a la exposición del Paradigma de Programación Orientada a Objetos (Unidad VI, Programación I).
- Invitar a los estudiantes y docentes a escanear el código QR para abrir la Guía de Lectura Móvil y los 4 laboratorios Python ejecutables en el navegador.
-->

---
layout: code-explain
clicks: 2
transition: slide-left
kicker: "Bloque 1 · Introducción al Paradigma"
kickerVariant: "interface"
title: "¿Qué es un Paradigma y qué Propone la POO?"
badge: "3 pasos interactivos"
---

<ParadigmShiftVisualizer />

<!--
Notas de exposición (Diapositiva 2 — Qué es un paradigma y cambio conceptual):
- Paso 1: Definir un paradigma como un marco conceptual que organiza cómo representamos información, estado y flujo de control.
- Paso 2: Contrastar el eje organizativo procedural (datos y funciones separables, aun contando con módulos) frente al eje orientado a objetos (cápsulas que reúnen estado, operaciones e invariantes).
- Paso 3: Explicar en qué contextos aporta mayor valor (dominios con reglas ricas, interfaces intercambiables, evolución en equipo).
-->

---
layout: code-explain
clicks: 2
transition: slide-left
kicker: "Bloque 1 · Motivación en Ingeniería de Software"
kickerVariant: "problem"
title: "Problemas que Impulsaron el Modelo de Objetos"
badge: "3 pasos interactivos"
---

<SoftwareCrisisDiagram />

<!--
Notas de exposición (Diapositiva 3 — Problemas de ingeniería de software):
- Paso 1: Explicar el efecto dominó cuando múltiples funciones dependen de la representación física exacta de una estructura global o compartida.
- Paso 2: Mostrar el riesgo de validaciones dispersas: basta con que una función olvide validar una regla para corromper el estado.
- Paso 3: Mostrar cómo la frontera de contrato aísla la representación interna detrás de métodos públicos.
-->

---
layout: code-explain
clicks: 5
transition: slide-left
kicker: "Bloque 1 · Origen y Evolución Histórica"
kickerVariant: "class"
title: "De Simula 67 a los Lenguajes Multiparadigma"
badge: "Línea de tiempo · 6 hitos"
---

<HistoryTimeline />

<!--
Notas de exposición (Diapositiva 4 — Línea de tiempo histórica):
- Recorrer los 6 hitos: Simula 67 (Dahl y Nygaard: clases para simulación física), Smalltalk-72/80 (Alan Kay: paso de mensajes), C++ (Stroustrup: abstracción de costo cero en sistemas), Python (1991: modelo uniforme de objetos y protocolos), Java (1995: adopción empresarial masiva) y C# / lenguajes multiparadigma modernos (2000+).
-->

---
layout: code-explain
clicks: 3
transition: slide-left
kicker: "Bloque 2 · Fundamentos y Estructuras"
kickerVariant: "class"
title: "Anatomía de una Clase en Python"
badge: "4 etapas en el código"
---

<ClassAnatomyStepper />

<!--
Notas de exposición (Diapositiva 5 — Clases, constructores, atributos y métodos):
- Etapa 1: La clase como molde y tipo que define estructura y contrato común, sin reservar aún estado individual.
- Etapa 2: El inicializador __init__ establece el estado válido inicial y rechaza parámetros fuera de rango desde el nacimiento del objeto.
- Etapa 3: Atributos internos y propiedades (@property) exponen consultas seguras sin habilitar escrituras arbitrarias.
- Etapa 4: Los métodos definen el comportamiento y las transiciones de estado válidas.
-->

---
layout: code-explain
clicks: 3
transition: slide-left
kicker: "Bloque 2 · Instanciación y Referencias"
kickerVariant: "interface"
title: "De un Único Molde a Múltiples Instancias Vivas"
badge: "Diagrama animado · 4 pasos"
---

<ObjectInstancesDiagram />

<!--
Notas de exposición (Diapositiva 6 — Instanciación, estado independiente y aliasing):
- Paso 1: La clase CuentaBancaria define el comportamiento compartido.
- Paso 2: Dos llamadas al constructor producen dos objetos distintos con estados independientes (ana y bruno).
- Paso 3: Invocación de métodos (ana.transferir_a(bruno, 10_000)): colaboración coordinada entre instancias.
- Paso 4: Referencias y aliasing (alias = ana): ambas variables apuntan al mismo objeto en memoria, no crean una copia.
-->

---
layout: code-explain
clicks: 2
transition: slide-left
kicker: "Bloque 2 · Interacción y Semántica de Referencias"
kickerVariant: "valid"
title: "Paso de Mensajes, Identidad (<code>is</code>) e Igualdad (<code>==</code>)"
badge: "3 demostraciones Python"
---

<MessagePassingShowcase />

<!--
Notas de exposición (Diapositiva 7 — Paso de mensajes, identidad vs igualdad y copias defensivas):
- Paso 1: Carrito colabora con instancias de Producto delegándoles consultas a través de métodos públicos.
- Paso 2: Diferenciar identidad de referencia (is) frente a igualdad lógica de valor (== / __eq__).
- Paso 3: Riesgo de exponer colecciones mutables internas y cómo evitar el aliasing accidental devolviendo una tupla inmutable.
-->

---
layout: code-explain
clicks: 2
transition: slide-left
kicker: "Bloque 3 · Pilar 1 de POO"
kickerVariant: "interface"
title: "Abstracción e Invariantes de Representación"
badge: "Problema → Contrato → Evolución"
---

<AbstractionContractSplit />

<!--
Notas de exposición (Diapositiva 8 — Abstracción e invariantes):
- Paso 1: Mostrar qué ocurre cuando el cliente manipula datos crudos sin contrato (ej. duraciones o escalas incompatibles).
- Paso 2: Clase Temperatura con invariante física estricta (_kelvin >= 0.0) garantizada en todos los constructores y propiedades.
- Paso 3: Independencia de representación: se puede cambiar la unidad interna sin romper el código cliente.
-->

---
layout: code-explain
clicks: 2
transition: slide-left
kicker: "Bloque 3 · Pilar 2 de POO"
kickerVariant: "valid"
title: "Encapsulamiento y Visibilidad en Python"
badge: "Demostración en 3 pasos"
---

<EncapsulationShowcase />

<!--
Notas de exposición (Diapositiva 9 — Encapsulamiento):
- Paso 1: Estructura mutable expuesta donde cualquier resta directa deja un saldo inválido (-$15.000).
- Paso 2: Clase CuentaBancaria con _saldo (convención PEP 8 de miembro protegido) y @property; aclarar diferencia con __saldo (name mangling _CuentaBancaria__saldo para evitar colisiones en subclases, no privacidad de compilador).
- Paso 3: Verificación en tiempo de ejecución: ante sobregiro, lanza ValueError antes de mutar _saldo.
-->

---
layout: lab-entry
transition: fade-out
kicker: "Laboratorio 01 · Python + WebAssembly"
kickerVariant: "valid"
title: "Práctica en Vivo: Encapsulamiento e Invariantes"
badge: "Lab 01 · Ejecutable"
---

<LabLaunchpad
  slug="01-encapsulamiento"
  summary="Experimentá con <code>CuentaBancaria</code> en Python real ejecutado en el navegador con Pyodide: probá montos válidos, sobregiros rechazados y colaboración entre dos instancias."
  :hints="['1. Sobregiro (&gt; $30.000)', '2. Escritura directa <code>cuenta.saldo</code>', '3. Transferencia entre instancias']"
/>

<!--
Notas de exposición (Diapositiva 10 — Laboratorio 01):
- Demostrar brevemente el deslizador de extracción superando los $30.000 para ver cómo el diccionario crudo se corrompe mientras CuentaBancaria preserva su invariante.
-->

---
layout: code-explain
clicks: 2
transition: slide-left
kicker: "Bloque 3 · Pilar 3 de POO"
kickerVariant: "class"
title: "Herencia, Clases Abstractas y Subtipado"
badge: "Problema → Jerarquía → Reglas"
---

<InheritanceShowcase />

<!--
Notas de exposición (Diapositiva 11 — Herencia):
- Paso 1: Clases desconectadas que duplican atributos y validaciones comunes.
- Paso 2: Clase base abstracta Envio(ABC) con @abstractmethod costo(), reutilización con super().__init__() y especialización en subclases.
- Paso 3: Distinguir herencia de código (subclase) frente a subtipado conductual (Liskov) y mencionar el algoritmo C3 MRO de Python en herencia múltiple.
-->

---
layout: code-explain
clicks: 2
transition: slide-left
kicker: "Bloque 3 · Diseño de Relaciones"
kickerVariant: "problem"
title: "Herencia («es-un») vs. Composición y Delegación («tiene-un»)"
badge: "Antipatrón → Solución → Criterio"
---

<CompositionVsInheritance />

<!--
Notas de exposición (Diapositiva 12 — Composición y delegación frente a herencia):
- Paso 1: Mostrar por qué heredar de list para construir una Pila rompe la disciplina LIFO (el cliente hereda pop(0), sort, insert) y genera el problema de la clase base frágil.
- Paso 2: Reescribir PilaSegura componiendo una lista interna privada y delegando únicamente apilar, desapilar y tope.
- Paso 3: Sintetizar la regla práctica: heredar solo ante relación genuina de subtipo; componer y delegar para reutilizar mecanismos.
-->

---
layout: code-explain
clicks: 3
transition: slide-left
kicker: "Bloque 3 · Pilar 4 de POO"
kickerVariant: "interface"
title: "Polimorfismo y Despacho Dinámico"
badge: "4 vistas · Mecanismos y tipos"
---

<PolymorphismDispatch />

<!--
Notas de exposición (Diapositiva 13 — Polimorfismo y despacho dinámico):
- Paso 1: Cadena rígida de isinstance / if-elif que obliga a editar el emisor ante cada nuevo canal.
- Paso 2: Despacho dinámico con Protocol en Python: emitir_alertas envía canal.enviar(mensaje) sin conocer la clase concreta.
- Paso 3: Explicar cómo funciona internamente: vptr/vtable en lenguajes compilados estáticos (C++) vs búsqueda dinámica en __class__ y MRO en Python.
- Paso 4: Distinguir polimorfismo de subtipos/protocolos (inclusión) frente a polimorfismo paramétrico (Generic[T]) y ad-hoc (sobrecarga/@singledispatch).
-->

---
layout: lab-entry
transition: fade-out
kicker: "Laboratorio 02 · Python + WebAssembly"
kickerVariant: "valid"
title: "Práctica en Vivo: Herencia y Despacho Dinámico"
badge: "Lab 02 · Ejecutable"
---

<LabLaunchpad
  slug="02-herencia-polimorfismo"
  summary="Procesá un lote heterogéneo de <code>EnvioEstandar</code>, <code>EnvioExpres</code> y <code>EnvioRefrigerado</code> con una única función polimórfica y creá tu propia subclase <code>EnvioDronUrbano</code> en el editor."
  :hints="['1. Ajustar distancia y peso del lote', '2. Activar recargo urgente expres', '3. Extender <code>EnvioDronUrbano</code> en Sandbox']"
/>

<!--
Notas de exposición (Diapositiva 14 — Laboratorio 02):
- Mostrar en el simulador cómo procesar_lote_envios invoca e.costo() sobre las 3 subclases sin usar condicionales de tipo.
-->

---
layout: code-explain
clicks: 4
transition: slide-left
kicker: "Bloque 4 · Principios de Diseño Orientado a Objetos"
kickerVariant: "class"
title: "Principios SOLID: Alta Cohesión y Bajo Acoplamiento"
badge: "Explorador S · O · L · I · D"
---

<SolidInteractiveMap />

<!--
Notas de exposición (Diapositiva 15 — Principios SOLID):
- Priorizar la comprensión sobre las siglas:
  - S (Responsabilidad Única): separar modelo, persistencia y formato.
  - O (Abierto/Cerrado): agregar nuevas reglas mediante nuevas clases sin reescribir el motor probado.
  - L (Sustitución de Liskov): un subtipo nunca debe romper las garantías del supertipo (ej. Cuadrado heredando de Rectangulo mutable).
  - I (Segregación de Interfaces): contratos cohesivos pequeños en lugar de interfaces monolíticas.
  - D (Inversión de Dependencias): el dominio depende de abstracciones, no de motores concretos.
-->

---
layout: code-explain
clicks: 2
transition: slide-left
kicker: "Bloque 4 · Patrón de Comportamiento"
kickerVariant: "valid"
title: "Patrón Strategy: Algoritmos Intercambiables en Vivo"
badge: "Problema → Diagrama → Ejecución"
---

<StrategyShowcase />

<!--
Notas de exposición (Diapositiva 16 — Patrón Strategy):
- Paso 1: Método monolítico acoplado a banderas de texto ("regular", "beca", "efectivo").
- Paso 2: Separar el contexto Pedido del protocolo EstrategiaDescuento mediante composición.
- Paso 3: Demostrar en código cómo el mismo objeto Pedido cambia su estrategia en tiempo de ejecución sin recrear la instancia.
-->

---
layout: code-explain
clicks: 1
transition: slide-left
kicker: "Bloque 4 · Patrones Estructurales"
kickerVariant: "interface"
title: "Adapter y Decorator: Integrar y Extender sin Heredar"
badge: "2 patrones con diagramas"
---

<AdapterDecoratorSplit />

<!--
Notas de exposición (Diapositiva 17 — Adapter y Decorator):
- Pestaña 1 (Adapter): Traduce una interfaz externa incompatible (PasarelaExternaSDK.send_payment_cents) al contrato esperado por nuestro dominio sin contaminarlo.
- Pestaña 2 (Decorator): Envuelve un objeto que implementa el mismo protocolo para sumar responsabilidades (prefijos, auditoría, reintentos) de forma apilable sin explosión de subclases.
-->

---
layout: lab-entry
transition: fade-out
kicker: "Laboratorio 03 · Python + WebAssembly"
kickerVariant: "valid"
title: "Práctica en Vivo: Patrón Strategy en un Pedido"
badge: "Lab 03 · Ejecutable"
---

<LabLaunchpad
  slug="03-patron-strategy"
  summary="Intercambiá en caliente la política de descuento de un mismo objeto <code>Pedido</code> y compará simultáneamente las cuatro estrategias o programá <code>DescuentoDocenteInvestigador</code>."
  :hints="['1. Alternar 4 estrategias en caliente', '2. Variar monto y cantidad de ítems', '3. Programar nueva estrategia en Sandbox']"
/>

<!--
Notas de exposición (Diapositiva 18 — Laboratorio 03):
- Cambiar el selector de estrategia en vivo para evidenciar cómo Pedido delega el cálculo sin ningún if/elif en su código.
-->

---
layout: code-explain
clicks: 2
transition: slide-left
kicker: "Bloque 5 · Análisis Crítico de Ingeniería"
kickerVariant: "problem"
title: "Compromisos (Trade-offs), Memoria y Límites de POO"
badge: "3 dimensiones de análisis"
---

<TradeoffsMatrix />

<!--
Notas de exposición (Diapositiva 19 — Trade-offs y cuándo NO usar POO):
- Paso 1: Contrastar beneficios reales (invariantes, extensibilidad) frente a costos reales (complejidad accidental si se crean jerarquías especulativas).
- Paso 2: Rigor técnico en memoria y caché: evitar generalizaciones falsas ("todo objeto vive siempre en el heap"). Depende del lenguaje (valor en pila en C++/structs vs referencias en Python, devirtualización JIT, localidad espacial SoA vs AoS).
- Paso 3: Casos donde otro enfoque es preferible: scripts breves de transformación, cómputo numérico/vectorial y pipelines puros sin estado.
-->

---
layout: code-explain
clicks: 2
transition: slide-left
kicker: "Bloque 5 · Comparación Multiparadigma"
kickerVariant: "interface"
title: "Un Mismo Problema en Python: Imperativo, POO y Funcional"
badge: "3 soluciones equivalentes O(n)"
---

<ParadigmTriadComparison />

<!--
Notas de exposición (Diapositiva 20 — Comparación Imperativo vs POO vs Funcional):
- Mostrar el mismo lote de ventas resuelto con los tres enfoques en Python:
  1. Imperativo/Procedural: bucle directo con acumuladores locales (simple y explícito).
  2. Orientado a Objetos: VentaConfirmada + ProcesadorVentasPOO con invariantes y formato desacoplable.
  3. Funcional: @dataclass(frozen=True) + comprensión pura sin mutación de estado.
- Subrayar que los tres recorren el lote en tiempo O(n) y arrojan idéntico resultado; ninguno es universalmente superior.
-->

---
layout: lab-entry
transition: fade-out
kicker: "Laboratorio 04 · Python + WebAssembly"
kickerVariant: "valid"
title: "Práctica en Vivo: Comparación de los 3 Paradigmas"
badge: "Lab 04 · Ejecutable"
---

<LabLaunchpad
  slug="04-comparacion-paradigmas"
  summary="Ejecutá en paralelo las implementaciones Imperativa, Orientada a Objetos y Funcional sobre el mismo lote configurable de ventas y verificá su equivalencia matemática."
  :hints="['1. Modificar IVA y umbral mayorista', '2. Verificar equivalencia exacta <code>O(n)</code>', '3. Agregar descuento extra en los 3 estilos']"
/>

<!--
Notas de exposición (Diapositiva 21 — Laboratorio 04):
- Mostrar en pantalla cómo al cambiar la alícuota de IVA o el umbral mayorista las tres implementaciones coinciden al centavo.
-->

---
layout: conclusions
transition: slide-left
kicker: "Bloque 6 · Conclusiones Metodológicas"
kickerVariant: "class"
title: "Cómo Elegir el Paradigma Adecuado en Ingeniería"
badge: "Síntesis conceptual"
---

<ConclusionsSynthesis />

<!--
Notas de exposición (Diapositiva 22 — Conclusiones):
- Cerrar con las tres preguntas guía de ingeniería: ¿qué invariantes debemos proteger?, ¿qué ejes van a variar? y ¿cuál es el costo dominante del proyecto?
- Destacar cómo el software moderno en Python combina fronteras modulares orientadas a objetos con transformaciones funcionales internas e implementaciones algorítmicas imperativas claras.
-->

---
layout: conclusions
transition: fade-out
kicker: "Bloque 6 · Cierre y Referencias Académicas"
kickerVariant: "valid"
title: "Bibliografía Consultada y Acceso a Laboratorios"
badge: "Programación I · 2026"
---

<BibliographyAndResources />

<!--
Notas de exposición (Diapositiva 23 — Bibliografía y recursos):
- Presentar las fuentes primarias y libros de referencia utilizados para elaborar la exposición y el trabajo práctico.
- Dejar en pantalla los accesos directos y el botón de código QR para preguntas de la cátedra y exploración libre desde los celulares.
-->
